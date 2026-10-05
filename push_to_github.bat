@echo off
echo ============================================================
echo Pushing AI Workforce Upskilling Platform to GitHub
echo Target: https://github.com/yashshitole2124/ai-workforce-upskilling-platform
echo ============================================================
cd /d "%~dp0"
git branch -M main
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ============================================================
    echo SUCCESS! Repository successfully pushed to:
    echo https://github.com/yashshitole2124/ai-workforce-upskilling-platform
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo [ACTION NEEDED]
    echo If you have not created the repository on GitHub yet:
    echo 1. Open: https://github.com/new?name=ai-workforce-upskilling-platform
    echo 2. Click 'Create repository' (Do not add README or .gitignore)
    echo 3. Run this batch file again!
    echo ============================================================
)
pause
