from sqlalchemy.orm import relationship
from flask_login import UserMixin
from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    todo_items = db.relationship("ToDoItem", backref="author")


class ToDoItem(db.Model):
    # __tablename__ = "todo_items"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75), nullable=False)
    description = db.Column(db.Text, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
