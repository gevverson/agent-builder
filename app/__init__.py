from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from mem0 import Memory

# --- CONFIGURATION ---
mem0_config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": ".mem0_db",
            # --- FIX IS HERE: Use the correct name "embedding_model_dims" ---
            "embedding_model_dims": 768
        }
    },
    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "text-embedding-004",
            "api_key": Config.GEMINI_API_KEY
        }
    },
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-flash-latest",
            "api_key": Config.GEMINI_API_KEY
        }
    }
}
# ---------------------

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    from app import routes, models
    app.register_blueprint(routes.bp)
    return app

mem0 = Memory.from_config(mem0_config)