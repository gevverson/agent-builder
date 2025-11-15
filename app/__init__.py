from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

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
    
    # This creates the database tables if they don't exist
   
    return app