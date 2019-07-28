from flask import Flask, request, jsonfy, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from random import choice
from string import ascii_lowercase, ascii_uppercase


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'thekeyboardcat'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
db = SQLAlchemy(app)


class Urls(db.model):
    id_url = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), unique=True)
    # unique because if there were >1 there'd be conflicts
    shortenend_url = db.Column(db.String(50), unique=True)
    # 1 = random, 2 = custom
    type = db.Column(db.Integer)


class Url:
    def __init__(self, url):
        self.url = str(url)

    def shorten(self, size='8'):
        """Shotens an URL

        sets self.shortenend and returns shotened URL, sets type to random(1)
        """
        # upper/lower case and nums
        chars = ascii_uppercase + ascii_lowercase + '0123456789'

        # defaults to true so it enters the loop
        duplicate = True
        while duplicate:
            short = ''.join(choice(chars) for i in range(size))
            # Checks if the short url is a duplicate
            if not self.get_from_short(short).url:
                duplicate = False

        self.shortenend = short
        self.type = 1
        return short

    def custom_url(self, url):
        """Sets url to given url and changes type to Custom(2)"""
        self.shortenend_url = url
        self.type = 2
        return True

    def persist(self):
        """Saves object to the db."""
        _url = Urls(
                url=self.url,
                shortenend_url=self.shortenend_url,
                type=2)
        db.session.add(_url)
        db.session.commit()
        return True

    @staticmethod
    def get_from_id(id_url):
        """Returns an url object based on given id."""
        q = Urls.query.filter_by(id_url=id_url).first()
        obj = Url(q.url)
        obj.id = q.url_id
        obj.url = q.url
        obj.shortenend_url = q.shortenend_url
        obj.type = q.type
        return obj

    @staticmethod
    def get_from_url(url, type=1):
        """Returns an url object based on given url."""
        q = Urls.query.filter_by(url=url, type=type).first()
        obj = Url(q.url)
        obj.id = q.url_id
        obj.url = q.url
        obj.shortenend_url = q.shortenend_url
        obj.type = q.type
        return obj

    @staticmethod
    def get_from_short(short_url):
        """Returns an url object based on giver shortenend url."""
        q = Urls.query.filter_by(shortenend_url=short_url).first()
        obj = Url(q.url)
        obj.id = q.url_id
        obj.url = q.url
        obj.shortenend_url = q.shortenend_url
        obj.type = q.type
        return obj


@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Shortens url."""
    data = request.get_json()
    q_url = Url.get_from_url(data['url']).url
    if q_url:
        return jsonfy({
                'msg': 'ok',
                'method': 'already exists',
                'url': q_url
            })
    _url = Url(data['url'])
    _url.persist()

    return jsonfy({
        'msg': 'Ok',
        'method': 'new',
        'url': _url.shortenend
        })


@app.route('/u/<url>', methods=['GET'])
def redirect_url(url):
    """Returns the actual URL."""
    try:
        _url = Url.get_from_url(url=url, type=1).url
    except AttributeError:
        return jsonfy({
                'msg': 'not found',
                'url': None
            })

    return jsonfy({
            'msg': 'ok',
            'url': _url
        })


@app.route('/c/<url>', methods=['GET'])
def redirect_custom(url):
    """Returns custom url."""
    try:
        _url = Url.get_from_url(url=url, type=2).url
    except AttributeError:
        return jsonfy({
                'msg': 'not found',
                'url': None
            })

    return jsonfy({
                'msg': 'ok',
                'url': _url
            })


if __name__ == '__main__':
    # binds to port if defined else defaults to 8000
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, port=port)
