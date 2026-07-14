import os
import sys
import subprocess
import time
import urllib.request
import tkinter as tk
from tkinter import messagebox

def get_root_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_log_file():
    log_dir = os.path.join(get_root_dir(), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, 'startup.log')

def log(message):
    try:
        with open(get_log_file(), 'a', encoding='utf-8') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    except Exception:
        pass

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

def verify_java_client(root_dir, java_exe):
    java_dir = os.path.join(root_dir, 'java-client')
    lib_dir = os.path.join(java_dir, 'lib')
    required_paths = [
        (java_exe, 'runtime\\jre\\bin\\javaw.exe'),
        (os.path.join(java_dir, 'bin', 'Login.class'), 'java-client\\bin\\Login.class'),
        (os.path.join(java_dir, 'bin', 'Quiz.class'), 'java-client\\bin\\Quiz.class'),
    ]
    missing = [label for path, label in required_paths if not os.path.exists(path)]

    has_jars = os.path.isdir(lib_dir) and any(
        filename.lower().endswith('.jar') for filename in os.listdir(lib_dir)
    )
    if not has_jars:
        missing.append('java-client\\lib\\*.jar')

    if missing:
        show_error_and_exit(
            "Installation Error",
            "The Java client is incomplete. Missing: "
            + ", ".join(missing)
            + ". Please reinstall Quiz Generator with the latest installer."
        )

def poll_backend():
    max_retries = 30
    for i in range(max_retries):
        try:
            req = urllib.request.Request("http://localhost:5000/health")
            with urllib.request.urlopen(req, timeout=1) as response:
                if response.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(1)
    return False

def show_error_and_exit(title, message):
    log(f"ERROR: {title} - {message}")
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    sys.exit(1)

def is_setup_complete():
    state_file = os.path.join(get_root_dir(), 'setup.state')
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "setup_complete=true" in content:
                    return True
        except Exception as e:
            log(f"Error reading setup.state: {e}")
    return False

def run_bootstrap():
    log("Setup is incomplete. Launching bootstrap...")
    root_dir = get_root_dir()
    bootstrap_exe = os.path.join(root_dir, 'QuizGeneratorBootstrap.exe')
    
    try:
        bootstrap_process = subprocess.Popen(
            [bootstrap_exe],
            cwd=root_dir,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        bootstrap_process.wait()
    except Exception as e:
        show_error_and_exit("Bootstrap Error", f"Could not launch the bootstrap process: {e}")

def main():
    log("=== Launcher Started ===")
    
    root_dir = get_root_dir()
    os.chdir(root_dir)
    ensure_app_directories(root_dir)
    
    # 1. Check state
    if not is_setup_complete():
        run_bootstrap()
        # Re-check state after bootstrap exits
        if not is_setup_complete():
            show_error_and_exit("Setup Incomplete", "First-time setup failed or was canceled. The application cannot start.")
    
    log("Setup verified. Proceeding with launch...")
    
    java_dir = os.path.join(root_dir, 'java-client')
    backend_dir = os.path.join(root_dir, 'python-backend')
    runtime_jre = os.path.join(root_dir, 'runtime', 'jre')
    runtime_python = os.path.join(root_dir, 'runtime', 'python')
    java_exe = os.path.join(runtime_jre, 'bin', 'javaw.exe')
    verify_java_client(root_dir, java_exe)
    
    # 2. Start Flask backend
    log("Starting Flask backend...")
    python_exe = os.path.join(runtime_python, 'python.exe')
    app_py = os.path.join(backend_dir, 'app.py')
    
    env = os.environ.copy()
    env['CONTENT_DIR'] = os.path.join(root_dir, 'content')
    env['TEMP_DIR'] = os.path.join(root_dir, 'temp')
    env['OUTPUT_DIR'] = os.path.join(root_dir, 'output')
    env['QUIZ_DIR'] = os.path.join(root_dir, 'quiz_out')
    env['RUNTIME_DIR'] = os.path.join(root_dir, 'runtime')
    env['RUNTIME_MODELS_DIR'] = os.path.join(root_dir, 'runtime', 'models')
    env['RUNTIME_LOGS_DIR'] = os.path.join(root_dir, 'runtime', 'logs')
    env['RUNTIME_CONFIG_DIR'] = os.path.join(root_dir, 'runtime', 'config')
    
    try:
        backend_log_file = open(get_log_file(), 'a', encoding='utf-8')
        backend_process = subprocess.Popen(
            [python_exe, app_py],
            cwd=backend_dir,
            stdout=backend_log_file,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW,
            env=env
        )
    except Exception as e:
        show_error_and_exit("Backend Error", f"Could not start the backend process: {e}")
        
    # 3. Poll health
    log("Waiting for backend to be ready...")
    if not poll_backend():
        backend_process.terminate()
        show_error_and_exit("Backend Timeout", "The backend failed to start within the expected time. Please check logs/startup.log.")
        
    # 4. Launch Java
    log("Backend is ready. Launching Java client...")
    classpath = os.path.join(java_dir, 'bin') + os.pathsep + os.path.join(java_dir, 'lib', '*')
    
    try:
        java_log_file = open(get_log_file(), 'a', encoding='utf-8')
        java_process = subprocess.Popen(
            [java_exe, "-cp", classpath, "Login"],
            cwd=java_dir,
            stdout=java_log_file,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception as e:
        backend_process.terminate()
        show_error_and_exit("Java Error", f"Could not start the Java application: {e}")
        
    # 5. Wait for Java
    java_exit_code = java_process.wait()
    java_log_file.close()
    log(f"Java client exited with code {java_exit_code}.")
    
    # 6. Terminate backend
    log("Terminating backend...")
    backend_process.terminate()
    try:
        backend_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        backend_process.kill()
    backend_log_file.close()

    if java_exit_code != 0:
        show_error_and_exit(
            "Java Error",
            f"The Java application exited with code {java_exit_code}. Please check logs/startup.log for details."
        )
        
    log("=== Launcher Exited ===")

if __name__ == '__main__':
    main()
