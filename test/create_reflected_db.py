"""This script is used to create our test database which we can reflect in test app."""


from flask_sqlalchemy import SQLAlchemy

from flask import Flask

app = Flask(__name__)
config = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///reflect.db'
}

app.config.update(**config)

db = SQLAlchemy(app)

with app.app_context():
    db.engine.execute('CREATE TABLE IF NOT EXISTS User (id INT, name VARCHAR(50), email VARCHAR(50), PRIMARY KEY (id))')
