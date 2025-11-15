from app import db

# 1. The "Agent" Table
# This will store the name and instructions for each AI agent.
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    
    # This creates a "link" from the Agent to its KnowledgeFiles.
    # It tells the Agent: "You have many files."
    knowledge_files = db.relationship('KnowledgeFile', backref='agent', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Agent {self.name}>'


# 2. The "KnowledgeFile" Table
# This will store the text content from the files Roman uploads.
class KnowledgeFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # This is the "foreign key" that links this file back to an Agent.
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)

    def __repr__(self):
        return f'<KnowledgeFile {self.filename}>'