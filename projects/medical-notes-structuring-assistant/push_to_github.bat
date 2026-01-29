@echo off
setlocal EnableDelayedExpansion

REM Configuration
set "REPO_URL=https://github.com/saadtoorx/generative-ai.git"
set "REL_PATH=projects/medical-notes-structuring-assistant"
set "TEMP_CLONE_DIR=%TEMP%\gene_ai_repo_%RANDOM%"
set "SOURCE_DIR=%CD%"

echo ==========================================
echo   Pushing to GitHub
echo ==========================================
echo.
echo [1/6] Cloning remote repository...
echo       URL: %REPO_URL%
git clone --depth 1 "%REPO_URL%" "%TEMP_CLONE_DIR%"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to clone repository.
    goto :Cleanup
)

echo.
echo [2/6] Creating target directory...
set "TARGET_DIR=%TEMP_CLONE_DIR%\%REL_PATH%"
if not exist "%TARGET_DIR%" (
    echo       Creating: %REL_PATH%
    mkdir "%TARGET_DIR%"
) else (
    echo       Target directory already exists. merging changes...
)

echo.
echo [3/6] Copying files...
REM Use robocopy to exclude common garbage
robocopy "%SOURCE_DIR%" "%TARGET_DIR%" /E /XD .git __pycache__ venv env .venv .idea .vscode /XF *.pyc *.pyo *.pyd .DS_Store
if %ERRORLEVEL% GEQ 8 (
    echo [ERROR] Copy failed.
    goto :Cleanup
)

echo.
echo [4/6] Staging changes...
cd /d "%TEMP_CLONE_DIR%"
git add "%REL_PATH%"

echo.
echo [5/6] Committing...
git commit -m "Add Medical Notes Structuring Assistant project"
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] No changes to commit or commit failed.
    goto :Cleanup
)

echo.
echo [6/6] Pushing to GitHub...
git push origin main
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Push failed. You may need to authenticate or resolve conflicts.
) else (
    echo.
    echo [SUCCESS] Project pushed successfully!
    echo          View at: %REPO_URL%/tree/main/%REL_PATH%
)

:Cleanup
echo.
echo [Cleanup] Removing temporary files...
cd /d "%SOURCE_DIR%"
rmdir /s /q "%TEMP_CLONE_DIR%"
echo.
echo Done.
pause
