from flask import Flask, request, jsonfy, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from random import choice
from string import ascii_lowercase, ascii_uppercase


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thekeyboardcat'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://lucas:passwd@localhost/shorturl'
db = SQLAlchemy(app)

class Urls(db.model):
    id_url = db.Column(db.Integer, primary_key=True)
    # url is unique because if an url is already in the db the same shorturl is supplied
    url = db.Column(db.String(1000), unique=True)
    # unique because if there were >1 there'd be conflicts
    shortenend_url = db.Column(db.String(50), unique=True)

class Url:
    def __init__(self, url):
        self.url = str(url)
        self.shortened = self.shorten()

    def shorten(self, size='8'):
	"""Shotens an URL, sets self.shortened and returns shotened URL"""
        chars = ascii_uppercase + ascii_lowercase + '0123456789'

        # defaults to true so it enters the loop
        duplicate = True
        while duplicate:
            short = ''.join(choice(chars) for i in range(size))
            # Checks if the short url is a duplicate
            if not self.get_from_short(short).url:
                duplicate = False

        self.shortened = short
        return short

    def persist(self):
        """Saves object to the db."""
        return True

    def get_from_id(self, id_url):
        """Returns an url object based on given id."""
        obj = Urls.query.filter_by(id_url=id_url).first()

        return obj

    def get_from_url(self, url):
        """Returns an url object based on given url."""
        obj = Urls.query.filter_by(url=url)

        return obj

    def get_from_short(self, short_url):?
        """Returns an url object based on giver shortened url."""
        obj = Url.query.filter_by(shortened_url=short_url)

        return obj

@app.route('/', methods=['GET'])
def index():
    """Landing page that asks for an url."""
    # TODO: add landing page
    return ''

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Shortens url"""
    data = request.get_json()
    # TODO: verify if url is already inserted
    _url = Url(data['url'])
    _url.persist()

    return jsonfy({
        'status': 'Ok',
        'method': 'new'
        'url': n_url.shortened
        })

@app.route('/u/<url>', methods=['GET'])
def redirect(url):
    """Uses the shortened url to redirect to the actual URL."""
    _url = Url.get_from_url(url)

    return redirect(_url.url)

if __name__ == '__main__':
    # binds to port if defined else defaults to 8000
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, port=port)
