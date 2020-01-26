from src.database import db


class Url(db.Model):
    id_url = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000))
    # 50 because of custom urls
    shortenend_url = db.Column(db.String(50), unique=True)
    # 1 = random, 2 = custom
    url_type = db.Column(db.Integer)
