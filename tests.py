from app import app, db
from app.models import User, Upload
from app.forms import RegisterForm, LoginForm

from tinyforms.fields import Field, EmailField, PasswordField

import unittest

class LoginCase(unittest.TestCase):
    def setUp(self):
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{usern}@localhost/newgram_test?charset=utf8mb4'.format(usern='jude', passwd=None)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        u = User(username='test', email='test@mail.com', password_hash=generate_password_hash('hello world'))

        l = LoginForm({'username': 'test', 'password': 'hello world'})

        self.assertTrue(l.username == u.username)
        self.assertTrue(l.password == u.password)
        self.assertFalse(l.password == 'dlrow olleh')

    def test_login_form(self):
        self.assertRaise(Field.MissingFieldData, LoginForm({'username': 'test', 'password': None}))
        self.assertRaise(Field.MissingFieldData, LoginForm({'username': None, 'password': 'hello world'}))
        self.assertRaise(Field.FieldLengthExceeded, LoginForm({'username': 'a' * 129, 'password': 'hello world'}))
        try:
            LoginForm({'username': 'a' * 128, 'password': 'hello world'})
        except:
            self.fail('LoginForm username length failed')
