# Quiz Generator Desktop — Installation Guide

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10 (64-bit) | Windows 11 (64-bit) |
| **RAM** | 8 GB | 16 GB |
| **Disk Space** | 2 GB (app) + 5 GB (AI model) | 10 GB free |
| **CPU** | 4 cores | 8 cores |
| **GPU** | Not required | NVIDIA GPU recommended for faster AI |
| **Internet** | Required for first launch only | — |

> **Note**: The AI model download (first launch only) requires an internet connection and approximately 4–5 GB of disk space. After the initial setup, the application works completely offline.

## Installation Steps

### 1. Download the Installer

Download `QuizGeneratorSetup.exe` from the provided distribution link.

### 2. Run the Installer

1. Double-click `QuizGeneratorSetup.exe`
2. If Windows SmartScreen appears, click **"More info"** → **"Run anyway"**
3. Accept the MIT License agreement
4. Choose the installation directory (default: `C:\Program Files\Quiz Generator`)
5. Select shortcut options:
   - ✅ Create a Desktop shortcut
   - ✅ Create a Start Menu shortcut
6. Click **Install**
7. Wait for the installation to complete
8. Optionally check **"Launch Quiz Generator"** and click **Finish**

### 3. First Launch — Setup Wizard

The first time you launch Quiz Generator, a setup wizard appears automatically:

```
Welcome to Quiz Generator Desktop

Setting up your system...

  ✓  Python Runtime
  ✓  Java Runtime
  ✓  Poppler (PDF tools)
  ✓  Runtime Directories
  ◌  Ollama (Local AI)          ← Installing if needed
  ◌  AI Model (llava)           ← Downloading (~5 GB)
  ◌  Starting Backend
  ◌  Launching Application

  ████████████░░░░░  65%
  Downloading model llava...
```

**What happens during first launch:**

1. **System Check** — Verifies all bundled components (Python, Java, Poppler) are present
2. **Ollama Check** — If Ollama is not installed, it downloads and installs it automatically
3. **Model Download** — Downloads the AI model required for quiz generation (~5 GB, one-time)
4. **Backend Start** — Starts the Python backend server locally
5. **UI Launch** — Opens the Quiz Generator interface

> **Important**: The model download can take 5–15 minutes depending on your internet speed. Please be patient — this only happens once.

### 4. Subsequent Launches

After the first launch, opening Quiz Generator is instant:

1. Double-click the **Quiz Generator** icon on your Desktop
2. The backend starts automatically in the background
3. The Quiz Generator interface opens
4. When you close the interface, the backend shuts down automatically

No terminal windows, no manual commands, no configuration needed.

## How to Use

1. **Enter your name** on the login screen
2. **Drag and drop a PDF** onto the drop zone, or click to browse
3. Wait for the AI to process the PDF and generate quiz questions
4. Click **Rules** to see the quiz rules, then **Start** to begin
5. Answer the questions within the time limit
6. View your score at the end

## Runtime Components

Quiz Generator bundles the following components (you don't need to install them separately):

| Component | Purpose |
|-----------|---------|
| **Python 3.12** | Runs the backend AI pipeline |
| **Java Runtime (JRE 21)** | Runs the quiz interface |
| **Poppler** | Converts PDF pages to images for AI analysis |
| **Ollama** | Hosts the local AI model for question generation |
| **llava** | Vision-language AI model for understanding PDF content |

## Offline Mode

After the first launch (which requires internet for model download), Quiz Generator works **completely offline**:

- ✅ PDF processing — local
- ✅ AI inference — runs on your machine via Ollama
- ✅ Quiz generation — local
- ✅ No data sent to external servers
- ✅ No cloud dependencies

This makes it ideal for exam preparation in environments without internet access.

## File Locations

| What | Where |
|------|-------|
| Application files | `C:\Program Files\Quiz Generator\` |
| Your quiz data | `%LOCALAPPDATA%\Quiz Generator\quiz_out\` |
| Uploaded PDFs | `%LOCALAPPDATA%\Quiz Generator\content\` |
| Application logs | `%LOCALAPPDATA%\Quiz Generator\logs\` |
| Configuration | `C:\Program Files\Quiz Generator\python-backend\.env` |

## Troubleshooting

### "Backend Failed to Start"

**Cause**: Port 5000 may be in use by another application.

**Fix**:
1. Open Task Manager → find any process using port 5000 and end it
2. Or edit `C:\Program Files\Quiz Generator\python-backend\.env` and change `FLASK_PORT=5000` to another port (e.g., `5001`)
3. Restart Quiz Generator

### "Ollama Not Found"

**Cause**: Ollama installation failed or was removed.

**Fix**:
1. Download Ollama manually from https://ollama.com/download
2. Install it
3. Restart Quiz Generator

### "AI Model Not Found"

**Cause**: The model download was interrupted or failed.

**Fix**:
1. Open a terminal (Command Prompt or PowerShell)
2. Run: `ollama pull llava`
3. Wait for the download to complete
4. Restart Quiz Generator

### "Java Runtime Not Found"

**Cause**: The bundled JRE is corrupted or missing.

**Fix**: Reinstall Quiz Generator using the installer.

### Quiz generation takes too long

**Cause**: The AI model runs on CPU, which is slower than GPU.

**Tip**:
- If you have an NVIDIA GPU, ensure you have the latest NVIDIA drivers installed
- Ollama will automatically use your GPU if available
- Processing time depends on the number of PDF pages (typically 1–2 minutes per page)

### Application won't start after Windows update

**Fix**: Reinstall Quiz Generator. Your quiz data in `%LOCALAPPDATA%\Quiz Generator\quiz_out\` will be preserved.

## Uninstalling

1. Go to **Settings → Apps → Installed Apps**
2. Find **Quiz Generator** and click **Uninstall**
3. Follow the prompts
4. You will be asked whether to keep or delete your saved quiz data

> **Note**: Uninstalling Quiz Generator does NOT remove Ollama or downloaded AI models. To remove those, uninstall Ollama separately from Windows Settings.

## Getting Help

If you encounter issues not covered here, check the application log at:

```
%LOCALAPPDATA%\Quiz Generator\logs\startup.log
```

This file contains detailed information about what happened during startup.
