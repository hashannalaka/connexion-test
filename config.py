class Config:
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://flaskuser:flaskpassword@localhost:3352/connexion_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://testuser:testpassword@localhost:3353/connexion_test_db'
    )
