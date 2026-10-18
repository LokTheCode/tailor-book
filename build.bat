@echo off
REM =========================================================
REM  Build Tailor Book for Windows
REM    1. dist\TailorBook\TailorBook.exe   (the app, via PyInstaller)
REM    2. installer_output\TailorBook_Setup_v<version>.exe   (via Inno Setup 6)
REM  Run from the project folder:  build.bat
REM =========================================================

echo Checking settings...
python tools\prebuild_check.py || goto :error

echo Installing build tools...
pip install -r requirements.txt pyinstaller || goto :error

echo.
echo Building the app...
pyinstaller --noconfirm --clean --windowed ^
  --name TailorBook ^
  --icon assets\brand\tailorbook.ico ^
  --add-data "assets;assets" ^
  main.py || goto :error

echo.
echo Building the installer...
set ISCC="%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist %ISCC% (
  echo Inno Setup 6 not found. Install it from https://jrsoftware.org/isdl.php
  echo then run this file again, or open setup.iss in Inno Setup and click Compile.
  goto :end
)
%ISCC% setup.iss || goto :error

echo.
echo Done. Installer is in installer_output\
goto :end

:error
echo.
echo Build failed - see the messages above.
exit /b 1

:end
