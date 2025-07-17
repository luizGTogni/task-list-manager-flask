from src import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, default="Task")
    description = db.Column(db.String(150), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    user_owner = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }