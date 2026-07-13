import os
import pdf2image
from config import Config
from utils import logger

def extract_images_from_pdf(pdf_path: str) -> int:
    """
    Converts a PDF file into a sequence of PNG images and saves them in TEMP_DIR.
    
    Args:
        pdf_path: The absolute path to the PDF file.
        
    Returns:
        int: The number of pages/images generated.
        
    Raises:
        Exception: If the conversion fails (e.g. Poppler missing).
    """
    try:
        logger.info(f"Starting PDF to image conversion for: {pdf_path}")
        
        import shutil
        pdfinfo_path = shutil.which("pdfinfo")
        poppler_path = os.path.dirname(pdfinfo_path) if pdfinfo_path else None
        
        images = pdf2image.convert_from_path(pdf_path, poppler_path=poppler_path)
        
        for idx, image in enumerate(images):
            image_path = os.path.join(Config.TEMP_DIR, f"output_page_{idx + 1}.png")
            image.save(image_path, 'PNG')
            
        logger.info(f"Images created successfully! Total pages: {len(images)}")
        return len(images)
        
    except Exception as e:
        import traceback
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_num = exc_tb.tb_lineno
        stack_trace = traceback.format_exc()
        logger.error(f"Error converting PDF to images.")
        logger.error(f"Exception Type: {exc_type.__name__}")
        logger.error(f"Message: {str(e)}")
        logger.error(f"File: {file_name}")
        logger.error(f"Line Number: {line_num}")
        logger.error(f"Stack Trace:\n{stack_trace}")
        raise e
