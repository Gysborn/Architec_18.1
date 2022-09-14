class Config:
    DEBUG = True
    SECRET = 'test'
    SQLALCHEMY_DATABASE_URI = "sqlite:///temporary.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False