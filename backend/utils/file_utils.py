import os
import shutil
from config import Config
from utils.logger import logger

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
