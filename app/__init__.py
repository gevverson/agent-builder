from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

# --- THE CORRECTED IMPORT ---
# We are importing the class 'MemoryClient' as suggested by the error
from mem0 import MemoryClient

# Create the database instance
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the database with the app
    db.init_app(app)

    # Import and register our routes
    from app import routes, models
    app.register_blueprint(routes.bp)
    
    return app

# Initialize Mem0
# --- THE CORRECTED INITIALIZATION ---
# We are creating an instance of 'MemoryClient'
mem0 = MemoryClient()