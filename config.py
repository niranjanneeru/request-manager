import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", True)
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_API_URL = os.getenv("QDRANT_API_URL")

    BASE_URL = os.getenv("BASE_URL")
