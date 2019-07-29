from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from random import choice
from string import ascii_lowercase, ascii_uppercase


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'thekeyboardcat'
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Urls(db.Model):
    id_url = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000))
    # 50 because of custom urls
    shortenend_url = db.Column(db.String(50), unique=True)
    # 1 = random, 2 = custom
    type = db.Column(db.Integer)


class Url:
    def __init__(self, url):
        self.url = str(url)

    def shorten(self, size=5):
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
            if not self.get_from_short(short):
                duplicate = False

        self.shortenend_url = short
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
                type=self.type)
        db.session.add(_url)
        db.session.commit()
        return True

    @staticmethod
    def get_from_id(id_url):
        """Returns an url object based on given id."""
        q = Urls.query.filter_by(id_url=id_url).first()
        if not q:
            return None
        obj = Url(q.url)
        obj.id = q.url_id
        obj.url = q.url
        obj.shortenend_url = q.shortenend_url
        obj.type = q.type
        return obj

    @staticmethod
    def get_from_url(url, type):
        """Returns an url object based on given url."""
        q = Urls.query.filter_by(url=url, type=type).first()
        if not q:
            return None
        obj = Url(q.url)
        obj.id = q.id_url
        obj.url = q.url
        obj.shortenend_url = q.shortenend_url
        obj.type = q.type
        return obj

    @staticmethod
    def get_from_short(short_url):
        """Returns an url object based on giver shortenend url."""
        q = Urls.query.filter_by(shortenend_url=short_url, type=1).first()
        if not q:
            return None
        obj = Url(q.url)
        obj.id = q.id_url
        obj.url = q.url
        obj.shortenend_url = q.shortenend_url
        obj.type = 1
        return obj

    @staticmethod
    def get_from_custom(custom_url):
        """Returns url obj based on custom_url"""
        q = Urls.query.filter_by(shortenend_url=custom_url, type=2).first()
        if not q:
            return None
        obj = Url(q.url)
        obj.id = q.id_url
        obj.url = q.url
        obj.shortenend_url = q.shortenend_url
        obj.type = 2

        return obj


@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Shortens url."""
    data = request.get_json()
    if 'url' not in data:
        return jsonify({
            'msg': 'Error, expected url parameter',
            'code': 422
            })
    q_url = Url.get_from_url(data['url'], type=1)
    if q_url:
        return jsonify({
                'msg': 'ok',
                'url': q_url.shortenend_url
            })
    _url = Url(data['url'])
    _url.shorten()
    _url.persist()

    return jsonify({
        'msg': 'ok',
        'url': _url.shortenend_url
        })


@app.route('/custom', methods=['POST'])
def custom_url():
    """Sets a custom shortenend URL."""
    data = request.get_json()
    # Verify if needed parameters were given
    if 'url' not in data:
        return jsonify({
            'msg': 'Error, expected url parameter',
            'code': 422
            })
    if 'custom_url' not in data:
        return jsonify({
            'msg': 'Error, expected custom_url parameter',
            'code': 422
            })

    # Verify if given custom_url is already in db
    _url = Url.get_from_custom(data['custom_url'])
    if hasattr(_url, 'url'):
        return jsonify({
            'msg': 'given custom_url already used',
            'code': 409
            })

    url = Url(data['url'])
    url.custom_url(data['custom_url'])
    url.persist()

    return jsonify({
        'msg': 'ok',
        'url': data['url'],
        'custom_url': data['custom_url']
        })


@app.route('/u/<url>', methods=['GET'])
def redirect_url(url):
    """Returns the actual URL."""
    _url = Url.get_from_short(url)
    if not _url:
        return jsonify({
                'msg': 'not found',
                'url': None
                })

    return jsonify({
            'msg': 'ok',
            'url': _url.url
        })


@app.route('/c/<url>', methods=['GET'])
def redirect_custom(url):
    """Returns url based on given custom_url."""
    _url = Url.get_from_custom(url)
    if not hasattr(_url, 'url'):
        return jsonify({
                'msg': 'not found',
                'url': None
            })

    return jsonify({
                'msg': 'ok',
                'url': _url.url
            })


if __name__ == '__main__':
    # binds to port if defined else defaults to 8000
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, port=port)
