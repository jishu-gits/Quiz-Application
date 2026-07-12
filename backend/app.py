import shutil
from flask import Flask
from flask_cors import CORS
from config import Config
from utils.logger import logger
from utils.file_utils import ensure_directories
from routes.quiz_routes import quiz_bp
from utils.response import error_response

def create_app():
    """Application factory for the Flask backend."""
    app = Flask(__name__)
    
    # Startup Validation for Poppler (pdf2image dependency)
    if not shutil.which("pdfinfo"):
        logger.error("CRITICAL: Poppler is not installed or not in PATH. 'pdfinfo' is missing.")
        logger.error("PDF uploads will fail. Please install poppler-utils.")
    
    # Configure CORS to allow Next.js during development
    # In a strict production environment, you would restrict origins.
    CORS(app)
    
    # Ensure all required folders exist
    ensure_directories()
    
    # Register API blueprints
    app.register_blueprint(quiz_bp, url_prefix='/')
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(e):
        return error_response(message="Endpoint not found", status_code=404)
        
    @app.errorhandler(500)
    def internal_error(e):
        return error_response(message="Internal server error", status_code=500)

    @app.route('/health', methods=['GET'])
    def health_check():
        return {"status": "healthy", "service": "Quiz AI Backend"}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    logger.info(f"Starting server on {Config.HOST}:{Config.PORT}...")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, use_reloader=False)
