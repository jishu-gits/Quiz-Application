"""
Quiz Generator Desktop — Startup Manager
=========================================
Single entry point for the application. Handles:
  - First-run setup wizard (Ollama detection, model pull)
  - Normal launch (start backend, wait for health, launch Java UI)
  - Error reporting via friendly GUI dialogs

Launched via launch.vbs → pythonw.exe startup_manager.pyw
No console window is ever shown to the user.
"""

import os
import sys
import time
import json
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

# ---------------------------------------------------------------------------
# Paths — resolved relative to the install directory
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent              # <install>/scripts/
INSTALL_DIR = SCRIPT_DIR.parent                           # <install>/
PYTHON_BACKEND = INSTALL_DIR / "python-backend"
JAVA_CLIENT = INSTALL_DIR / "java-client"
RUNTIME_DIR = INSTALL_DIR / "runtime"
PYTHON_DIR = RUNTIME_DIR / "python"
JRE_DIR = RUNTIME_DIR / "jre"
POPPLER_DIR = RUNTIME_DIR / "poppler"
LOGS_DIR = RUNTIME_DIR / "logs"

DATA_DIR = Path(os.environ.get("LOCALAPPDATA", INSTALL_DIR)) / "Quiz Generator"
MARKER_FILE = DATA_DIR / ".setup_complete"

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 5000
HEALTH_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/health"

# Ollama model to pull — read from .env or default
DEFAULT_OLLAMA_MODEL = "llava"

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _read_env_model():
    """Read the OLLAMA_MODEL value from the backend .env file."""
    env_file = PYTHON_BACKEND / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("OLLAMA_MODEL="):
                return line.split("=", 1)[1].strip()
    return DEFAULT_OLLAMA_MODEL


def _find_executable(name, extra_dirs=None):
    """Find an executable on PATH or in extra_dirs."""
    path = shutil.which(name)
    if path:
        return path
    for d in (extra_dirs or []):
        candidate = Path(d) / name
        if candidate.exists():
            return str(candidate)
        if os.name == "nt":
            candidate_exe = Path(d) / f"{name}.exe"
            if candidate_exe.exists():
                return str(candidate_exe)
    return None


def _get_python_exe():
    """Return the embedded Python executable path."""
    for name in ("pythonw.exe", "python.exe"):
        p = PYTHON_DIR / name
        if p.exists():
            return str(p)
    # Fallback to system python
    return shutil.which("pythonw") or shutil.which("python") or sys.executable


def _get_java_exe():
    """Return javaw.exe (GUI, no console) from bundled JRE or system."""
    jre_bin = JRE_DIR / "bin"
    for name in ("javaw.exe", "javaw", "java.exe", "java"):
        p = jre_bin / name
        if p.exists():
            return str(p)
    return _find_executable("javaw") or _find_executable("java")


def _get_ollama_exe():
    """Find the ollama executable."""
    return _find_executable("ollama")


def _health_check():
    """Return True if backend health endpoint responds."""
    try:
        req = Request(HEALTH_URL, method="GET")
        resp = urlopen(req, timeout=3)
        return resp.status == 200
    except Exception:
        return False


def _wait_for_backend(timeout=60):
    """Block until backend health check passes or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _health_check():
            return True
        time.sleep(1)
    return False


def _log(msg):
    """Append a log line to the runtime log file."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / "startup.log"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {msg}\n")


# ---------------------------------------------------------------------------
# Startup checks
# ---------------------------------------------------------------------------

def check_python():
    exe = _get_python_exe()
    return exe is not None, exe or "Not found"


def check_java():
    exe = _get_java_exe()
    return exe is not None, exe or "Not found"


def check_poppler():
    poppler_bin = POPPLER_DIR / "Library" / "bin"
    if not poppler_bin.exists():
        poppler_bin = POPPLER_DIR / "bin"
    if not poppler_bin.exists():
        poppler_bin = POPPLER_DIR
    pdfinfo = poppler_bin / ("pdfinfo.exe" if os.name == "nt" else "pdfinfo")
    if pdfinfo.exists():
        return True, str(poppler_bin)
    # Check system PATH
    sys_pdfinfo = shutil.which("pdfinfo")
    if sys_pdfinfo:
        return True, str(Path(sys_pdfinfo).parent)
    return False, "Not found"


def check_ollama():
    exe = _get_ollama_exe()
    return exe is not None, exe or "Not found"


def check_model(model_name):
    """Check if the specified Ollama model is available."""
    try:
        req = Request("http://localhost:11434/api/tags", method="GET")
        resp = urlopen(req, timeout=10)
        data = json.loads(resp.read().decode("utf-8"))
        names = []
        for m in data.get("models", []):
            name = m.get("name") or m.get("model") or ""
            names.append(name)
        if model_name in names:
            return True
        if ":" not in model_name and f"{model_name}:latest" in names:
            return True
        return False
    except Exception:
        return False


# ---------------------------------------------------------------------------
# GUI — First Run Wizard
# ---------------------------------------------------------------------------

class FirstRunWizard(tk.Tk):
    """Tkinter wizard shown on first launch to verify and install dependencies."""

    def __init__(self):
        super().__init__()
        self.title("Quiz Generator — First Run Setup")
        self.geometry("520x460")
        self.resizable(False, False)
        self.configure(bg="#1a1a2e")

        # Try to set icon
        icon_path = INSTALL_DIR / "installer" / "assets" / "app.ico"
        if not icon_path.exists():
            icon_path = INSTALL_DIR / "app.ico"
        if icon_path.exists():
            try:
                self.iconbitmap(str(icon_path))
            except Exception:
                pass

        self.completed = False
        self.ollama_model = _read_env_model()

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Start checks in a background thread
        self.after(500, self._start_checks)

    def _build_ui(self):
        # Title
        title = tk.Label(
            self, text="Welcome to Quiz Generator Desktop",
            font=("Segoe UI", 16, "bold"), fg="#e0e0e0", bg="#1a1a2e"
        )
        title.pack(pady=(25, 5))

        subtitle = tk.Label(
            self, text="Setting up your system...",
            font=("Segoe UI", 10), fg="#888888", bg="#1a1a2e"
        )
        subtitle.pack(pady=(0, 20))

        # Check items frame
        self.checks_frame = tk.Frame(self, bg="#1a1a2e")
        self.checks_frame.pack(fill="x", padx=40)

        self.check_labels = {}
        items = [
            ("python", "Python Runtime"),
            ("java", "Java Runtime"),
            ("poppler", "Poppler (PDF tools)"),
            ("runtime", "Runtime Directories"),
            ("ollama", "Ollama (Local AI)"),
            ("model", f"AI Model ({self.ollama_model})"),
            ("backend", "Starting Backend"),
            ("launch", "Launching Application"),
        ]
        for key, text in items:
            row = tk.Frame(self.checks_frame, bg="#1a1a2e")
            row.pack(fill="x", pady=3)

            status_lbl = tk.Label(
                row, text="○", font=("Segoe UI", 12), fg="#555555",
                bg="#1a1a2e", width=3
            )
            status_lbl.pack(side="left")

            text_lbl = tk.Label(
                row, text=text, font=("Segoe UI", 11), fg="#cccccc",
                bg="#1a1a2e", anchor="w"
            )
            text_lbl.pack(side="left", fill="x", expand=True)

            self.check_labels[key] = (status_lbl, text_lbl)

        # Progress bar (for model pull)
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            self, variable=self.progress_var, maximum=100, length=440
        )
        self.progress_bar.pack(pady=(20, 5))

        self.status_label = tk.Label(
            self, text="Initializing...",
            font=("Segoe UI", 9), fg="#888888", bg="#1a1a2e"
        )
        self.status_label.pack()

        # Bottom button (hidden initially)
        self.close_btn = tk.Button(
            self, text="Close", font=("Segoe UI", 10),
            bg="#e74c3c", fg="white", relief="flat", padx=20, pady=5,
            command=self._on_close
        )

    def _set_check(self, key, status):
        """status: 'ok', 'fail', 'working', 'skip'"""
        icons = {"ok": "✓", "fail": "✗", "working": "◌", "skip": "–"}
        colors = {"ok": "#2ecc71", "fail": "#e74c3c", "working": "#f39c12", "skip": "#888888"}
        lbl, _ = self.check_labels[key]
        lbl.config(text=icons.get(status, "○"), fg=colors.get(status, "#555555"))

    def _set_status(self, text):
        self.status_label.config(text=text)

    def _start_checks(self):
        thread = threading.Thread(target=self._run_checks, daemon=True)
        thread.start()

    def _run_checks(self):
        all_ok = True

        # 1. Python
        self.after(0, lambda: self._set_check("python", "working"))
        self.after(0, lambda: self._set_status("Checking Python..."))
        ok, detail = check_python()
        self.after(0, lambda: self._set_check("python", "ok" if ok else "fail"))
        _log(f"Python: {'OK' if ok else 'FAIL'} — {detail}")
        if not ok:
            all_ok = False
        time.sleep(0.3)

        # 2. Java
        self.after(0, lambda: self._set_check("java", "working"))
        self.after(0, lambda: self._set_status("Checking Java..."))
        ok, detail = check_java()
        self.after(0, lambda: self._set_check("java", "ok" if ok else "fail"))
        _log(f"Java: {'OK' if ok else 'FAIL'} — {detail}")
        if not ok:
            all_ok = False
        time.sleep(0.3)

        # 3. Poppler
        self.after(0, lambda: self._set_check("poppler", "working"))
        self.after(0, lambda: self._set_status("Checking Poppler..."))
        ok, detail = check_poppler()
        self.after(0, lambda: self._set_check("poppler", "ok" if ok else "fail"))
        _log(f"Poppler: {'OK' if ok else 'FAIL'} — {detail}")
        if not ok:
            all_ok = False
        time.sleep(0.3)

        # 4. Runtime dirs
        self.after(0, lambda: self._set_check("runtime", "working"))
        self.after(0, lambda: self._set_status("Checking runtime directories..."))
        dirs_ok = True
        for d in [RUNTIME_DIR, LOGS_DIR, DATA_DIR]:
            d.mkdir(parents=True, exist_ok=True)
            if not d.is_dir():
                dirs_ok = False
        self.after(0, lambda: self._set_check("runtime", "ok" if dirs_ok else "fail"))
        _log(f"Runtime dirs: {'OK' if dirs_ok else 'FAIL'}")
        time.sleep(0.3)

        # 5. Ollama
        self.after(0, lambda: self._set_check("ollama", "working"))
        self.after(0, lambda: self._set_status("Checking Ollama..."))
        ollama_ok, ollama_detail = check_ollama()

        if not ollama_ok:
            self.after(0, lambda: self._set_status("Installing Ollama..."))
            _log("Ollama not found — attempting installation")
            ollama_ok = self._install_ollama()

        self.after(0, lambda: self._set_check("ollama", "ok" if ollama_ok else "fail"))
        _log(f"Ollama: {'OK' if ollama_ok else 'FAIL'}")
        if not ollama_ok:
            all_ok = False
        time.sleep(0.3)

        # 6. Model
        self.after(0, lambda: self._set_check("model", "working"))
        self.after(0, lambda: self._set_status(f"Checking model {self.ollama_model}..."))

        # Make sure Ollama server is running before checking model
        if ollama_ok:
            self._ensure_ollama_running()
            time.sleep(2)

            model_available = check_model(self.ollama_model)
            if not model_available:
                self.after(0, lambda: self._set_status(f"Downloading model {self.ollama_model}..."))
                _log(f"Model {self.ollama_model} not found — pulling")
                model_available = self._pull_model()
            self.after(0, lambda: self._set_check("model", "ok" if model_available else "fail"))
            _log(f"Model {self.ollama_model}: {'OK' if model_available else 'FAIL'}")
            if not model_available:
                all_ok = False
        else:
            self.after(0, lambda: self._set_check("model", "skip"))
            _log("Skipping model check — Ollama not available")
        time.sleep(0.3)

        if not all_ok:
            self.after(0, lambda: self._set_status("Setup completed with issues. See log for details."))
            self.after(0, lambda: self.close_btn.pack(pady=(15, 0)))
            _log("First-run setup completed with errors")
            return

        # 7. Start backend
        self.after(0, lambda: self._set_check("backend", "working"))
        self.after(0, lambda: self._set_status("Starting backend server..."))
        backend_proc = self._start_backend()
        backend_ready = _wait_for_backend(timeout=30)
        self.after(0, lambda: self._set_check("backend", "ok" if backend_ready else "fail"))
        _log(f"Backend: {'OK' if backend_ready else 'FAIL'}")
        if not backend_ready:
            self.after(0, lambda: self._set_status("Backend failed to start. Check logs."))
            self.after(0, lambda: self.close_btn.pack(pady=(15, 0)))
            return
        time.sleep(0.3)

        # 8. Launch Java UI
        self.after(0, lambda: self._set_check("launch", "working"))
        self.after(0, lambda: self._set_status("Launching Quiz Generator..."))
        java_proc = self._launch_java()
        if java_proc:
            self.after(0, lambda: self._set_check("launch", "ok"))
            self.after(0, lambda: self._set_status("Done! Quiz Generator is running."))
            _log("Java UI launched successfully")

            # Mark setup complete
            MARKER_FILE.parent.mkdir(parents=True, exist_ok=True)
            MARKER_FILE.write_text("setup_complete", encoding="utf-8")
            _log("First-run setup marked complete")

            # Wait a moment then close wizard, monitor Java
            time.sleep(2)
            self.after(0, self.destroy)
            self._monitor_processes(backend_proc, java_proc)
        else:
            self.after(0, lambda: self._set_check("launch", "fail"))
            self.after(0, lambda: self._set_status("Failed to launch Java UI."))
            self.after(0, lambda: self.close_btn.pack(pady=(15, 0)))

    def _install_ollama(self):
        """Run the Ollama installation PowerShell script."""
        script = SCRIPT_DIR / "install_ollama.ps1"
        if not script.exists():
            _log(f"install_ollama.ps1 not found at {script}")
            return False
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script)],
                capture_output=True, text=True, timeout=300,
                startupinfo=startupinfo
            )
            _log(f"Ollama install stdout: {result.stdout}")
            _log(f"Ollama install stderr: {result.stderr}")
            # Re-check
            return check_ollama()[0]
        except Exception as e:
            _log(f"Ollama install failed: {e}")
            return False

    def _ensure_ollama_running(self):
        """Start the Ollama server if it's not already running."""
        try:
            req = Request("http://localhost:11434/api/tags", method="GET")
            urlopen(req, timeout=3)
            return  # Already running
        except Exception:
            pass
        # Start ollama serve in background
        ollama_exe = _get_ollama_exe()
        if ollama_exe:
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                subprocess.Popen(
                    [ollama_exe, "serve"],
                    startupinfo=startupinfo,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                _log("Started ollama serve")
                time.sleep(3)
            except Exception as e:
                _log(f"Failed to start ollama serve: {e}")

    def _pull_model(self):
        """Pull the Ollama model, updating the progress bar."""
        ollama_exe = _get_ollama_exe()
        if not ollama_exe:
            return False
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
            proc = subprocess.Popen(
                [ollama_exe, "pull", self.ollama_model],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                startupinfo=startupinfo, text=True
            )
            self.after(0, lambda: self.progress_var.set(0))
            progress = 0
            for line in proc.stdout:
                line = line.strip()
                _log(f"ollama pull: {line}")
                # Parse progress from ollama output (e.g. "pulling ... 45%")
                if "%" in line:
                    try:
                        pct_str = line.split("%")[0].strip().split()[-1]
                        pct = float(pct_str)
                        progress = pct
                        self.after(0, lambda p=pct: self.progress_var.set(p))
                        self.after(0, lambda p=pct: self._set_status(
                            f"Downloading model {self.ollama_model}... {p:.0f}%"
                        ))
                    except (ValueError, IndexError):
                        pass
                elif "success" in line.lower():
                    progress = 100
                    self.after(0, lambda: self.progress_var.set(100))

            proc.wait(timeout=600)
            self.after(0, lambda: self.progress_var.set(100))
            return proc.returncode == 0 or check_model(self.ollama_model)
        except Exception as e:
            _log(f"Model pull failed: {e}")
            return False

    def _start_backend(self):
        """Start the Flask backend in the background."""
        return _start_backend_process()

    def _launch_java(self):
        """Launch the Java Swing UI."""
        return _launch_java_process()

    def _monitor_processes(self, backend_proc, java_proc):
        """Wait for Java to exit, then kill backend."""
        try:
            java_proc.wait()
        except Exception:
            pass
        _log("Java UI closed — shutting down backend")
        try:
            backend_proc.terminate()
            backend_proc.wait(timeout=5)
        except Exception:
            try:
                backend_proc.kill()
            except Exception:
                pass

    def _on_close(self):
        self.completed = False
        self.destroy()


# ---------------------------------------------------------------------------
# Normal (non-first-run) launch
# ---------------------------------------------------------------------------

def normal_launch():
    """Quick-launch path for subsequent runs after first-run completes."""
    _log("Normal launch started")

    # Quick dependency check
    java_exe = _get_java_exe()
    if not java_exe:
        _show_error(
            "Java Runtime Not Found",
            "The Java Runtime was not found.\n\n"
            "Please reinstall Quiz Generator or install Java manually."
        )
        return

    python_exe = _get_python_exe()
    if not python_exe:
        _show_error(
            "Python Runtime Not Found",
            "The embedded Python runtime was not found.\n\n"
            "Please reinstall Quiz Generator."
        )
        return

    # Ensure Ollama is running
    ollama_exe = _get_ollama_exe()
    if ollama_exe:
        try:
            req = Request("http://localhost:11434/api/tags", method="GET")
            urlopen(req, timeout=3)
        except Exception:
            # Start ollama serve
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                subprocess.Popen(
                    [ollama_exe, "serve"],
                    startupinfo=startupinfo,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                _log("Started ollama serve")
                time.sleep(3)
            except Exception as e:
                _log(f"Failed to start ollama serve: {e}")

    # Start backend
    _log("Starting backend...")
    backend_proc = _start_backend_process()
    if not _wait_for_backend(timeout=30):
        _show_error(
            "Backend Failed to Start",
            "The Quiz Generator backend did not start properly.\n\n"
            "Check the log file at:\n"
            f"{LOGS_DIR / 'startup.log'}"
        )
        try:
            backend_proc.terminate()
        except Exception:
            pass
        return

    _log("Backend is ready")

    # Launch Java
    java_proc = _launch_java_process()
    if not java_proc:
        _show_error(
            "Application Launch Failed",
            "Failed to launch the Quiz Generator interface.\n\n"
            "Check the log file at:\n"
            f"{LOGS_DIR / 'startup.log'}"
        )
        try:
            backend_proc.terminate()
        except Exception:
            pass
        return

    _log("Java UI launched — monitoring")

    # Wait for Java to close, then kill backend
    try:
        java_proc.wait()
    except Exception:
        pass
    _log("Java UI closed — shutting down backend")
    try:
        backend_proc.terminate()
        backend_proc.wait(timeout=5)
    except Exception:
        try:
            backend_proc.kill()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Process launchers
# ---------------------------------------------------------------------------

def _start_backend_process():
    """Start the Flask backend as a background process."""
    python_exe = _get_python_exe()
    app_py = PYTHON_BACKEND / "app.py"
    env = os.environ.copy()
    # Add poppler to PATH so pdf2image can find it
    poppler_ok, poppler_path = check_poppler()
    if poppler_ok:
        env["PATH"] = poppler_path + os.pathsep + env.get("PATH", "")

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0

    proc = subprocess.Popen(
        [python_exe, str(app_py)],
        cwd=str(PYTHON_BACKEND),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        startupinfo=startupinfo,
    )
    _log(f"Backend started with PID {proc.pid}")
    return proc


def _launch_java_process():
    """Launch the Java Swing UI."""
    java_exe = _get_java_exe()
    if not java_exe:
        return None

    # Build classpath: java-client/bin + jackson JARs
    bin_dir = JAVA_CLIENT / "bin"
    lib_dir = JAVA_CLIENT / "lib"

    classpath_parts = [str(bin_dir)]
    if lib_dir.exists():
        for jar in lib_dir.glob("*.jar"):
            classpath_parts.append(str(jar))

    classpath = os.pathsep.join(classpath_parts)

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0

    try:
        proc = subprocess.Popen(
            [java_exe, "-cp", classpath, "Login"],
            cwd=str(JAVA_CLIENT),
            startupinfo=startupinfo,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _log(f"Java UI started with PID {proc.pid}")
        return proc
    except Exception as e:
        _log(f"Failed to launch Java: {e}")
        return None


def _show_error(title, message):
    """Show a GUI error dialog."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    _log("=" * 60)
    _log("Quiz Generator startup")

    if MARKER_FILE.exists():
        # Normal launch — no wizard
        normal_launch()
    else:
        # First run — show wizard
        _log("First run detected — showing setup wizard")
        wizard = FirstRunWizard()
        wizard.mainloop()


if __name__ == "__main__":
    main()
