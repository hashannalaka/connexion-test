from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_POOL_SIZE = 6
SQLALCHEMY_POOL_RECYCLE = 14400

# Maximum execution time for read only select statements in milliseconds.
MAX_EXECUTION_TIME = 60 * 1000
SQLALCHEMY_ENGINE_OPTIONS = {
    'connect_args': {'init_command': f'SET SESSION MAX_EXECUTION_TIME={MAX_EXECUTION_TIME}'},
    'pool_pre_ping': True,
    'pool_size': SQLALCHEMY_POOL_SIZE,
    'pool_recycle': SQLALCHEMY_POOL_RECYCLE,
}

db = SQLAlchemy(engine_options=SQLALCHEMY_ENGINE_OPTIONS)

from models.user import User
from models.account import Account