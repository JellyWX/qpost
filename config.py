import os

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test key'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{usern}@localhost/newgram?charset=utf8mb4'.format(usern='jude', passwd=None)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_IMAGE_SIZE = 500
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024