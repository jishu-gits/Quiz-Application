# Quiz Generator — Installer Build Guide

This document describes how to build `QuizGeneratorSetup.exe` from the Inno Setup project.

## Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| **Inno Setup** | 6.x | https://jrsoftware.org/isdl.php |
| **Java JDK** | 21+ | Required only for compiling `.java` → `.class` |

## Step 1: Download Runtime Binaries

The following runtime components must be placed in `desktop/runtime/` before building. They are not checked into version control because they are large binary distributions.

### Python 3.12 Embedded (Windows x64)

```
Download: https://www.python.org/ftp/python/3.12.4/python-3.12.4-embed-amd64.zip
Extract to: desktop/runtime/python/
```

After extracting, install pip and required packages:

```powershell
cd desktop\runtime\python

# Enable site-packages: edit python312._pth and uncomment "import site"
(Get-Content python312._pth) -replace '#import site','import site' | Set-Content python312._pth

# Install pip
Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
.\python.exe get-pip.py

# Install backend dependencies
.\python.exe -m pip install -r ..\..\python-backend\requirements.txt

# Verify
.\python.exe -c "import flask; print('Flask', flask.__version__)"
```

### Poppler for Windows

```
Download: https://github.com/oschwartz10612/poppler-windows/releases/latest
Extract to: desktop/runtime/poppler/
```

Ensure `desktop/runtime/poppler/Library/bin/pdfinfo.exe` exists (or `poppler/bin/pdfinfo.exe` depending on the release structure).

### Java Runtime Environment (JRE 21)

```
Download: https://adoptium.net/temurin/releases/?os=windows&arch=x64&package=jre&version=21
Extract to: desktop/runtime/jre/
```

Ensure `desktop/runtime/jre/bin/javaw.exe` exists.

### Jackson JSON Library (for Java client)

```
Download the following JARs from Maven Central:
  - jackson-core-2.17.2.jar
  - jackson-databind-2.17.2.jar
  - jackson-annotations-2.17.2.jar

Place in: desktop/java-client/lib/
```

Download URLs:
- https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-core/2.17.2/jackson-core-2.17.2.jar
- https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.17.2/jackson-databind-2.17.2.jar
- https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.17.2/jackson-annotations-2.17.2.jar

## Step 2: Compile Java Source

Compile the Java source files with the Jackson JARs on the classpath:

```powershell
cd desktop\java-client

# Create bin/ and lib/ directories
New-Item -ItemType Directory -Force -Path bin, lib

# Compile (adjust classpath separator ; for Windows)
javac -cp "lib\*" -d bin src\Login.java src\Quiz.java src\Rules.java src\Score.java
```

Verify `desktop/java-client/bin/Login.class` exists.

## Step 3: Verify Directory Structure

Before building, the tree should look like:

```
desktop/
├── installer/
│   ├── QuizGenerator.iss          ← Inno Setup script
│   ├── assets/
│   │   ├── app.ico
│   │   └── license.rtf
│   └── scripts/
│       ├── startup_manager.pyw
│       ├── launch.vbs
│       └── install_ollama.ps1
├── java-client/
│   ├── src/                       ← Java source
│   ├── bin/                       ← Compiled .class files
│   ├── lib/                       ← Jackson JARs
│   └── *.jpg                      ← UI images
├── python-backend/
│   ├── app.py, config.py, etc.
│   └── .env
└── runtime/
    ├── python/                    ← Embedded Python + packages
    ├── poppler/                   ← Poppler binaries
    └── jre/                       ← JRE 21
```

## Step 4: Build the Installer

### Option A: Inno Setup GUI

1. Open `desktop/installer/QuizGenerator.iss` in Inno Setup
2. Click **Build → Compile**
3. Output: `desktop/installer/output/QuizGeneratorSetup.exe`

### Option B: Command Line

```powershell
# Assumes iscc.exe is in PATH (Inno Setup installs it)
cd desktop\installer
iscc QuizGenerator.iss
```

Output: `desktop/installer/output/QuizGeneratorSetup.exe`

## Output

The built installer will be at:

```
desktop/installer/output/QuizGeneratorSetup.exe
```

This single file can be distributed to end users. It contains everything needed except:
- **Ollama** — downloaded and installed automatically on first run if not already present
- **AI Model** — pulled automatically on first run via `ollama pull`

## Installer Behavior

1. Shows license agreement (MIT)
2. Lets user choose install directory (default: `C:\Program Files\Quiz Generator`)
3. Creates Desktop and Start Menu shortcuts
4. Generates `.env` with absolute paths to writable data directory (`%LOCALAPPDATA%\Quiz Generator`)
5. Optionally launches the app after install
6. First launch triggers the setup wizard (Ollama + model check)

## Uninstall Behavior

- Removes all application files from `C:\Program Files\Quiz Generator`
- Asks user whether to delete saved quiz data from `%LOCALAPPDATA%\Quiz Generator`
- Does NOT remove Ollama (system-wide dependency)
