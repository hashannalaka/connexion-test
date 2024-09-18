from typing import Generator
from unittest.mock import MagicMock

import pytest
from app import setup_application, setup_interfaces, db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import pytest

flask_app, connexion_app = setup_application(is_test=True)


@pytest.fixture(scope='session')
def client():
    """Create and configure a new app instance for each test session."""

    setup_interfaces(connexion_app)
    with connexion_app.test_client() as client:
        with flask_app.app_context():
            db.create_all()
            yield client
            db.drop_all()
            return


@pytest.fixture(scope='session')
def init_db():
    with flask_app.app_context():
        db.create_all()  # Create tables for the test database
        print('db created')
        yield db  # Provide the database session for tests
        db.drop_all()  # Tear down the database after tests
        return


@pytest.fixture(autouse=True, scope='function')
def session():
    with flask_app.app_context():
        # rollback = db.session.rollback
        # expunge_all = db.session.expunge_all
        # commit = db.session.commit
        #
        # db.session.commit = MagicMock()
        # db.session.rollback = MagicMock()
        # db.session.remove = MagicMock()
        #
        # # Clear the session, and the transaction before every test.
        # expunge_all()
        # rollback()
        #
        # yield
        #
        # db.session.rollback = rollback
        # db.session.expunge_all = expunge_all
        # db.session.commit = commit
        db.session.expunge_all()
        db.session.rollback()
        db.session.begin(subtransactions=True)
        yield
        db.session.rollback()
