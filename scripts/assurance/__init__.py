"""Phase-3 assurance helpers.

These modules populate the heavier checks in assurance.json that need
external resources (per-project rerun scripts, PDFs) and so couldn't ship
in Phase 1/2. Each helper degrades to `not-run` when its inputs aren't
present, so adding the resource for one project doesn't break others.
"""
