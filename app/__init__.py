from flask import Flask


def create_app():
    app = Flask(__name__)

    from .auth.routes import auth
    from .routes.routes import routes
    from .preferences.routes import preferences

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(routes, url_prefix='/routes')
    app.register_blueprint(preferences, url_prefix='/preferences')

    return app
