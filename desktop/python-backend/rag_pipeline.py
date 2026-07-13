import os
import PIL.Image
from config import Config
from utils import logger
from llm_client import get_vision_model

def analyze_images() -> str:
    """
    Runs vision inference on each extracted image in TEMP_DIR via the local LLM.
    Merges outputs into a single string.
    
    Returns:
        str: The merged content text extracted from all images.
        
    Raises:
        Exception: If no images are found or if inference fails.
    """
    merged_text = ""
    
    # Process all PNG files in sorted order
    images = sorted([f for f in os.listdir(Config.TEMP_DIR) if f.endswith(".png")])
    if not images:
        raise Exception("No images found in the temp folder.")
        
    logger.info(f"Starting vision analysis on {len(images)} images using the local LLM...")
    
    model = get_vision_model()
        
    prompt = (
        "Analyze the given image. This image is a part of multiset. "
        "Understand the image, extract the important content related points "
        "and explain them in concised bullet points."
    )
    
    for image_file in images:
        image_path = os.path.join(Config.TEMP_DIR, image_file)
        logger.info(f"Processing image: {image_path}")
        
        with PIL.Image.open(image_path) as img:
            response = model.generate_content([prompt, img])
            merged_text += "\n" + response.text
        
    # Save merged text to output file
    output_file = os.path.join(Config.OUTPUT_DIR, "explanation.txt")
    with open(output_file, "w", encoding='utf-8') as fout:
        fout.write(merged_text)
        
    logger.info("Image inference completed and merged text saved.")
    return merged_text
