@echo off
echo === Londons Kitchen Data Import ===
echo.
echo Choose an import method:
echo 1. Run interactive Python script (recommended)
echo 2. Use Railway Dashboard (manual)
echo 3. Show instructions for Railway CLI
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Running interactive import script...
    python import_simple.py
) else if "%choice%"=="2" (
    echo.
    echo === Railway Dashboard Method ===
    echo 1. Go to https://railway.app
    echo 2. Open your Londons Kitchen project
    echo 3. Click on PostgreSQL database
    echo 4. Go to 'Query' tab
    echo 5. Copy contents of railway_import.sql and run
    echo.
    echo Note: Replace sample data with your actual data from local_data_export.json
    pause
) else if "%choice%"=="3" (
    echo.
    echo === Railway CLI Method ===
    echo To install Railway CLI:
    echo 1. Open PowerShell as Administrator
    echo 2. Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo 3. Run: npm install -g @railway/cli
    echo 4. Run: railway login
    echo 5. Run: railway run python import_simple.py
    pause
) else (
    echo Invalid choice. Please run again.
    pause
)