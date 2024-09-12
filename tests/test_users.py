from models.user import User
from app import db
from conftest import MiddlewareConnexionTestClient
from starlette.testclient import TestClient
from app import connexion_app


def test_user_get(client: TestClient):
    test_user = User(name='Hash')
    db.session.add(test_user)
    db.session.flush()

    response = client.get(url='/users', headers={'X-HubSpot-Signature': 'some-signature'})

    print('56', response.json())


def test_user_creation(client: 'MiddlewareConnexionTestClient'):
    response = client.put(
        url='/users',
        json={'users': [{'id': 1, 'name': 'hash'}]},
        headers={'X-HubSpot-Signature': 'some-signature'})

    print(response.json())


def test_no_db():
    with connexion_app.test_client(connexion_app) as client:
        response = client.get('/without_db')
        print(response.json())


def test_user_get1(client: TestClient):
    with connexion_app.test_client(connexion_app) as client:
        test_user = User(name='Hash')
        db.session.add(test_user)
        db.session.flush()

        response = client.get(url='/users', headers={'X-HubSpot-Signature': 'some-signature'})

        print('56', response.json())
