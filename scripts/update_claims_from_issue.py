"""Parse a GitHub issue body (form-template format) and update claims.json.

Invoked by .github/workflows/update-claims.yml on issues:opened/edited/
labeled/closed/reopened events. Reads env vars set by GitHub Actions:

  ISSUE_NUMBER, ISSUE_TITLE, ISSUE_BODY, ISSUE_USER, ISSUE_LABELS,
  ISSUE_STATE, ISSUE_CREATED_AT

Label 'claim' → adds/updates a claim entry with status='claimed'.
Label 'submitted' → updates the matching claim to status='submitted'.
Closed issue → removes from claims.json (paper reopens).
"""
from __future__ import annotations
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

CLAIMS = Path(__file__).resolve().parents[1] / "claims.json"


def parse_form_body(body: str) -> dict[str, str]:
    """GitHub form templates render issue body as:

        ### Field Label 1

        value 1

        ### Field Label 2

        value 2

    Convert to {label_slug: value} dict.
    """
    out: dict[str, str] = {}
    if not body:
        return out
    # Split on "### " headers
    parts = re.split(r"^###\s+", body, flags=re.MULTILINE)
    for part in parts[1:]:
        lines = part.strip().splitlines()
        if not lines:
            continue
        label = lines[0].strip()
        # Value = non-blank lines after the label until next ### (already split)
        value_lines = [l for l in lines[1:] if l.strip()]
        value = "\n".join(value_lines).strip()
        # Normalize: "_No response_" is GitHub's placeholder when a non-required field is blank
        if value in {"_No response_", "None"}:
            value = ""
        # Slugify label
        slug = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
        out[slug] = value
    return out


def find_label_value(parsed: dict, *keys: str) -> str:
    """Look up any of the given slug keys, prefix-match tolerant."""
    for k in keys:
        # Exact match
        if k in parsed:
            return parsed[k]
        # Prefix match (handles slight label rewording)
        for pk, pv in parsed.items():
            if pk.startswith(k):
                return pv
    return ""


def main() -> int:
    title = os.environ.get("ISSUE_TITLE", "")
    body = os.environ.get("ISSUE_BODY", "")
    state = os.environ.get("ISSUE_STATE", "open")
    created_at = os.environ.get("ISSUE_CREATED_AT", "")
    labels_json = os.environ.get("ISSUE_LABELS", "[]")
    user = os.environ.get("ISSUE_USER", "")
    issue_num = os.environ.get("ISSUE_NUMBER", "")

    try:
        labels = [lab["name"] for lab in json.loads(labels_json)]
    except Exception:
        labels = []

    parsed = parse_form_body(body)
    paper_num = find_label_value(parsed, "paper_number", "paper_no", "paper")
    # Strip anything non-digit (students sometimes prefix with #)
    paper_num = re.sub(r"[^\d]", "", paper_num)
    if not paper_num:
        # Fall back to title parsing: [CLAIM #123] Name  or [SUBMITTED #123] Name
        m = re.search(r"#(\d+)", title)
        if m:
            paper_num = m.group(1)

    if not paper_num:
        print(f"[warn] no paper_number parseable from issue #{issue_num}; skipping")
        return 0

    # Load existing claims
    if CLAIMS.is_file():
        claims = json.loads(CLAIMS.read_text(encoding="utf-8") or "{}")
    else:
        claims = {}

    today = dt.date.today().isoformat()
    # Prefer GitHub's issue-created timestamp for claim date (canonical)
    if created_at:
        try:
            claim_date = dt.datetime.fromisoformat(created_at.replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            claim_date = today
    else:
        claim_date = today

    # If issue was closed, treat as cancellation — remove the claim.
    # (Submission confirmation leaves the issue open with 'submitted' label.)
    #
    # CLAIM-SPOOFING GUARD (P1-3 from 2026-04-15 system review):
    # Anyone can open a GitHub issue. Without this check, a third party
    # could open a new issue for someone else's paper_num, then close it,
    # and silently delete the original student's claim. The fix: require
    # the closer to be the same github_user that originally claimed it.
    # If the user differs, we IGNORE the close and log a warning so the
    # board owner can investigate.
    # P1-14 — single write path: branches below only mutate `claims` (or
    # return early on spoof detection). The file is written once at the
    # end of main().
    if state == "closed" and "submitted" not in labels:
        existing_claim = claims.get(paper_num)
        if existing_claim is None:
            print(f"[info] issue #{issue_num} closed but no claim for #{paper_num}")
        else:
            owner = existing_claim.get("github_user", "")
            if owner and user and owner != user:
                print(
                    f"[warn] issue #{issue_num} closed by '{user}' but claim "
                    f"#{paper_num} is owned by '{owner}'. Ignoring close to "
                    f"prevent claim-spoofing. The original claimant must close "
                    f"their own issue."
                )
                return 2
            print(f"[info] issue #{issue_num} closed → removing claim #{paper_num}")
            del claims[paper_num]

    if "submitted" in labels:
        # Update existing claim (if any) to submitted status.
        # Same spoofing guard: if a different user adds the 'submitted' label
        # to someone else's claim, refuse the update.
        existing = claims.get(paper_num, {})
        owner = existing.get("github_user", "")
        if owner and user and owner != user:
            print(
                f"[warn] issue #{issue_num} 'submitted' label set by '{user}' "
                f"but claim #{paper_num} is owned by '{owner}'. Ignoring "
                f"submission update to prevent claim-spoofing."
            )
            return 2
        submit_date = find_label_value(parsed, "date_of_submission", "submit_date") or today
        submission_id = find_label_value(parsed, "submission_confirmation", "submission_id", "manuscript_id", "doi")
        name = find_label_value(parsed, "your_name") or existing.get("name", "")
        claims[paper_num] = {
            **existing,
            "name": name,
            "status": "submitted",
            "submit_date": submit_date,
            "submission_id": submission_id,
            "issue_number": int(issue_num) if issue_num else None,
            "github_user": user,
        }
        if "claim_date" not in claims[paper_num]:
            claims[paper_num]["claim_date"] = claim_date
        print(f"[info] marked #{paper_num} SUBMITTED by {name} (issue #{issue_num})")

    elif "extension" in labels:
        # 10-day auto-approved extension.
        # Must reference an existing claim owned by this user.
        existing = claims.get(paper_num, {})
        owner = existing.get("github_user", "")
        if not owner:
            print(
                f"[warn] issue #{issue_num} requested EXTENSION for #{paper_num} "
                f"by '{user}', but there is no active claim. Ignoring."
            )
            return 2
        if owner and user and owner != user:
            print(
                f"[warn] issue #{issue_num} requested EXTENSION for #{paper_num} "
                f"by '{user}', but claim is owned by '{owner}'. Refusing."
            )
            return 2
        if existing.get("status") != "claimed":
            print(
                f"[info] claim #{paper_num} is status={existing.get('status','?')}; "
                f"extension has no effect. Skipping."
            )
            return 0
        claims[paper_num] = {**existing, "extended": True}
        print(f"[info] granted 10-day auto-extension for #{paper_num} (now 40-day window)")

    elif "claim" in labels:
        # New or updated claim.
        # Spoofing guard: if this paper is ALREADY claimed by a different
        # github_user, refuse the new claim. Same user re-opening / editing
        # their own issue is fine and overwrites freely.
        #
        # P1-4 — GRACE PERIOD. After a claim expires, don't immediately let
        # a different user overwrite it on day 31. Keep ownership sticky for
        # an additional 48 hours so the original claimant has a small window
        # to request an extension (or notice they missed the deadline and
        # submit). After the grace period, the paper truly reopens.
        prior = claims.get(paper_num, {})
        prior_owner = prior.get("github_user", "")
        prior_status = prior.get("status", "")
        EXPIRY_GRACE_DAYS = 2

        def _claim_is_within_grace(claim: dict) -> bool:
            """True if expired but still within grace window."""
            if claim.get("status") != "claimed":
                return False
            cd_str = claim.get("claim_date", "")
            try:
                cd = dt.date.fromisoformat(cd_str)
            except ValueError:
                return False
            win = 40 if claim.get("extended") else 30
            age = (dt.date.today() - cd).days
            return win < age <= win + EXPIRY_GRACE_DAYS

        if prior_owner and user and prior_owner != user:
            if prior_status == "claimed" or _claim_is_within_grace(prior):
                print(
                    f"[warn] issue #{issue_num} attempted CLAIM of #{paper_num} by "
                    f"'{user}', but paper is still owned by '{prior_owner}' "
                    f"(claim_date={prior.get('claim_date', '?')}; "
                    f"grace={EXPIRY_GRACE_DAYS}d). Refusing to overwrite."
                )
                return 2

        # One-paper-at-a-time rule: a given user may hold AT MOST one active
        # (non-submitted, non-expired) claim at a time. Editing one's own
        # existing claim on the same paper_num is fine (prior_owner == user
        # branch above handles that). Anything else is refused until the
        # student either submits or lets the current claim expire.
        for other_num, other in claims.items():
            if other_num == paper_num:
                continue
            if other.get("status") != "claimed":
                continue  # submitted claims don't block new claims
            if other.get("github_user") != user or not user:
                continue
            # Check expiry: treat expired claims as inactive (page-side
            # JS already treats them as reopened).
            cd = other.get("claim_date", "")
            window = 40 if other.get("extended") else 30
            try:
                cd_date = dt.date.fromisoformat(cd)
                age = (dt.date.today() - cd_date).days
                if age > window:
                    continue  # expired, doesn't block
            except ValueError:
                continue
            print(
                f"[warn] issue #{issue_num}: '{user}' already holds an active "
                f"claim on paper #{other_num} (claim_date={cd}). The one-paper-"
                f"at-a-time rule refuses a new claim on #{paper_num}. Submit "
                f"or wait for #{other_num} to expire first."
            )
            return 2
        name = find_label_value(parsed, "your_name", "name")
        affiliation = find_label_value(parsed, "your_affiliation_university", "affiliation", "your_affiliation")
        email = find_label_value(parsed, "your_email", "email")
        orcid = find_label_value(parsed, "your_orcid", "orcid")
        senior_author = find_label_value(parsed, "senior_last_author_faculty_supervisor", "senior_author", "senior")
        claims[paper_num] = {
            "name": name,
            "affiliation": affiliation,
            "email": email,
            "orcid": orcid,
            "senior_author": senior_author,
            "claim_date": claim_date,
            "status": "claimed",
            "submit_date": None,
            "submission_id": None,
            "issue_number": int(issue_num) if issue_num else None,
            "github_user": user,
        }
        print(f"[info] marked #{paper_num} CLAIMED by {name} ({affiliation}), senior author: {senior_author or 'NONE'} (issue #{issue_num})")

    else:
        print(f"[info] issue #{issue_num} has neither 'claim' nor 'submitted' label; ignoring")
        return 0

    CLAIMS.write_text(json.dumps(claims, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[info] wrote {CLAIMS} ({len(claims)} total claims)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
