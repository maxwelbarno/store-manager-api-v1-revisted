from flask import Flask
from instance.config import app_config
from .api import v1_blueprint
from flask_jwt_extended import JWTManager
from functools import wraps
from app.api.models import revoked_tokens


def create_app(config_name):
    """
        This function wraps the creation of a new Flask object
        and returns it after it's loaded up with configuration settings 
        using 'app.config' and connected to DB using 'db.init_app(app)'
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    jwt = JWTManager(app)

    # create user claims
    @jwt.user_claims_loader
    def add_claims_to_access_token(identity):
        return {
            'is_admin': identity
        }

    # check revoked tokens from revoked_tokens list
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in revoked_tokens

    # register blueprint
    app.register_blueprint(v1_blueprint)

    return app
