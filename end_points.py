import logging
from models.user import User
from flask import jsonify, Response
from app import flask_app, db


def get_users():
    # Query all users
    logging.debug("get_users function called")
    # with flask_app.app_context():
    users = User.query.all()
    # Return users as JSON
    return jsonify([{'id': user.id, 'name': user.name} for user in users])


def put_users(body: dict) -> Response:
    print(body)

    for user in body.get("users"):
        new_user = User(name=user['name'])
        db.session.add(new_user)

    db.session.commit()
    # Return users as JSON
    return jsonify({})
