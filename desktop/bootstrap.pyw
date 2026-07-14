import os
import sys
import subprocess
import time
import json
import urllib.request
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import shutil

def get_root_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def ensure_app_directories(root_dir):
    required_dirs = [
        os.path.join(root_dir, 'logs'),
        os.path.join(root_dir, 'content'),
        os.path.join(root_dir, 'temp'),
        os.path.join(root_dir, 'output'),
        os.path.join(root_dir, 'quiz_out'),
        os.path.join(root_dir, 'runtime', 'models'),
        os.path.join(root_dir, 'runtime', 'logs'),
        os.path.join(root_dir, 'runtime', 'config'),
    ]
    for directory in required_dirs:
        os.makedirs(directory, exist_ok=True)

def check_ollama_installed():
    try:
        req = urllib.request.Request("http://localhost:11434/")
        with urllib.request.urlopen(req, timeout=1) as resp:
            if resp.status == 200:
                return True
    except:
        pass
    if shutil.which('ollama'): return True
    default_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")
    return os.path.exists(default_path)

def download_file(url, dest_path, progress_callback=None):
    try:
        response = urllib.request.urlopen(url)
        total_size_str = response.info().get('Content-Length')
        total_size = int(total_size_str.strip()) if total_size_str else 0
        downloaded = 0
        chunk_size = 8192
        start_time = time.time()
        
        with open(dest_path, 'wb') as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback and total_size > 0:
                    elapsed = time.time() - start_time
                    speed = downloaded / elapsed if elapsed > 0 else 0
                    eta_sec = (total_size - downloaded) / speed if speed > 0 else 0
                    progress_callback(downloaded, total_size, speed, eta_sec)
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

class BootstrapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Generator - First Time Setup")
        self.root.geometry("480x220")
        self.root.eval('tk::PlaceWindow . center')
        self.root.resizable(False, False)
        
        self.lbl_status = tk.Label(root, text="Preparing setup...", font=("Segoe UI", 11))
        self.lbl_status.pack(pady=(20, 10))
        
        self.progress = ttk.Progressbar(root, mode='indeterminate', length=380)
        self.progress.pack(pady=10)
        
        self.lbl_detail = tk.Label(root, text="", font=("Segoe UI", 9), fg="gray")
        self.lbl_detail.pack(pady=5)
        
        # Start work
        threading.Thread(target=self.run_setup, daemon=True).start()

    def update_status(self, text, detail="", mode='indeterminate', value=0, maximum=100):
        self.root.after(0, self._update_status_ui, text, detail, mode, value, maximum)

    def _update_status_ui(self, text, detail, mode, value, maximum):
        self.lbl_status.config(text=text)
        self.lbl_detail.config(text=detail)
        self.progress.config(mode=mode)
        if mode == 'determinate':
            self.progress['maximum'] = maximum
            self.progress['value'] = value
        else:
            self.progress.start(10)

    def format_speed_eta(self, speed_bytes, eta_sec):
        speed_mb = speed_bytes / (1024 * 1024)
        m, s = divmod(int(eta_sec), 60)
        eta_str = f"{m:02d}:{s:02d}"
        return f"{speed_mb:.1f} MB/s", eta_str

    def run_setup(self):
        try:
            root_dir = get_root_dir()
            ensure_app_directories(root_dir)
            
            # Step 1: Python Packages
            self.update_status("Checking Python dependencies...", "Installing missing packages")
            python_exe = os.path.join(root_dir, 'runtime', 'python', 'python.exe')
            req_file = os.path.join(root_dir, 'python-backend', 'requirements.txt')
            if os.path.exists(python_exe) and os.path.exists(req_file):
                subprocess.run(
                    [python_exe, "-m", "pip", "install", "-r", req_file],
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    check=False
                )
            
            # Step 2: Ollama Install
            if not check_ollama_installed():
                self.update_status("Downloading Ollama...", "Please wait while Ollama is downloaded")
                temp_dir = os.path.join(root_dir, 'temp')
                os.makedirs(temp_dir, exist_ok=True)
                installer_path = os.path.join(temp_dir, 'OllamaSetup.exe')
                
                def dl_progress(down, total, speed, eta_sec):
                    pct = int((down/total)*100) if total > 0 else 0
                    speed_str, eta_str = self.format_speed_eta(speed, eta_sec)
                    detail = f"{pct}% | Speed: {speed_str} | ETA: {eta_str}"
                    self.update_status("Downloading Ollama installer...", detail, mode='determinate', value=pct)
                    
                success = download_file("https://ollama.com/download/OllamaSetup.exe", installer_path, dl_progress)
                if not success:
                    raise Exception("Failed to download Ollama installer. Please check your internet connection.")
                
                self.update_status("Installing Ollama...", "Running silent installation (this may trigger a UAC prompt)", mode='indeterminate')
                subprocess.run([installer_path, "/SILENT"], check=True)
                
                # Wait for Ollama service
                self.update_status("Starting Ollama service...", "Waiting for localhost:11434")
                service_up = False
                for _ in range(60):
                    try:
                        req = urllib.request.Request("http://localhost:11434/")
                        with urllib.request.urlopen(req, timeout=1) as resp:
                            if resp.status == 200:
                                service_up = True
                                break
                    except:
                        # Try to launch it if it didn't start automatically
                        try:
                            ollama_exe = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")
                            if os.path.exists(ollama_exe):
                                subprocess.Popen([ollama_exe, "serve"], creationflags=subprocess.CREATE_NO_WINDOW)
                        except:
                            pass
                    time.sleep(1)
                    
                if not service_up:
                    raise Exception("Ollama installed but service did not start.")

            # Step 3: Check/Pull the vision model used for PDF image analysis
            model_name = "llava"
            self.update_status("Verifying AI Model...", f"Checking for '{model_name}'")
            
            # Query the API directly to avoid PATH issues
            has_model = False
            try:
                req = urllib.request.Request("http://localhost:11434/api/tags")
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    models = [m.get("name", "") for m in data.get("models", [])]
                    has_model = any(model_name in m for m in models)
            except Exception as e:
                # If tags fails, assume we don't have it and try to pull anyway
                print(f"Failed to fetch tags: {e}")
                
            if not has_model:
                self.update_status(f"Preparing to download '{model_name}'...", "Connecting to Ollama service...")
                
                req = urllib.request.Request(
                    "http://localhost:11434/api/pull", 
                    data=json.dumps({"name": model_name}).encode('utf-8'), 
                    headers={'Content-Type': 'application/json'}
                )
                start_time = time.time()
                with urllib.request.urlopen(req) as resp:
                    for line in resp:
                        if line:
                            data = json.loads(line)
                            status_msg = data.get("status", "")
                            completed = data.get("completed", 0)
                            total = data.get("total", 0)
                            
                            if total > 0:
                                elapsed = time.time() - start_time
                                speed = completed / elapsed if elapsed > 0 else 0
                                eta_sec = (total - completed) / speed if speed > 0 else 0
                                
                                speed_str, eta_str = self.format_speed_eta(speed, eta_sec)
                                pct = int((completed/total)*100)
                                detail = f"{pct}% | Speed: {speed_str} | ETA: {eta_str} | {status_msg}"
                                self.update_status(f"Pulling Model '{model_name}'", detail, mode='determinate', value=pct)
                            else:
                                self.update_status(f"Pulling Model '{model_name}'", status_msg, mode='indeterminate')
                
            # Step 4: Validate Poppler
            self.update_status("Verifying dependencies...", "Checking Poppler")
            poppler_dir = os.path.join(root_dir, 'runtime', 'poppler')
            if not os.path.exists(poppler_dir):
                print("Warning: Poppler missing.")
                
            # Step 5: Configuration
            env_path = os.path.join(root_dir, 'python-backend', '.env')
            if not os.path.exists(env_path):
                # Ensure a minimal env exists
                with open(env_path, 'w', encoding='utf-8') as f:
                    f.write(f'OLLAMA_MODEL={model_name}\n')
            else:
                with open(env_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'OLLAMA_MODEL=' in content:
                    import re
                    content = re.sub(r'OLLAMA_MODEL=.*', f'OLLAMA_MODEL={model_name}', content)
                else:
                    content += f'\nOLLAMA_MODEL={model_name}\n'
                with open(env_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            # Step 6: Write setup completion state
            state_file = os.path.join(root_dir, 'setup.state')
            with open(state_file, 'w', encoding='utf-8') as f:
                f.write('setup_complete=true\n')

            # Done
            self.update_status("Setup Complete!", "Starting application...", mode='determinate', value=100)
            time.sleep(1)
            
            # Note: Launcher invoked us and is waiting. We just exit successfully.
            self.root.after(0, self.root.destroy)
            
        except Exception as e:
            def show_error():
                messagebox.showerror("Setup Error", f"An error occurred during setup:\n{str(e)}")
                self.root.destroy()
            self.root.after(0, show_error)
            sys.exit(1)

def main():
    root = tk.Tk()
    app = BootstrapApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
