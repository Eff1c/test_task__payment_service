import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SecretKey01'
    FLASKY_POST_PER_PAGE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SHOP_ID = 5
    PAYWAY = "advcash_rub"
    SHOP_CURRENCY = 840 # 840 - USD

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql+psycopg2://root:root@localhost/payment'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql+psycopg2://root:root@localhost/payment_service'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}