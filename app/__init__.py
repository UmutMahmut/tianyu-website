import os
from flask import Flask
from .routes import bp as main_bp


def create_app(config_object='config.ProductionConfig'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_object)

    # 从 systemd Environment= 注入的环境变量读取 SECRET_KEY
    env_secret_key = os.getenv("SECRET_KEY")
    if env_secret_key:
        app.config["SECRET_KEY"] = env_secret_key

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY is not set")

    # HTTPS 站点建议开启
    app.config.setdefault("SESSION_COOKIE_SECURE", True)
    app.config.setdefault("SESSION_COOKIE_SAMESITE", "Lax")

    app.register_blueprint(main_bp)
    return app