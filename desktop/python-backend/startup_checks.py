import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from config import Config
from llm_client import get_available_models, has_model
from utils import logger


@dataclass
class StartupCheck:
    name: str
    ok: bool
    message: str


@dataclass
class StartupVerificationResult:
    checks: list

    @property
    def ok(self):
        return all(check.ok for check in self.checks)


def verify_startup():
    checks = [
        _check_python(),
        _check_ollama_installed(),
        _check_selected_model(),
        _check_poppler(),
        *_check_runtime_directories(),
    ]

    for check in checks:
        if check.ok:
            logger.info(f"Startup check passed: {check.name} - {check.message}")
        else:
            logger.error(f"Startup check failed: {check.name} - {check.message}")

    result = StartupVerificationResult(checks=checks)
    if result.ok:
        logger.info("Startup verification completed successfully.")
    else:
        logger.error("Startup verification completed with missing requirements.")
    return result


def _check_python():
    executable = Path(sys.executable)
    if executable.exists():
        version = ".".join(map(str, sys.version_info[:3]))
        return StartupCheck("Python", True, f"Python {version} at {executable}")

    python_path = shutil.which("python") or shutil.which("python3")
    if python_path:
        return StartupCheck("Python", True, f"Python executable found at {python_path}")

    return StartupCheck("Python", False, "Python executable was not found.")


def _check_ollama_installed():
    ollama_path = shutil.which("ollama")
    if ollama_path:
        return StartupCheck("Ollama", True, f"Ollama executable found at {ollama_path}")

    return StartupCheck(
        "Ollama",
        False,
        "Ollama executable was not found in PATH. Install Ollama or add it to PATH.",
    )


def _check_selected_model():
    try:
        model_names = get_available_models()
    except RuntimeError as exc:
        return StartupCheck("Selected model", False, str(exc))

    if has_model(model_names, Config.OLLAMA_MODEL):
        return StartupCheck("Selected model", True, f"Model is available: {Config.OLLAMA_MODEL}")

    available = ", ".join(model_names) if model_names else "none"
    return StartupCheck(
        "Selected model",
        False,
        f"Model '{Config.OLLAMA_MODEL}' is not available in Ollama. Available models: {available}",
    )


def _check_poppler():
    poppler_bin_dir = Config.get_poppler_bin_dir()
    if poppler_bin_dir:
        return StartupCheck("Poppler", True, f"pdfinfo found in {poppler_bin_dir}")

    return StartupCheck(
        "Poppler",
        False,
        "Poppler was not found. Place Poppler under desktop/runtime/poppler, set POPPLER_PATH, or add pdfinfo to PATH.",
    )


def _check_runtime_directories():
    checks = []
    for folder in Config.get_runtime_directories():
        path = Path(folder)
        checks.append(
            StartupCheck(
                f"Runtime folder {path.name}",
                path.is_dir(),
                str(path) if path.is_dir() else f"Missing runtime folder: {path}",
            )
        )
    return checks
