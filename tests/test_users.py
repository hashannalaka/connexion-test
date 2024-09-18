from config import TestConfig
from models.user import User
from app import db
from conftest import client
# from starlette.testclient import TestClient

# connexion_app.test_client = middleware_starlette_test_client
# def test_user_get(client: TestClient):
#     test_user = User(name='Hash')
#     db.session.add(test_user)
#     db.session.flush()
#
#     response = client.get(url='/users', headers={'X-HubSpot-Signature': 'some-signature'})
#
#     print('56', response.json())
#
#
# def test_user_creation(client: 'MiddlewareConnexionTestClient'):
#     response = client.put(
#         url='/users',
#         json={'users': [{'id': 1, 'name': 'hash'}]},
#         headers={'X-HubSpot-Signature': 'some-signature'})
#
#     print(response.json())
#
#
# def test_no_db():
#     with connexion_app.test_client(connexion_app) as client:
#         response = client.get('/without_db')
#         print(response.json())
#
#
# def test_user_get1(client: TestClient):
#     with connexion_app.test_client(connexion_app) as client:
#         test_user = User(name='Hash')
#         db.session.add(test_user)
#         db.session.flush()
#
#         response = client.get(url='/users', headers={'X-HubSpot-Signature': 'some-signature'})
#
#         print('56', response.json())


def test_user_get_new_db(client):
    # with connexion_app.test_client() as client:
    # print(connexion_app.app.config["SQLALCHEMY_DATABASE_URI"])
    test_user = User(name='paul')
    db.session.add(test_user)
    db.session.commit()

    response = client.get(
        url='/users', headers={'X-HubSpot-Signature': 'some-signature'}
    )

    print(response.json())


def test_user_creation(client):
    # with connexion_app.test_client() as client:

    response = client.put(
        url='/users',
        json={
            'users': [
                {'id': 1, 'name': 'hash'},
                {'id': 1, 'name': 'alex'},
            ]
        },
        headers={'X-HubSpot-Signature': 'some-signature'},
    )

    print(response.json())
    users = User.query.all()
    print([user.name for user in users])


def test_without_db(client):
    # with connexion_app.test_client() as client:
    response = client.get('/without_db')

    print(response.json())
