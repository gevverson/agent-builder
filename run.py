from app import create_app, db

# --- NEW: We must import all our models so the DB can see them ---
from app.models import Agent, KnowledgeFile, Conversation

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # This creates the tables for Agent, KnowledgeFile, AND Conversation
        db.create_all() 

    print("Database tables created successfully in 'app.db'!")
    app.run(debug=True, port=5000)