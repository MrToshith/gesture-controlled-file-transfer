@echo off
call conda activate air_transfer
if %errorlevel% neq 0 (
    echo Failed to activate conda environment 'air_transfer'.
    echo Please make sure you have created it.
    pause
    exit /b
)
echo Starting server...
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
pause
