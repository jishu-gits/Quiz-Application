# Backend Architecture

The backend of the Quiz Application has been migrated to use the Google Gemini API. It is designed to be a lightweight Flask service that processes uploaded PDFs, extracts their content, and generates a structured quiz in JSON format.

## Pipeline Overview

When a user uploads a PDF from the frontend, the following sequence occurs:

1. **Upload & Save**: The `/extract` route receives the PDF and saves it temporarily to the `content/` folder.
2. **PDF to Image Conversion**: The `pdf_service.py` uses `pdf2image` and Poppler to convert each page of the PDF into high-quality PNG images, stored in the `temp/` folder.
3. **Vision Analysis (Gemini Vision)**: `vision_service.py` sequentially processes these images using the Google Gemini model. It extracts the core educational concepts and summarizes them into concise text.
4. **Quiz Generation (Gemini LLM)**: `quiz_service.py` takes the extracted text from the previous step and prompts the Gemini model to generate exactly 10 high-quality multiple-choice questions. It forces the output into a strict JSON format.
5. **Response**: The JSON is validated and passed back to the frontend, and all temporary folders are cleaned up to prevent storage bloat.

## Key Services

- `vision_service.py`: Interfaces with the Google GenAI SDK to perform visual question answering and text extraction from screenshots of the PDF.
- `quiz_service.py`: Uses the Google GenAI SDK to generate structured JSON schemas containing the final questions.
- `pdf_service.py`: Handles all OS-level interactions involving Poppler to correctly rasterize the PDFs.

## Migration Note

The backend was originally designed for the NVIDIA API but has since been successfully migrated to the `google-generativeai` SDK for more reliable multimodal processing capabilities.
