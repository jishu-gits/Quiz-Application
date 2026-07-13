; ===========================================================================
; Quiz Generator Desktop — Inno Setup Script
; ===========================================================================
; Build command:  iscc QuizGenerator.iss
; Requires:       Inno Setup 6.x (https://jrsoftware.org/isinfo.php)
;
; Before building, ensure the following runtime binaries are staged:
;   desktop/runtime/python/    — Python 3.12 embeddable (Windows x64)
;   desktop/runtime/poppler/   — Poppler for Windows
;   desktop/runtime/jre/       — JRE 21 (Adoptium Temurin)
;   desktop/java-client/lib/   — Jackson JAR files
;   desktop/java-client/bin/   — Compiled .class files
; See installer/README.md for exact download URLs.
; ===========================================================================

#define AppName       "Quiz Generator"
#define AppVersion    "1.0.0"
#define AppPublisher  "Bidhan Manna"
#define AppURL        "https://github.com/jishu-gits/Quiz-Application"
#define AppExeName    "launch.vbs"

; Source root is the desktop/ directory (parent of installer/)
#define DesktopRoot   ".."

[Setup]
AppId={{B3F8A2D1-7C4E-4A9B-8E5F-1D2C3B4A5E6F}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
LicenseFile={#DesktopRoot}\installer\assets\license.rtf
OutputDir={#DesktopRoot}\installer\output
OutputBaseFilename=QuizGeneratorSetup
SetupIconFile={#DesktopRoot}\installer\assets\app.ico
UninstallDisplayIcon={app}\installer\assets\app.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
MinVersion=10.0
; Allow non-admin install (user can change to per-user)
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checked
Name: "startmenuicon"; Description: "Create a Start Menu shortcut"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checked

; ===========================================================================
; Files — Bundle everything into the install directory
; ===========================================================================
[Files]
; --- Python Backend ---
Source: "{#DesktopRoot}\python-backend\*"; DestDir: "{app}\python-backend"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "__pycache__,*.pyc,content\*,temp\*,output\*,quiz_out\*"

; --- Java Client ---
Source: "{#DesktopRoot}\java-client\src\*"; DestDir: "{app}\java-client\src"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#DesktopRoot}\java-client\bin\*"; DestDir: "{app}\java-client\bin"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists(ExpandConstant('{#DesktopRoot}\java-client\bin'))
Source: "{#DesktopRoot}\java-client\lib\*"; DestDir: "{app}\java-client\lib"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists(ExpandConstant('{#DesktopRoot}\java-client\lib'))
Source: "{#DesktopRoot}\java-client\*.jpg"; DestDir: "{app}\java-client"; Flags: ignoreversion

; --- Runtime: Embedded Python ---
Source: "{#DesktopRoot}\runtime\python\*"; DestDir: "{app}\runtime\python"; Flags: ignoreversion recursesubdirs createallsubdirs

; --- Runtime: Poppler ---
Source: "{#DesktopRoot}\runtime\poppler\*"; DestDir: "{app}\runtime\poppler"; Flags: ignoreversion recursesubdirs createallsubdirs

; --- Runtime: JRE ---
Source: "{#DesktopRoot}\runtime\jre\*"; DestDir: "{app}\runtime\jre"; Flags: ignoreversion recursesubdirs createallsubdirs

; --- Scripts (startup manager, launcher, ollama installer) ---
Source: "{#DesktopRoot}\installer\scripts\startup_manager.pyw"; DestDir: "{app}\scripts"; Flags: ignoreversion
Source: "{#DesktopRoot}\installer\scripts\launch.vbs"; DestDir: "{app}\scripts"; Flags: ignoreversion
Source: "{#DesktopRoot}\installer\scripts\install_ollama.ps1"; DestDir: "{app}\scripts"; Flags: ignoreversion

; --- Installer assets (icon for shortcuts) ---
Source: "{#DesktopRoot}\installer\assets\app.ico"; DestDir: "{app}"; Flags: ignoreversion

; --- Empty runtime directories (created as markers) ---
; Actual writable dirs are created in [Code] under {localappdata}

; ===========================================================================
; Icons — Desktop and Start Menu shortcuts
; ===========================================================================
[Icons]
Name: "{group}\{#AppName}"; Filename: "wscript.exe"; Parameters: """{app}\scripts\launch.vbs"""; IconFilename: "{app}\app.ico"; WorkingDir: "{app}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"; IconFilename: "{app}\app.ico"
Name: "{autodesktop}\{#AppName}"; Filename: "wscript.exe"; Parameters: """{app}\scripts\launch.vbs"""; IconFilename: "{app}\app.ico"; WorkingDir: "{app}"; Tasks: desktopicon

; ===========================================================================
; Run — Post-install actions
; ===========================================================================
[Run]
; Optionally launch after install
Filename: "wscript.exe"; Parameters: """{app}\scripts\launch.vbs"""; Description: "Launch {#AppName}"; Flags: postinstall nowait skipifsilent

; ===========================================================================
; Uninstall — What to remove
; ===========================================================================
[UninstallDelete]
; Remove runtime logs
Type: filesandordirs; Name: "{app}\runtime\logs"
; Remove cached __pycache__
Type: filesandordirs; Name: "{app}\python-backend\__pycache__"
; Remove scripts dir
Type: filesandordirs; Name: "{app}\scripts"
; Note: {localappdata}\Quiz Generator\quiz_out is preserved (user data)

; ===========================================================================
; Code — Custom Pascal Script
; ===========================================================================
[Code]

// Create writable data directories and generate .env with absolute paths
procedure CreateDataDirectories();
var
  DataDir, ContentDir, TempDir, OutputDir, QuizDir, LogsDir, ConfigDir: String;
  EnvFile: String;
  EnvContent: TStringList;
begin
  DataDir := ExpandConstant('{localappdata}\Quiz Generator');
  ContentDir := DataDir + '\content';
  TempDir := DataDir + '\temp';
  OutputDir := DataDir + '\output';
  QuizDir := DataDir + '\quiz_out';
  LogsDir := DataDir + '\logs';
  ConfigDir := DataDir + '\config';

  // Create all data directories
  ForceDirectories(ContentDir);
  ForceDirectories(TempDir);
  ForceDirectories(OutputDir);
  ForceDirectories(QuizDir);
  ForceDirectories(LogsDir);
  ForceDirectories(ConfigDir);

  // Create runtime directories under install dir
  ForceDirectories(ExpandConstant('{app}\runtime\logs'));
  ForceDirectories(ExpandConstant('{app}\runtime\models'));
  ForceDirectories(ExpandConstant('{app}\runtime\config'));

  // Generate .env with absolute paths for the backend
  EnvFile := ExpandConstant('{app}\python-backend\.env');
  EnvContent := TStringList.Create;
  try
    EnvContent.Add('# Server Configuration');
    EnvContent.Add('FLASK_HOST=127.0.0.1');
    EnvContent.Add('FLASK_PORT=5000');
    EnvContent.Add('FLASK_DEBUG=False');
    EnvContent.Add('');
    EnvContent.Add('# Application Paths (absolute — writable location)');
    EnvContent.Add('CONTENT_DIR=' + ContentDir);
    EnvContent.Add('TEMP_DIR=' + TempDir);
    EnvContent.Add('OUTPUT_DIR=' + OutputDir);
    EnvContent.Add('QUIZ_DIR=' + QuizDir);
    EnvContent.Add('');
    EnvContent.Add('# Runtime Paths');
    EnvContent.Add('RUNTIME_DIR=' + ExpandConstant('{app}\runtime'));
    EnvContent.Add('RUNTIME_LOGS_DIR=' + LogsDir);
    EnvContent.Add('RUNTIME_CONFIG_DIR=' + ConfigDir);
    EnvContent.Add('POPPLER_PATH=' + ExpandConstant('{app}\runtime\poppler'));
    EnvContent.Add('LOG_FILE=' + LogsDir + '\backend.log');
    EnvContent.Add('');
    EnvContent.Add('# AI Configuration (Ollama — local LLM)');
    EnvContent.Add('OLLAMA_BASE_URL=http://localhost:11434');
    EnvContent.Add('OLLAMA_MODEL=llava');
    EnvContent.Add('OLLAMA_REQUEST_TIMEOUT=300');
    EnvContent.Add('DEFAULT_QUESTION_COUNT=10');
    EnvContent.Add('');
    EnvContent.Add('# Startup');
    EnvContent.Add('STARTUP_CHECK_STRICT=False');
    EnvContent.SaveToFile(EnvFile);
  finally
    EnvContent.Free;
  end;
end;

// Check if Ollama is already installed
function IsOllamaInstalled(): Boolean;
var
  ResultCode: Integer;
begin
  Result := Exec('cmd.exe', '/c where ollama', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
  if not Result then
  begin
    // Also check common locations
    Result := FileExists(ExpandConstant('{localappdata}\Programs\Ollama\ollama.exe'))
              or FileExists(ExpandConstant('{pf}\Ollama\ollama.exe'));
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create data directories and .env
    CreateDataDirectories();
  end;
end;

// Uninstall: ask user about quiz data
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  QuizDir: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    QuizDir := ExpandConstant('{localappdata}\Quiz Generator\quiz_out');
    if DirExists(QuizDir) then
    begin
      if MsgBox('Do you want to remove your saved quiz data?' + #13#10 +
                'This cannot be undone.', mbConfirmation, MB_YESNO) = IDYES then
      begin
        DelTree(ExpandConstant('{localappdata}\Quiz Generator'), True, True, True);
      end;
    end;
  end;
end;
