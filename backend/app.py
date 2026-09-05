"""Main Flask Application Entry Point"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from backend.config import config
from loguru import logger

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Setup logging
logger.add(
    app.config['LOG_FILE'],
    rotation="500 MB",
    retention="10 days",
    level=app.config['LOG_LEVEL']
)

# Register blueprints
from backend.routes import stocks, analysis, predictions
app.register_blueprint(stocks.stocks_bp, url_prefix='/api')
app.register_blueprint(analysis.analysis_bp, url_prefix='/api')
app.register_blueprint(predictions.predictions_bp, url_prefix='/api')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'environment': env
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all exceptions"""
    logger.error(f"Unhandled exception: {error}")
    return jsonify({'error': str(error)}), 500

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = app.config['DEBUG']
    app.run(host='0.0.0.0', port=port, debug=debug)
