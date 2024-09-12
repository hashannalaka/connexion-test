from models import db


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    account_city = db.Column(db.String(80), nullable=False)

    def __init__(self, name: str, account_city: str) -> None:
        self.name = name
        self.account_city = account_city
