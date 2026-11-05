"""Synthetic regression: DOI existence checks cannot chase publisher redirects.

Loopback HTTP and injected openers only. No article acquisition or external DOI
requests; a successful existence result is not scientific source verification.
"""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib
import sys
import threading
from pathlib import Path
from urllib.error import HTTPError
import urllib.request

import pytest

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "scripts"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
dr = importlib.import_module("assurance.doi_resolver")


def test_no_redirect_handler_refuses_synthetic_publisher_hop():
    hits = []

    class LocalHandler(BaseHTTPRequestHandler):
        def do_HEAD(self):
            hits.append(self.path)
            self.send_response(302 if self.path == "/doi" else 200)
            if self.path == "/doi":
                self.send_header("Location", "/publisher")
            self.end_headers()

        def log_message(self, *_args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), LocalHandler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        request = urllib.request.Request(
            f"http://127.0.0.1:{server.server_port}/doi", method="HEAD"
        )
        opener = urllib.request.build_opener(dr._NoPublisherRedirect())
        with pytest.raises(HTTPError) as err:
            opener.open(request, timeout=5)
        assert err.value.code == 302
        assert hits == ["/doi"]
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


def test_real_fetcher_selects_no_redirect_opener_and_preserves_302(monkeypatch):
    builds, requests = [], []

    def fake_build_opener(handler):
        builds.append(handler)

        class SyntheticOpener:
            def open(self, req, timeout):
                requests.append((req.full_url, req.get_method(), timeout))
                raise HTTPError(
                    req.full_url, 302, "Moved",
                    {"Location": "https://publisher.invalid/synthetic"}, None
                )
        return SyntheticOpener()

    monkeypatch.setattr(dr.urllib.request, "build_opener", fake_build_opener)
    assert dr.http_head_fetcher("10.9999/synthetic", timeout=2) == ("resolved", 302)
    assert len(builds) == 1 and isinstance(builds[0], dr._NoPublisherRedirect)
    assert requests == [("https://doi.org/10.9999/synthetic", "HEAD", 2)]


@pytest.mark.parametrize("code,verdict", [
    (404, "unresolved"), (410, "unresolved"), (403, "unknown"),
])
def test_negative_status_controls_do_not_follow_or_promote(monkeypatch, code, verdict):
    class SyntheticOpener:
        def open(self, req, timeout):
            raise HTTPError(req.full_url, code, "fixture", {}, None)

    monkeypatch.setattr(
        dr.urllib.request, "build_opener", lambda handler: SyntheticOpener()
    )
    assert dr.http_head_fetcher("10.9999/synthetic") == (verdict, code)


@pytest.mark.parametrize("location", [
    None, "", "/publisher", "javascript:alert(1)", "https://",
    "https://[unclosed", "https://publisher.invalid/\\r\\nbad",
])
def test_redirect_missing_or_malformed_location_is_inconclusive(monkeypatch, location):
    """A bare 3xx status is not proof of DOI resolution; never follow it."""
    requests = []

    class SyntheticOpener:
        def open(self, req, timeout):
            requests.append((req.full_url, req.get_method()))
            headers = {"Location": location} if location is not None else {}
            raise HTTPError(req.full_url, 302, "synthetic", headers, None)

    monkeypatch.setattr(
        dr.urllib.request, "build_opener", lambda handler: SyntheticOpener()
    )
    assert dr.http_head_fetcher("10.9999/synthetic") == ("unknown", 302)
    assert requests == [("https://doi.org/10.9999/synthetic", "HEAD")]


@pytest.mark.parametrize("code", [301, 302, 303, 307, 308])
def test_redirect_with_absolute_web_location_remains_resolved(monkeypatch, code):
    """Valid DOI-service redirects remain sufficient without fetching publishers."""
    requests = []

    class SyntheticOpener:
        def open(self, req, timeout):
            requests.append(req.full_url)
            raise HTTPError(
                req.full_url, code, "synthetic",
                {"Location": "https://publisher.invalid/synthetic"}, None
            )

    monkeypatch.setattr(
        dr.urllib.request, "build_opener", lambda handler: SyntheticOpener()
    )
    assert dr.http_head_fetcher("10.9999/synthetic") == ("resolved", code)
    assert requests == ["https://doi.org/10.9999/synthetic"]
