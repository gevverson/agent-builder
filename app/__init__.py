from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from mem0 import Memory

# --- RESEARCHED CONFIGURATION ---
# 1. Vector Store: Qdrant (Stable, Local)
# 2. Embedder: Sentence-Transformers (Local)
# 3. LLM: Gemini (Your Key)
mem0_config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": ".mem0_db" # Local folder for memory
        }
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "all-MiniLM-L6-v2"
        }
    },
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-2.0-flash-lite-preview-02-05", # Your working model
            "api_key": Config.GEMINI_API_KEY
        }
    }
}

# Create database instance
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app import routes, models
    app.register_blueprint(routes.bp)
    
    return app

# Initialize Mem0
mem0 = Memory.from_config(mem0_config)