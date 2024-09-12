class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskuser:flaskpassword@localhost:3306/flask_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://testuser:testpassword@localhost:3307/flask_test_db'
