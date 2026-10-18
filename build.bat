@echo off
REM =========================================================
REM  Build Tailor Book for Windows
REM    1. dist\TailorBook\TailorBook.exe   (the app, via PyInstaller)
REM    2. installer_output\TailorBook_Setup_v<version>.exe   (via Inno Setup 6)
REM  Double-click this file, or run  build.bat  in Command Prompt.
REM  Don't compile setup.iss in Inno Setup on its own: step 1 must run first.
REM =========================================================

REM Always work in the project folder, wherever this was started from
cd /d "%~dp0"

echo [1/4] Checking settings...
python --version >nul 2>&1 || (
  echo Python was not found. Install Python 3.11 or 3.12 from python.org
  echo and tick "Add python.exe to PATH" during install.
  goto :error
)
python tools\prebuild_check.py || goto :error

echo.
echo [2/4] Installing build tools (first time takes a few minutes)...
python -m pip install --upgrade -r requirements.txt pyinstaller || goto :error

echo.
echo [3/4] Building the app...
python -m PyInstaller --noconfirm --clean --windowed ^
  --name TailorBook ^
  --icon assets\brand\tailorbook.ico ^
  --add-data "assets;assets" ^
  main.py || goto :error

if not exist "dist\TailorBook\TailorBook.exe" (
  echo The app was not built: dist\TailorBook\TailorBook.exe is missing.
  goto :error
)

echo.
echo [4/4] Building the installer...
set ISCC="%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist %ISCC% set ISCC="%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not exist %ISCC% (
  echo Inno Setup 6 not found. Install it from https://jrsoftware.org/isdl.php
  echo The app itself is ready in dist\TailorBook\ - run this file again after installing.
  goto :error
)
%ISCC% setup.iss || goto :error

echo.
echo =========================================================
echo  Done. Your installer is in the installer_output folder:
dir /b installer_output\*.exe
echo =========================================================
explorer installer_output
goto :end

:error
echo.
echo Build stopped - read the message above.
pause
exit /b 1

:end
pause
