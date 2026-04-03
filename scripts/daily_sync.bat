@echo off
echo [%date% %time%] E156 Daily Sync starting...

:: Add any newly complete E156 projects to the workbook
cd /d C:\E156
python add_new_projects.py >NUL 2>NUL

:: Build the current batch manifest from discovered submissions
python scripts\build_batch_manifest.py >NUL 2>NUL

:: Regenerate all submissions (picks up any paper.md changes)
python scripts\generate_submission.py --batch C:\E156\scripts\_batch_all.json >NUL 2>NUL

:: Update dashboards
python scripts\create_push_helpers.py >NUL 2>NUL

:: Commit and push all submission repos plus the dashboard repo
python scripts\sync_repos.py >NUL 2>NUL

echo [%date% %time%] E156 Daily Sync complete.
