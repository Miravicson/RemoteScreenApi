import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from dotenv import load_dotenv, find_dotenv
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager


load_dotenv(find_dotenv())

# instantiate db object

db = SQLAlchemy()

migrate = Migrate()

bootstrap = Bootstrap()
moment = Moment()

ma = Marshmallow()

jwt = JWTManager()


config = os.getenv('APP_SETTINGS')


def create_app(config_class=config):
    ''' factory function for creating the flask application instance. Accepts a configuration class and returns an instance of the flask application '''
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    moment.init_app(app)
    ma.init_app(app)
    CORS(app)
    jwt.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    from app.auth import RevokedTokenModel

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)

    @app.route('/')
    def index():
        return jsonify({
            "message": "Home for the RemoteScreen API"
        })

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app


from app import models
