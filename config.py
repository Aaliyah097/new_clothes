import os
from dotenv import load_dotenv

_basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    load_dotenv()

    SECRET_KEY = os.environ.get('SECRET_KEY')

    CORS_HEADERS = 'Content-Type'

    BASIC_AUTH_USERNAME = os.environ.get('USER')
    BASIC_AUTH_PASSWORD = os.environ.get('PASSWORD')
    BASIC_AUTH_FORCE = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')
    DATABASE_CONNECT_OPTIONS = {}

    UPLOAD_FOLDER = os.path.join(_basedir, "static/")
    ALLOWED_EXTENSIONS = {"jpg", "png", "svg", 'webp'}
    MAX_CONTENT_LENGTH = 1000 * 1024 * 1024  # 1000mb
