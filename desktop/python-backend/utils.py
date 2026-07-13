import logging
import sys
import os
import shutil
from flask import jsonify
from config import Config

# =============================================================================
# Logger (from utils/logger.py)
# =============================================================================

def setup_logger(name='quiz_backend'):
    """Configures and returns a standard logger for the application."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        
        # Standardized log format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        
        logger.addHandler(ch)

        if os.path.isdir(Config.RUNTIME_LOGS_DIR):
            fh = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        else:
            logger.warning(f"Runtime log directory is missing: {Config.RUNTIME_LOGS_DIR}")
        
    return logger

# Global logger instance
logger = setup_logger()

# =============================================================================
# File Utilities (from utils/file_utils.py)
# =============================================================================

def ensure_directories():
    """Ensures all required application directories exist."""
    for folder in Config.get_directories():
        os.makedirs(folder, exist_ok=True)
        logger.info(f"Ensured directory exists: {folder}")

def cleanup_temp_folder():
    """Removes all files from the TEMP_DIR."""
    try:
        temp_dir = Config.TEMP_DIR
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        logger.info("Temp folder cleanup complete.")
    except Exception as e:
        logger.error(f"Error during temp folder cleanup: {e}")

def get_base_filename(filename):
    """Utility function to extract the base of a filename (without extension)."""
    return os.path.splitext(filename)[0]

# =============================================================================
# Response Helpers (from utils/response.py)
# =============================================================================

def success_response(data=None, message="Success", status_code=200):
    """
    Standardized success response format.
    The response maintains the original contract expected by the legacy Java client
    by allowing flat inclusion of specific keys via kwargs if data is a dict.
    """
    response_body = {
        "success": True,
        "message": message
    }
    
    if data is not None:
        if isinstance(data, dict):
            response_body.update(data)
        else:
            response_body["data"] = data
            
    return jsonify(response_body), status_code

def error_response(message="An error occurred", code="ERROR", status_code=500):
    """
    Standardized error response format.
    Ensures 'error' key exists for legacy compatibility.
    """
    response_body = {
        "success": False,
        "error": message,
        "code": code
    }
    return jsonify(response_body), status_code
