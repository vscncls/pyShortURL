from flask import Blueprint, request, jsonify
from src.models.urls import Url
from src.services.get_url import get_random_url
from src.database import db


url_blueprint = Blueprint('url', __name__)


@url_blueprint.route('/', methods=['GET'])
def get_url():
    required = ['shortenedUrl']
    missing = []
    for i in required:
        if i not in request.json:
            missing.append(i)
    if missing:
        return jsonify({
            "isError": True,
            "message": f"missing params {missing}"
        })

    url = Url().query.filter_by(
        shortenend_url=request.json['shortenedUrl']).first()
    if not url:
        return jsonify({
            "isError": True,
            "message": "URL not found"
        })

    return jsonify({
        'isError': False,
        'url': url['url'],
        'shortenedUrl': request.json['shortenedUrl']
    })


@url_blueprint.route('/random', methods=['POST'])
def random_url_post():
    required = ['url']
    missing = []
    for i in required:
        if i not in request.json:
            missing.append(i)
    if missing:
        return jsonify({
            "isError": True,
            "message": f"missing params {missing}"
        })

    url = Url(
        url=request.json['url'],
        url_type=1,
        shortenend_url=get_random_url()
    )

    # If url is already in db, use that one instead
    db_url = Url.query.filter_by(url=request.json['url'], url_type=1).first()
    url = db_url or url

    # Only checks if shortened url is not duplicate if its a new URL
    while not db_url:
        q = Url.query.filter_by(
            shortenend_url=url.shortenend_url).first()
        if not q:
            break
        url.shortenend_url = get_random_url()
    print('ijkgeriojg', url)
    db.session.add(url)
    db.session.commit()

    return jsonify({
        'isError': False,
        'url': request.json['url'],
        'shortenedUrl': url.shortenend_url
    })


@url_blueprint.route('/custom', methods=['POST'])
def custom_url_post():
    required = ['url', 'customUrl']
    missing = []
    for i in required:
        if i not in request.json:
            missing.append(i)
    if missing:
        return jsonify({
            "isError": True,
            "message": f"missing params {missing}"
        })
    q = Url.query.filter_by(
        shortenend_url=request.json['customUrl']).first()
    if q:
        return jsonify({
            "isError": True,
            "message": "CustomURL already taken."
        })

    url = Url(
        url=request.json['url'],
        url_type=2,
        shortenend_url=request.json['customUrl']
    )

    db.session.add(url)
    db.session.commit()

    return jsonify({
        'isError': False,
        'url': request.json['url'],
        'customUrl': url.shortenend_url
    })
