from app import app, db
from app.models import User, Upload
from app.forms import RegisterForm, LoginForm

from tinyforms.fields import Field, EmailField, PasswordField

import unittest

from werkzeug.security import generate_password_hash, check_password_hash

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
        self.assertFalse(l.password == u.password_hash)
        self.assertTrue(check_password_hash(u.password_hash, l.password))

    def test_login_form(self):
        try:
            LoginForm({'username': 'test', 'password': 'hello world'})
        except:
            self.fail('LoginForm normal failure')

        self.assertRaises(Field.MissingFieldData, lambda: LoginForm({'username': 'test', 'password': None}))
        self.assertRaises(Field.MissingFieldData, lambda: LoginForm({'username': None, 'password': 'hello world'}))
        self.assertRaises(Field.FieldLengthExceeded, lambda: LoginForm({'username': 'a' * 129, 'password': 'hello world'}))
        try:
            LoginForm({'username': 'a' * 128, 'password': 'hello world'})
        except:
            self.fail('LoginForm username boundary length failed')

    def test_register_form(self):
        try:
            r = RegisterForm({'username': 'test', 'email': 'test@gmail.com', 'password': 'hello world'})
        except:
            self.fail('RegisterForm normal failure')
        else:
            try:
                u = User.create_from_form(r)
                db.session.add(u)
                db.session.commit()
            except:
                self.fail('Failed to create user from valid form data')
            else:
                self.assertTrue(r.password == 'hello world')

        self.assertRaises(Field.MissingFieldData, lambda: RegisterForm({'username': None, 'email': 'test@gmail.com', 'password': 'hello world'}))
        self.assertRaises(Field.MissingFieldData, lambda: RegisterForm({'username': 'test', 'email': None, 'password': 'hello world'}))
        self.assertRaises(Field.MissingFieldData, lambda: RegisterForm({'username': 'test', 'email': 'test@gmail.com', 'password': None}))
        
        self.assertRaises(Field.FieldLengthExceeded, lambda: RegisterForm({'username': 'a' * 33, 'email': 'test@gmail.com', 'password': 'hello world'}))
        self.assertRaises(Field.FieldLengthExceeded, lambda: RegisterForm({'username': 'test', 'email': 't' * 129, 'password': 'hello world'}))

        try:
            RegisterForm({'username': 't' * 32, 'email': 'test@gmail.com', 'password': 'test'})
        except:
            self.fail('RegisterForm username boundary length failed')
        try:
            RegisterForm({'username': 'test', 'email': '@' * 128, 'password': 'test'})
        except:
            self.fail('RegisterForm email boundary length failed')

        self.assertRaises(EmailField.InvalidEmail, lambda: RegisterForm({'username': 'test', 'email': 'testgmail.com', 'password': 'hello world'}))

if __name__ == '__main__':
    unittest.main(verbosity=2)