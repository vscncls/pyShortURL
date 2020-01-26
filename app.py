from src.controllers import register_blueprints
from src.database import db
from flask import Flask
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
register_blueprints(app)


def setup_database():
    db.create_all(app=app)


if __name__ == "__main__":
    app.run()
