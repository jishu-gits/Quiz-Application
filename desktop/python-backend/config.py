import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent
DESKTOP_ROOT = BACKEND_DIR.parent
DEFAULT_RUNTIME_DIR = DESKTOP_ROOT / "runtime"
env_path = BACKEND_DIR / ".env"
load_dotenv(env_path)


def _env_bool(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in ("true", "1", "t", "yes", "y")


def _resolve_path(value, default_path, base_dir):
    path = Path(value) if value else Path(default_path)
    if not path.is_absolute():
        path = Path(base_dir) / path
    return str(path.resolve())


class Config:
    # Server config
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", 5000))
    DEBUG = _env_bool("FLASK_DEBUG", True)

    # Project-relative paths
    BASE_DIR = str(BACKEND_DIR)
    DESKTOP_DIR = str(DESKTOP_ROOT)

    CONTENT_DIR = _resolve_path(os.getenv("CONTENT_DIR"), BACKEND_DIR / "content", BACKEND_DIR)
    TEMP_DIR = _resolve_path(os.getenv("TEMP_DIR"), BACKEND_DIR / "temp", BACKEND_DIR)
    OUTPUT_DIR = _resolve_path(os.getenv("OUTPUT_DIR"), BACKEND_DIR / "output", BACKEND_DIR)
    QUIZ_DIR = _resolve_path(os.getenv("QUIZ_DIR"), BACKEND_DIR / "quiz_out", BACKEND_DIR)

    RUNTIME_DIR = _resolve_path(os.getenv("RUNTIME_DIR"), DEFAULT_RUNTIME_DIR, DESKTOP_ROOT)
    RUNTIME_POPPLER_DIR = _resolve_path(
        os.getenv("RUNTIME_POPPLER_DIR") or os.getenv("POPPLER_DIR"),
        Path(RUNTIME_DIR) / "poppler",
        RUNTIME_DIR,
    )
    RUNTIME_MODELS_DIR = _resolve_path(
        os.getenv("RUNTIME_MODELS_DIR"),
        Path(RUNTIME_DIR) / "models",
        RUNTIME_DIR,
    )
    RUNTIME_LOGS_DIR = _resolve_path(
        os.getenv("RUNTIME_LOGS_DIR"),
        Path(RUNTIME_DIR) / "logs",
        RUNTIME_DIR,
    )
    RUNTIME_CONFIG_DIR = _resolve_path(
        os.getenv("RUNTIME_CONFIG_DIR"),
        Path(RUNTIME_DIR) / "config",
        RUNTIME_DIR,
    )
    LOG_FILE = _resolve_path(os.getenv("LOG_FILE"), Path(RUNTIME_LOGS_DIR) / "backend.log", RUNTIME_LOGS_DIR)

    POPPLER_PATH = _resolve_path(os.getenv("POPPLER_PATH"), RUNTIME_POPPLER_DIR, RUNTIME_DIR)

    # Local LLM config
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "granite3.2-vision")
    OLLAMA_REQUEST_TIMEOUT = int(os.getenv("OLLAMA_REQUEST_TIMEOUT", 300))
    DEFAULT_QUESTION_COUNT = int(os.getenv("DEFAULT_QUESTION_COUNT", 10))

    STARTUP_CHECK_STRICT = _env_bool("STARTUP_CHECK_STRICT", False)

    @classmethod
    def get_directories(cls):
        """Returns a list of backend working directories."""
        return [cls.CONTENT_DIR, cls.TEMP_DIR, cls.OUTPUT_DIR, cls.QUIZ_DIR]

    @classmethod
    def get_runtime_directories(cls):
        """Returns the required desktop runtime directories."""
        return [
            cls.RUNTIME_POPPLER_DIR,
            cls.RUNTIME_MODELS_DIR,
            cls.RUNTIME_LOGS_DIR,
            cls.RUNTIME_CONFIG_DIR,
        ]

    @classmethod
    def get_poppler_bin_dir(cls):
        """Returns a Poppler binary directory if pdfinfo is available."""
        executable_names = ["pdfinfo.exe", "pdfinfo"] if os.name == "nt" else ["pdfinfo"]
        candidate_roots = [
            Path(cls.POPPLER_PATH),
            Path(cls.POPPLER_PATH) / "Library" / "bin",
            Path(cls.POPPLER_PATH) / "bin",
            Path(cls.RUNTIME_POPPLER_DIR),
            Path(cls.RUNTIME_POPPLER_DIR) / "Library" / "bin",
            Path(cls.RUNTIME_POPPLER_DIR) / "bin",
        ]

        for candidate in candidate_roots:
            if any((candidate / executable).exists() for executable in executable_names):
                return str(candidate.resolve())

        pdfinfo_path = shutil.which("pdfinfo")
        if pdfinfo_path:
            return str(Path(pdfinfo_path).resolve().parent)
        return None
