; =========================================================
; INNO SETUP SCRIPT - TAILOR BOOK
; =========================================================
; Build the app first (see build.bat), then compile this file with
; Inno Setup 6. The installer is written to installer_output\.

#define MyAppName "Tailor Book"
; Keep in step with APP_VERSION in config.py
#define MyAppVersion "1.1.0"
; Your business name, shown in "Apps & features" and the installer
#define MyAppPublisher "Tailor Book"
#define MyAppExeName "TailorBook.exe"

[Setup]
; Keep this AppId the same in every release so new versions upgrade the
; old install (it was also used by "Tailor Management System").
AppId={{A3D89421-512E-4C3D-88FA-749B890F3B91}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
; Add these once you have a website:
; AppPublisherURL=https://www.yourdomain.in
; AppSupportURL=https://www.yourdomain.in/support
; AppUpdatesURL=https://www.yourdomain.in/download

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Branding
SetupIconFile=assets\brand\tailorbook.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
WizardImageFile=assets\brand\wizard_large.bmp
WizardSmallImageFile=assets\brand\wizard_small.bmp

; Output file
OutputDir=installer_output
OutputBaseFilename=TailorBook_Setup_v{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[InstallDelete]
; Remove files and shortcuts left by the old "Tailor Management System" name
Type: files; Name: "{app}\TailorManagement.exe"
Type: files; Name: "{autoprograms}\Tailor Management System.lnk"
Type: files; Name: "{autodesktop}\Tailor Management System.lnk"

[Files]
; Everything PyInstaller built (see build.bat)
Source: "dist\TailorBook\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
