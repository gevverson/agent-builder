from app import db
from datetime import datetime

# This is our table for Agents (from Milestone 2)
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    knowledge_files = db.relationship('KnowledgeFile', backref='agent', lazy=True, cascade="all, delete-orphan")

    # --- NEW ---
    # This links the Agent to its conversation history
    conversations = db.relationship('Conversation', backref='agent', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Agent {self.name}>'

# This is our table for Knowledge Files (for later)
class KnowledgeFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)

    def __repr__(self):
        return f'<KnowledgeFile {self.filename}>'

# --- THIS IS YOUR NEW LONG-TERM MEMORY TABLE ---
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False) # Will be 'user' or 'model'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)

    def __repr__(self):
        return f'<Conversation {self.role}>'