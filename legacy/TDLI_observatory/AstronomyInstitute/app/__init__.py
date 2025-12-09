import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "tianyu-telescope-secret-key-2025")
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    return app
