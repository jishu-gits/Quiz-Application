; ===========================================================================
; Quiz Generator Desktop — Installer
; ===========================================================================

#define AppName       "Quiz Generator"
#define AppVersion    "1.0.0"
#define AppPublisher  "Bidhan Manna"
#define AppURL        "https://github.com/jishu-gits/Quiz-Application"
#define AppExeName    "launcher.pyw"
#define DesktopRoot   ".."

[Setup]
AppId={{B3F8A2D1-7C4E-4A9B-8E5F-1D2C3B4A5E6F}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
DefaultDirName={userappdata}\Programs\{#AppName}
DefaultGroupName={#AppName}
LicenseFile={#DesktopRoot}\installer\assets\license.rtf
OutputDir={#DesktopRoot}\installer\output
OutputBaseFilename=QuizGeneratorSetup
SetupIconFile={#DesktopRoot}\installer\assets\app.ico
UninstallDisplayIcon={app}\installer\assets\app.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startmenuicon"; Description: "Create a Start Menu shortcut"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; --- Bootstrappers ---
Source: "{#DesktopRoot}\dist\QuizGeneratorBootstrap.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#DesktopRoot}\dist\QuizGeneratorLauncher.exe"; DestDir: "{app}"; Flags: ignoreversion

; --- Python Backend ---
Source: "{#DesktopRoot}\python-backend\*"; DestDir: "{app}\python-backend"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "__pycache__,*.pyc,content\*,temp\*,output\*,quiz_out\*"

; --- Java Client ---
Source: "{#DesktopRoot}\java-client\src\*"; DestDir: "{app}\java-client\src"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#DesktopRoot}\java-client\bin\*"; DestDir: "{app}\java-client\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#DesktopRoot}\java-client\lib\*"; DestDir: "{app}\java-client\lib"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#DesktopRoot}\java-client\*.jpg"; DestDir: "{app}\java-client"; Flags: ignoreversion

; --- Runtime: Embedded Python ---
Source: "{#DesktopRoot}\runtime\python\*"; DestDir: "{app}\runtime\python"; Flags: ignoreversion recursesubdirs createallsubdirs

; --- Runtime: Poppler ---
Source: "{#DesktopRoot}\runtime\poppler\*"; DestDir: "{app}\runtime\poppler"; Flags: ignoreversion recursesubdirs createallsubdirs

; --- Runtime: JRE ---
Source: "{#DesktopRoot}\runtime\jre\*"; DestDir: "{app}\runtime\jre"; Flags: ignoreversion recursesubdirs createallsubdirs

; --- Installer assets (icon for shortcuts) ---
Source: "{#DesktopRoot}\installer\assets\app.ico"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\logs"
Name: "{app}\content"
Name: "{app}\temp"
Name: "{app}\output"
Name: "{app}\quiz_out"
Name: "{app}\runtime\models"
Name: "{app}\runtime\logs"
Name: "{app}\runtime\config"

[Icons]
; Shortcuts execute QuizGeneratorLauncher.exe
Name: "{group}\{#AppName}"; Filename: "{app}\QuizGeneratorLauncher.exe"; IconFilename: "{app}\app.ico"; WorkingDir: "{app}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"; IconFilename: "{app}\app.ico"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\QuizGeneratorLauncher.exe"; IconFilename: "{app}\app.ico"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
; Launch the Launcher process after installation (which will automatically detect first-time setup via bootstrap)
Filename: "{app}\QuizGeneratorLauncher.exe"; Description: "Launch {#AppName}"; Flags: postinstall nowait

[UninstallDelete]
; Clean up logs and runtime generated files
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\python-backend\__pycache__"
Type: filesandordirs; Name: "{app}\content"
Type: filesandordirs; Name: "{app}\temp"
Type: filesandordirs; Name: "{app}\output"
Type: files; Name: "{app}\setup.state"

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  QuizDir: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    QuizDir := ExpandConstant('{app}\quiz_out');
    if DirExists(QuizDir) then
    begin
      if MsgBox('Do you want to remove your saved quiz data?' + #13#10 +
                'This cannot be undone.', mbConfirmation, MB_YESNO) = IDYES then
      begin
        DelTree(ExpandConstant('{app}\quiz_out'), True, True, True);
        // If everything is deleted, remove the main directory
        DelTree(ExpandConstant('{app}'), True, True, True);
      end;
    end;
  end;
end;
