import os
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance (initialized in create_app)
db = SQLAlchemy()


def setup_db(app, database_path=None):
    """Bind a flask application and a SQLAlchemy service."""
    database_path = database_path or os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # optional: return db
    # return db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(), nullable=False, unique=True)

    def format(self):
        return {"id": self.id, "type": self.type}


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(), nullable=False)
    answer = db.Column(db.String(), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    def format(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "difficulty": self.difficulty,
        }
