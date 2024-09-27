from flask import Flask
import redis
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')

    from app.chat.routes import chat
    app.register_blueprint(chat, url_prefix='/api/chat')

    return app
