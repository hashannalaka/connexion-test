import traceback
from typing import Generator, Any
from unittest.mock import MagicMock
import pytest

from app import flask_app, connexion_app, db
from starlette.testclient import TestClient


class MiddlewareConnexionTestClient(TestClient):
    def __init__(self, app, *args, **kwargs):
        # Call the __init__ method of the base class
        super(MiddlewareConnexionTestClient, self).__init__(app, *args, **kwargs)  # pylint: disable=R1725

    def __enter__(self) -> 'MiddlewareConnexionTestClient':
        # Clean the SqlAlchemy session before each API request to make it seem that a new db transaction started.
        with flask_app.app_context():
            db.session.expunge_all()
            super().__enter__()
            return self

    class _RollbackException(Exception):
        pass

    # def _get_base_url(self) -> str:
    #     """Returns the base url based on path."""
    #     # Use integrations host URL as a default since we host redirects, and files in this subdomain.
    #     # For instance /dynamics/redirect/oneflow-app
    #     base_url =
    #     # The middleware only ever gets http requests because https is handled by a proxy.
    #     return base_url.replace('https', 'http')

    def _add_public_api_request_id_header(self, kwargs: dict) -> dict:
        """Add a request id header if it is not defined because that is what cloudfront does for all requests,
        so the integration tests behave the same by default."""
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        if ('x-amz-cf-id' or 'x-flow-trace-id') not in kwargs['headers']:
            kwargs['headers']['x-flow-trace-id'] = 'UnitTestRequestIDUnitTestRequestIDUnitTestRequestID'

        return kwargs

    def get(self, *args, **kwargs) -> Any:
        # Override this for other request methods as well
        with flask_app.app_context():
            db.session.expunge_all()
            try:
                with db.session.begin_nested():
                    # set imw base url
                    # base_url = kwargs.get('base_url') or self._get_base_url()
                    print(kwargs)
                    return super().get(*args, **kwargs)

            except self._RollbackException:
                pass

    def put(self, *args, **kwargs) -> Any:
        # Override this for other request methods as well
        with flask_app.app_context():
            db.session.expunge_all()
            try:
                with db.session.begin_nested():
                    # set imw base url
                    # base_url = kwargs.get('base_url') or self._get_base_url()
                    print(kwargs)
                    return super().put(*args, **kwargs)

            except self._RollbackException:
                pass


def middleware_starlette_test_client(app, **kwargs) -> MiddlewareConnexionTestClient:
    return MiddlewareConnexionTestClient(app, **kwargs)


connexion_app.test_client = middleware_starlette_test_client


@pytest.fixture(autouse=True, scope='session')
def client() -> Generator[MiddlewareConnexionTestClient, None, None]:
    # Ensure that the setup is done before any requests are made
    with connexion_app.test_client(connexion_app) as c:
        yield c


@pytest.fixture(autouse=True, scope='session')
def init_db() -> Generator:
    with flask_app.app_context():
        try:
            # Add database fixtures.
            db.drop_all()
            db.create_all()
            yield
            db.session.close()
            db.drop_all()
            return
        except Exception as e:
            # If we do not catch exceptions and rethrow a very serious one Nose will try to repeat the test forever
            traceback.print_exc()
            raise SystemExit from e


# Move this into a separate conftest.py file in the integration tests folder because it should only be run
# for tests involving the database, not for unit tests.
@pytest.fixture(autouse=True, scope='function')
def transact() -> Generator:
    with flask_app.app_context():
        rollback = db.session.rollback
        expunge_all = db.session.expunge_all
        commit = db.session.commit

        db.session.commit = MagicMock()
        db.session.rollback = MagicMock()
        db.session.remove = MagicMock()

        # Clear the session, and the transaction before every test.
        expunge_all()
        rollback()

        yield

        db.session.rollback = rollback
        db.session.expunge_all = expunge_all
        db.session.commit = commit
