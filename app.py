import connexion
from connexion import FlaskApp
from request_hooks import add_missing_slash
from config import Config, TestConfig
from models import db


def setup_application(is_test=False):
    _connexion_app = connexion.App(__name__, specification_dir='interface/')
    _flask_app = _connexion_app.app

    _flask_app.config['SQLALCHEMY_DATABASE_URI'] = (
        Config.SQLALCHEMY_DATABASE_URI
        if not is_test
        else TestConfig.SQLALCHEMY_DATABASE_URI
    )
    _flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = (
        Config.SQLALCHEMY_TRACK_MODIFICATIONS
    )

    _flask_app.before_request(add_missing_slash)

    _db = db.init_app(_flask_app)

    return _flask_app, _connexion_app


def setup_interfaces(connexion_flask_app: 'FlaskApp') -> None:

    connexion_flask_app.app.url_map.strict_slashes = False

    connexion_flask_app.add_api(
        'openapi.yml',
        strict_validation=True,
        validate_responses=True,
    )


flask_app, connexion_app = setup_application()
setup_interfaces(connexion_flask_app=connexion_app)
