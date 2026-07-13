# Quiz Application — Desktop Edition

Desktop edition of the Quiz Application. This reorganizes the project into a clean folder structure for a desktop deployment workflow.

## Folder Structure

```
desktop/
├── java-client/          # Java Swing GUI application
│   ├── src/
│   │   ├── Login.java    # Entry point — login screen with PDF drag-and-drop
│   │   ├── Rules.java    # Quiz rules screen
│   │   ├── Quiz.java     # Quiz-taking screen (fetches questions from backend)
│   │   ├── Score.java    # Results display screen
│   │   └── icons/        # UI icon assets
│   ├── login.jpg         # Login screen background image
│   ├── quiz.jpg          # Quiz screen background image
│   └── score.jpg         # Score screen background image
│
├── python-backend/       # Flask API backend
│   ├── app.py            # Flask application entry point
│   ├── config.py         # Configuration (paths, API keys, server settings)
│   ├── llm_client.py     # Gemini API model initialization
│   ├── pdf_processing.py # PDF-to-image conversion (via pdf2image/poppler)
│   ├── rag_pipeline.py   # Vision inference on extracted images
│   ├── quiz_generator.py # Quiz JSON generation from extracted text
│   ├── utils.py          # Logger, file utilities, response helpers
│   ├── requirements.txt  # Python dependencies
│   └── .env              # Environment variables (API keys, server config)
│
├── runtime/              # (Reserved) Runtime binaries, JRE, Python venv
├── installer/            # (Reserved) Installer scripts and packaging
└── docs/                 # (Reserved) Additional documentation
```

## How to Start the Backend

### Prerequisites

- Python 3.10+
- Poppler installed and in PATH (for `pdf2image`)
- A valid Gemini API key in `.env`

### Steps

```bash
cd desktop/python-backend

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

The server will start on `http://0.0.0.0:5000` by default.

### API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/extract` | POST | Upload a PDF (multipart `file` field). Processes it and generates quiz questions. |
| `/extractQuestions` | GET | Returns the latest generated quiz as JSON. |
| `/health` | GET | Health check endpoint. |

## How Java Connects (Future)

The Java Swing client communicates with the Python backend over HTTP:

1. **PDF Upload**: `Login.java` sends the PDF via `POST /extract` using `java.net.http.HttpClient` with multipart/form-data.
2. **Quiz Fetch**: `Quiz.java` retrieves questions via `GET /extractQuestions` and parses the JSON using Jackson (`ObjectMapper`).

Currently, the Java client is hardcoded to `http://localhost:5000`. No changes to the Java–backend communication protocol are planned at this stage — just the folder relocation.

> **Note**: Java–backend integration is not implemented in this edition. The Java client and Python backend are placed in their respective folders but are not yet wired together for a single-click launch.
