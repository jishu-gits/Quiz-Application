# Quiz Generator — Installer Testing Checklist

Use this checklist to verify the installer and first-run experience on a **clean Windows environment** (e.g., a fresh Windows 10/11 VM).

## Pre-requisites (Clean Environment Setup)
- [ ] Ensure **no** Java is installed (`java -version` fails).
- [ ] Ensure **no** Python is installed (`python --version` fails).
- [ ] Ensure **no** Poppler/pdfinfo is installed.
- [ ] Ensure **no** Ollama is installed.
- [ ] Ensure the VM has an active internet connection (required for downloading Ollama and pulling the model).
- [ ] Copy the built `QuizGeneratorSetup.exe` to the VM.

## 1. Installation Phase
- [ ] **Run Installer**: Double-click `QuizGeneratorSetup.exe`.
- [ ] **SmartScreen**: If prompted, verify you can bypass it ("More info" -> "Run anyway").
- [ ] **License**: Verify the MIT License displays correctly.
- [ ] **Directory**: Accept the default `C:\Program Files\Quiz Generator`.
- [ ] **Shortcuts**: Check both Desktop and Start Menu shortcut creation options.
- [ ] **Completion**: Verify the installation finishes without requiring any command-line intervention.

## 2. First-Run Setup Wizard
- [ ] **Launch**: Double-click the newly created Desktop shortcut for Quiz Generator.
- [ ] **Wizard UI**: Verify the "Quiz Generator — First Run Setup" window appears.
- [ ] **System Checks**:
    - [ ] Python Runtime: Verified ✅
    - [ ] Java Runtime: Verified ✅
    - [ ] Poppler: Verified ✅
    - [ ] Runtime Directories: Verified ✅
- [ ] **Ollama Installation**:
    - [ ] Status should change to "Installing Ollama...".
    - [ ] Verify Ollama installs silently without popping up its own setup UI.
    - [ ] Ollama (Local AI): Verified ✅
- [ ] **Model Download**:
    - [ ] Status should change to "Downloading model llava...".
    - [ ] Verify the progress bar updates incrementally.
    - [ ] AI Model (llava): Verified ✅
- [ ] **Background Initialization**:
    - [ ] Starting Backend: Verified ✅
    - [ ] Launching Application: Verified ✅
- [ ] **Completion**: Verify the Wizard closes automatically once the Java UI appears.

## 3. Application Functionality (End-to-End)
- [ ] **UI Visibility**: The Java Login screen appears successfully.
- [ ] **No Consoles**: Verify there are **no** stray command-prompt windows visible in the taskbar or screen.
- [ ] **Upload**: Drag and drop a valid PDF file onto the drop zone.
- [ ] **Processing**: Wait for processing to finish. Verify the success message appears.
- [ ] **Quiz Generation**: Proceed through the rules screen to the Quiz screen.
- [ ] **Gameplay**: Verify the generated questions load properly, options are selectable, and the final score is calculated.

## 4. Normal Launch
- [ ] **Close App**: Close the Java UI.
- [ ] **Wait**: Wait ~5 seconds to ensure the background Flask server shuts down. (Verify in Task Manager that `pythonw.exe` running `app.py` is gone).
- [ ] **Relaunch**: Double-click the Desktop shortcut again.
- [ ] **Speed**: Verify the UI appears quickly without going through the model download wizard again.

## 5. Uninstallation
- [ ] **Initiate**: Go to Windows Settings -> Apps -> Installed Apps -> Quiz Generator -> Uninstall.
- [ ] **Prompt**: When asked whether to remove saved quiz data, select **No**.
- [ ] **App Files**: Verify `C:\Program Files\Quiz Generator` is completely removed.
- [ ] **Shortcuts**: Verify Desktop and Start Menu shortcuts are removed.
- [ ] **Data Persistence**: Navigate to `%LOCALAPPDATA%\Quiz Generator\quiz_out` and verify your generated JSON files are still there.
- [ ] **Ollama Retention**: Verify Ollama is still installed on the system (as it's a global dependency).
