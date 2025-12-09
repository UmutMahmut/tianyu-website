import os
from app import create_app

config_obj = os.getenv('APP_CONFIG', 'config.ProductionConfig')
app = create_app(config_obj)
