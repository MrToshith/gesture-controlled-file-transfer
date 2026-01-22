@echo off
call conda activate air_transfer
if %errorlevel% neq 0 (
    echo Failed to activate conda environment 'air_transfer'.
    echo Please make sure you have created it.
    pause
    exit /b
)
echo Starting tracker...
python tracker.py
pause
