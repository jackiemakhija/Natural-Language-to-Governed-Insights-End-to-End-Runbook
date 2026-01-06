@echo off
REM Deploy Natural Language to Governed Insights to HF Spaces (Windows)

echo ==========================================================
echo  Natural Language to Governed Insights - HF Deployment
echo ==========================================================
echo.

REM Configuration
set /p HF_USERNAME="Enter your Hugging Face username: "
set /p SPACE_NAME="Enter your Space name (e.g., nl-governed-insights): "

set SPACE_URL=https://huggingface.co/spaces/%HF_USERNAME%/%SPACE_NAME%

echo.
echo Deployment Configuration:
echo   Username: %HF_USERNAME%
echo   Space Name: %SPACE_NAME%
echo   Space URL: %SPACE_URL%
echo.

REM Check git
git --version >nul 2>&1
if errorlevel 1 (
    echo Error: git is not installed
    exit /b 1
)

REM Create deployment directory
set DEPLOY_DIR=hf_deploy_temp
echo Creating deployment directory...
if exist %DEPLOY_DIR% rmdir /s /q %DEPLOY_DIR%
mkdir %DEPLOY_DIR%
cd %DEPLOY_DIR%

REM Initialize git
echo Initializing git repository...
git init
git lfs install

REM Add remote
echo Adding Hugging Face remote...
git remote add origin %SPACE_URL%

REM Copy files
echo Copying application files...
copy ..\app.py .
copy ..\main.py .
copy ..\requirements.txt .
copy ..\Dockerfile .
xcopy /E /I ..\src src
xcopy /E /I ..\data data
xcopy /E /I ..\config config

REM Copy README
echo Preparing README...
copy ..\README_HF.md README.md

REM Create .gitignore
(
echo __pycache__/
echo *.pyc
echo *.pyo
echo .Python
echo .env
echo .venv
echo *.log
echo .pytest_cache/
echo logs/
) > .gitignore

REM Git operations
echo Adding files to git...
git add .

echo Creating commit...
git commit -m "Deploy Natural Language to Governed Insights"

REM Push
echo.
echo Pushing to Hugging Face Spaces...
git push -u origin main --force

echo.
echo ==========================================================
echo  Deployment Complete!
echo ==========================================================
echo.
echo Next Steps:
echo   1. Visit: %SPACE_URL%
echo   2. Wait for build (2-3 minutes^)
echo   3. (Optional^) Add Azure secrets for full features
echo   4. Test with sample queries!
echo.
echo Space URL: %SPACE_URL%
echo.

REM Cleanup
cd ..
set /p CLEANUP="Remove deployment directory? (y/n): "
if /i "%CLEANUP%"=="y" (
    rmdir /s /q %DEPLOY_DIR%
    echo Cleanup complete
)

echo.
echo Deployment finished!
pause
