# Quiz Application Backend

This is the Flask backend for the Quiz Application. It processes uploaded PDFs, extracts educational content using Google Gemini Vision, and generates structured JSON quizzes using Google Gemini API.

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

### Required Variables:
- `GEMINI_API_KEY`: Your Google Gemini API key.

### Optional Variables (defaults provided):
- `GEMINI_MODEL`: The model to use (default: `gemini-1.5-flash` or `gemini-3.5-flash`).
- `FLASK_PORT`: The port the server runs on (default: `5000`).

## Local Setup

1. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Poppler Installation:**
   The backend relies on `pdf2image`, which requires `poppler-utils` to be installed and available on your system's `PATH`.
   - **Windows**: Download Poppler binaries, extract them, and add the `bin/` folder to your system `PATH`.
   - **Linux**: `sudo apt-get install poppler-utils`
   - **macOS**: `brew install poppler`

3. **Run the server:**
   ```bash
   python app.py
   ```

## Docker Build

You can build and run the backend locally using Docker. This avoids needing to install Poppler on your host machine.

```bash
docker build -t quiz-backend .
docker run -p 5000:5000 --env-file .env quiz-backend
```

## Railway Deployment

This backend is completely ready for deployment on [Railway](https://railway.app). 

Railway will automatically detect the `Dockerfile` and build the application. 

1. Create a New Project on Railway.
2. Deploy from your GitHub repository.
3. Under the **Variables** tab in Railway, add your `NVIDIA_API_KEY`.
4. The Dockerfile automatically installs `poppler-utils` and sets up the Python environment using `python:3.12-slim`.

The server will automatically start and expose the correct port!
