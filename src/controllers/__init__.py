from .url import url_blueprint


def register_blueprints(app):
    app.register_blueprint(url_blueprint, url_prefix='/')
