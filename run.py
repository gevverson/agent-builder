from app import create_app, db
from app.models import Agent, KnowledgeFile # <-- NEW: Import our models

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # This tells SQLAlchemy to look at all imported Models
        # (like Agent, KnowledgeFile) and create tables for them.
        db.create_all() 
        
    print("Database tables created in 'app.db'!")
    app.run(debug=True, port=5000)