from flask import Flask
from .routes import bp as main_bp

def create_app(config_object='config.ProductionConfig'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_object)
    app.register_blueprint(main_bp)
    return app
