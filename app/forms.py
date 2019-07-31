from tinyforms import FormDeserializer
from tinyforms.fields import Field, PasswordField, EmailField

class RegisterForm(FormDeserializer):
    username = Field('username', strict=True, max_length=32)
    password = PasswordField('password', strict=True)
    email = EmailField('email', strict=True, max_length=128)

class LoginForm(FormDeserializer):
    username = Field('username', strict=True, max_length=128)
    password = Field('password', strict=True)