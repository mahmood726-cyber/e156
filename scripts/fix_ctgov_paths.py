# sentinel:skip-file  (P0-hardcoded-local-path: portfolio-management script with intentional external project paths)
"""Fix ctgov paths in rewrite-workbook.txt after consolidation."""
import re

wb = "C:/E156/rewrite-workbook.txt"
text = open(wb, encoding="utf-8").read()

# Fix: PATH: C:\Projects\ctgov-xxx -> PATH: C:\Projects\ctgov-analyses\ctgov-xxx
# Handle both backslash and forward-slash variants
pattern = r"(PATH:\s*C:[/\\]Projects[/\\])(ctgov-)"
replacement = r"\1ctgov-analyses/\2"

fixed, count = re.subn(pattern, replacement, text)

# Also fix evidence dirs that moved
pattern2 = r"(PATH:\s*C:[/\\])(evidence_drift_intelligence|evidence_evolution|evidence_mizaan_intelligence|global_evidence_forecasting|medical_evolutionary_intelligence|forgotten-histories-ct)"
replacement2 = r"\1Projects/evidence-intelligence/\2"
fixed, count2 = re.subn(pattern2, replacement2, fixed)

print(f"Fixed {count} ctgov paths")
print(f"Fixed {count2} evidence paths")

open(wb, "w", encoding="utf-8").write(fixed)
print("Saved.")
