from app import create_app, db
# We only import Agent for now.
# Mem0 handles the memory internally, so we don't need a Conversation table.
from app.models import Agent 

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # This creates the database with just the Agent table
        db.create_all() 
    app.run(debug=True, port=5000)