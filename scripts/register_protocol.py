#!/usr/bin/env python
"""Register a review protocol by timestamping it in Git, and inject the public
GitHub permalink back into the capsule.

A Git commit is a tamper-evident, publicly verifiable timestamp: the commit SHA
plus GitHub's recorded commit date are an open, code-native pre-registration
record (an alternative to PROSPERO for a living, reproducible review). This CLI:

  1. commits the protocol file (if not already committed) -> captures the
     registration commit SHA and its ISO timestamp;
  2. builds the permanent GitHub blob URL pinned to that SHA;
  3. injects a registration line into the capsule between the markers
     <!--PROTOREG_START--> ... <!--PROTOREG_END-->.

It fails closed: no git repo, no remote, missing protocol, or missing markers
all stop the run with a specific message. It never fabricates a link.

Usage:
  python scripts/register_protocol.py \
      --protocol protocols/sglt2-hf-protocol.md \
      --capsule  flagship/sglt2-hf-capsule.html \
      [--author-name NAME --author-email EMAIL] [--dry-run]
"""
import argparse
import io
import os
import re
import subprocess
import sys

# UTF-8 stdout on Windows consoles (cp1252 would crash on any non-ASCII).
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

START = "<!--PROTOREG_START-->"
END = "<!--PROTOREG_END-->"


def die(msg):
    print("ERROR: " + msg)
    sys.exit(1)


def git(root, *args, check=True):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        die("git %s failed: %s" % (" ".join(args), (r.stderr or r.stdout).strip()))
    return r.stdout.strip()


def repo_root(path):
    start = path if os.path.isdir(path) else os.path.dirname(os.path.abspath(path))
    r = subprocess.run(["git", "-C", start, "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        die("not inside a git repository: %s" % start)
    return r.stdout.strip()


def remote_to_https(url):
    """git@github.com:owner/repo.git or https://github.com/owner/repo(.git) -> https base."""
    url = url.strip()
    m = re.match(r"git@([^:]+):(.+?)(?:\.git)?$", url)
    if m:
        return "https://%s/%s" % (m.group(1), m.group(2))
    m = re.match(r"https?://([^/]+)/(.+?)(?:\.git)?$", url)
    if m:
        return "https://%s/%s" % (m.group(1), m.group(2))
    die("could not parse remote URL into an https base: %s" % url)


def main():
    ap = argparse.ArgumentParser(description="Timestamp a protocol in Git and link it from the capsule.")
    ap.add_argument("--protocol", required=True, help="path to the protocol markdown")
    ap.add_argument("--capsule", required=True, help="path to the capsule HTML to inject into")
    ap.add_argument("--author-name", default=None)
    ap.add_argument("--author-email", default=None)
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--dry-run", action="store_true", help="show what would happen; do not commit or write")
    args = ap.parse_args()

    if not os.path.isfile(args.protocol):
        die("protocol not found: %s" % args.protocol)
    if not os.path.isfile(args.capsule):
        die("capsule not found: %s" % args.capsule)

    root = repo_root(args.protocol)
    rel_proto = os.path.relpath(os.path.abspath(args.protocol), root).replace(os.sep, "/")

    # identity (prefer repo config; else require args) -- never writes git config
    cfg = ["-c", "user.name=%s" % args.author_name, "-c", "user.email=%s" % args.author_email] \
        if (args.author_name and args.author_email) else []
    if not cfg:
        have_name = git(root, "config", "user.name", check=False)
        have_email = git(root, "config", "user.email", check=False)
        if not (have_name and have_email):
            die("git author identity not set. Pass --author-name and --author-email "
                "(this script never writes git config).")

    # is the protocol uncommitted / modified?
    status = git(root, "status", "--porcelain", "--", rel_proto)
    already = git(root, "log", "-1", "--format=%H", "--", rel_proto)
    if status:
        if args.dry_run:
            print("[dry-run] would commit %s as the registration (then inject the permalink)." % rel_proto)
            if not already:
                print("[dry-run] no prior commit exists yet; a real run creates the registration commit now.")
                return
        else:
            git(root, "add", "--", rel_proto)
            git(root, *cfg, "-c", "commit.gpgsign=false", "commit", "-q",
                "-m", "register protocol: %s (timestamped pre-registration)" % os.path.basename(rel_proto),
                "--", rel_proto)

    sha = git(root, "log", "-1", "--format=%H", "--", rel_proto)
    if not sha:
        die("protocol has no commit yet and was not committed; cannot timestamp.")
    date = git(root, "log", "-1", "--format=%cI", "--", rel_proto)[:10]

    remote_url = git(root, "remote", "get-url", args.remote, check=False)
    if not remote_url:
        die("no '%s' remote configured; a public permalink needs a GitHub remote." % args.remote)
    base = remote_to_https(remote_url)
    permalink = "%s/blob/%s/%s" % (base, sha, rel_proto)
    short = sha[:8]

    inject = ('Protocol pre-registered <b>%s</b> &mdash; '
              '<a class="srclink" href="%s" target="_blank" rel="noopener">commit %s</a> '
              '(immutable, timestamped on GitHub).') % (date, permalink, short)

    html = open(args.capsule, encoding="utf-8").read()
    if START not in html or END not in html:
        die("capsule is missing the %s ... %s markers; add them where the "
            "registration line should appear." % (START, END))
    new = re.sub(re.escape(START) + r".*?" + re.escape(END),
                 START + inject + END, html, flags=re.S)

    print("Protocol : %s" % rel_proto)
    print("Commit   : %s  (%s)" % (sha, date))
    print("Permalink: %s" % permalink)
    if args.dry_run:
        print("[dry-run] would inject the registration line into %s" % args.capsule)
        return
    if new != html:
        with open(args.capsule, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print("Injected registration link into %s" % args.capsule)
    else:
        print("Capsule already up to date.")


if __name__ == "__main__":
    main()
