from app import db

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    # We will add knowledge files back in the next milestone
    # knowledge_files = db.relationship(...) 

    def __repr__(self):
        return f'<Agent {self.name}>'