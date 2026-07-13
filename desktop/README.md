# Quiz Application Desktop Edition

The desktop edition contains the Java Swing client, local Python backend, desktop runtime folders, installer placeholder, and desktop documentation placeholder.

## Architecture

```
Java Swing UI
  -> HTTP on http://localhost:5000
Python Flask backend
  -> PDF processing
  -> RAG
  -> local Ollama
  -> generated quiz JSON
```

The Java application communicates with Python only through HTTP. It does not launch or call Python scripts directly.

## Layout

```
desktop/
  java-client/
  python-backend/
  runtime/
    poppler/
    models/
    logs/
    config/
  installer/
  docs/
```

## Backend Startup

```bash
cd desktop/python-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The backend listens on `http://localhost:5000`.

## Startup Checks

`python-backend/startup_checks.py` verifies:

- Python is available.
- Ollama is installed.
- The configured Ollama model is available.
- Poppler is available.
- Runtime folders exist.

Missing requirements are reported clearly in the console and backend log. Installation is not attempted.

## Runtime

Runtime paths are configured in `python-backend/config.py`.

- `runtime/poppler/`: local Poppler location.
- `runtime/models/`: reserved model/runtime assets.
- `runtime/logs/`: backend log output.
- `runtime/config/`: reserved runtime configuration.

## API

The backend API is unchanged:

| Endpoint | Method | Description |
| --- | --- | --- |
| `/extract` | POST | Upload and process a PDF. |
| `/extractQuestions` | GET | Return the latest generated quiz JSON. |
| `/health` | GET | Health check. |

## Java Client

`java-client/src/Login.java` uploads PDFs to `POST /extract`.

`java-client/src/Quiz.java` fetches quiz data from `GET /extractQuestions`.

The Swing UI layout and quiz behavior are preserved.
