
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# If testing declared model classes uncomment
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50))
    email = db.Column(db.String(length=50))
