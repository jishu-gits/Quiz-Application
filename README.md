# Quiz Application

A desktop quiz application with a Java Swing client, a local Flask backend, PDF processing, local RAG, and local Ollama-powered question generation.

The desktop edition keeps the existing Java UI behavior and communicates with the Python backend only through HTTP.

## Desktop Architecture

```
Java Swing UI
  -> http://localhost:5000
Local Python Flask backend
  -> PDF processing with pdf2image and Poppler
  -> RAG image analysis
  -> Ollama local model
  -> quiz JSON generation
```

No Python scripts are called directly from Java. The Java client uploads PDFs and fetches generated questions through the existing Flask endpoints.

## Folder Layout

```
desktop/
  java-client/
    src/
      Login.java
      Rules.java
      Quiz.java
      Score.java
      icons/
    login.jpg
    quiz.jpg
    score.jpg

  python-backend/
    app.py
    config.py
    llm_client.py
    startup_checks.py
    pdf_processing.py
    rag_pipeline.py
    quiz_generator.py
    utils.py
    requirements.txt

  runtime/
    poppler/
    models/
    logs/
    config/

  installer/
  docs/
```

## Runtime Folders

The desktop runtime folders are prepared but not packaged:

- `desktop/runtime/poppler/` stores a local Poppler distribution when one is bundled later.
- `desktop/runtime/models/` is reserved for local model/runtime assets.
- `desktop/runtime/logs/` stores backend runtime logs.
- `desktop/runtime/config/` is reserved for desktop runtime configuration.

No installer, executable, or package is created yet.

## Startup Sequence

1. Start Ollama locally.
2. Ensure the selected model exists in Ollama.
3. Start the Python backend.
4. The backend runs startup checks for Python, Ollama, the selected model, Poppler, and runtime folders.
5. Run the Java Swing client.
6. Drop a PDF in the Java UI.
7. Java sends the PDF to Flask over HTTP.
8. Flask processes the PDF, runs RAG, calls Ollama, saves the latest quiz JSON, and Java fetches it.

## Local Backend

From the repository root:

```bash
cd desktop/python-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The backend listens on:

```text
http://localhost:5000
```

The Flask server starts with the same factory and run pattern as the website backend:

```python
app = create_app()
app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, use_reloader=False)
```

## Backend API

The API contract is unchanged.

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/extract` | POST | Accepts multipart PDF upload in the `file` field and generates quiz JSON. |
| `/extractQuestions` | GET | Returns the latest generated quiz JSON. |
| `/health` | GET | Returns backend health status. |

## Java Communication

The Java Swing client uses `java.net.http.HttpClient`:

- `Login.java` sends `POST http://localhost:5000/extract`.
- `Quiz.java` sends `GET http://localhost:5000/extractQuestions`.

Java does not call Python scripts directly.

## Configuration

Runtime paths and backend settings live in `desktop/python-backend/config.py`.

Common environment overrides:

```text
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llava
POPPLER_PATH=../runtime/poppler
DEFAULT_QUESTION_COUNT=10
```

`llm_client.py` is the only module that knows how to talk to Ollama. The rest of the backend uses the same model call boundary for vision analysis and quiz generation.
