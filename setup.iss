; =========================================================
; INNO SETUP SCRIPT FOR TAILOR MANAGEMENT SYSTEM
; =========================================================

#define MyAppName "Tailor Management System"
#define MyAppVersion "1.0.1"
#define MyAppPublisher "Your Name or Company"
#define MyAppURL "https://yourdomain.com"
#define MyAppExeName "TailorManagement.exe"

[Setup]
AppId={{A3D89421-512E-4C3D-88FA-749B890F3B91}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation path in Program Files
DefaultDirName={autopf}\TailorManagement
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output file configuration
OutputDir=installer_output
OutputBaseFilename=TailorManagementSetup_v1.0.1
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Copy all compiled files from the PyInstaller output
Source: "dist\TailorManagement\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent