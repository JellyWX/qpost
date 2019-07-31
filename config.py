import os

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test key'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{usern}:{passwd}@localhost/newgram?charset=utf8mb4'.format(usern=, passwd=)

    SQLALCHEMY_TRACK_MODIFICATIONS = False