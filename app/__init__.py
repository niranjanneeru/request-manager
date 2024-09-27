from flask import Flask
import redis
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')

    from app.chat import chat
    app.register_blueprint(chat, url_prefix='/api/chat')

    from app.lesson_plan import  lesson_plan
    app.register_blueprint(lesson_plan, url_prefix='/api/lesson-plan')

    return app
