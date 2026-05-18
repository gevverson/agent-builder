import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Get secret key from .env
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    DEPLOY_WEBHOOK_SECRET = os.environ.get('DEPLOY_WEBHOOK_SECRET')
    DEPLOY_REPO_PATH = os.environ.get('DEPLOY_REPO_PATH')
    DEPLOY_WSGI_PATH = os.environ.get('DEPLOY_WSGI_PATH')
    DEPLOY_EXPECTED_REMOTE_URL = os.environ.get('DEPLOY_EXPECTED_REMOTE_URL')
    DEPLOY_EXPECTED_BRANCH = os.environ.get('DEPLOY_EXPECTED_BRANCH', 'main')
    MAX_MESSAGE_LENGTH = int(os.environ.get('MAX_MESSAGE_LENGTH', '2000'))
    MAX_AGENT_NAME_LENGTH = int(os.environ.get('MAX_AGENT_NAME_LENGTH', '100'))
    MAX_AGENT_INSTRUCTIONS_LENGTH = int(os.environ.get('MAX_AGENT_INSTRUCTIONS_LENGTH', '10000'))
    
    # Set up the local SQLite database file
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
