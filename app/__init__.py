import logging

from flask import Flask, request
from flask_cors import CORS

from config import Config


def create_app():
    app = Flask(__name__)
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

    # Log incoming requests
    @app.before_request
    def log_request_info():
        logging.info(f"Request: {request.method} {request.url} from {request.remote_addr}")
        logging.info(f"Headers: {dict(request.headers)}")
        if request.data:
            logging.info(f"Body: {request.data.decode('utf-8')}")

    # Log outgoing responses
    @app.after_request
    def log_response_info(response):
        logging.info(f"Response: {response.status} {response.get_data(as_text=True)}")
        return response

    CORS(app)
    app.config.from_object(Config)

    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')

    from app.chat import chat
    app.register_blueprint(chat, url_prefix='/api/chat')

    from app.lesson_plan import lesson_plan
    app.register_blueprint(lesson_plan, url_prefix='/api/lesson-plan')

    return app
