from flask import render_template, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from app.models import User, Upload
from app.forms import RegisterForm, LoginForm

from tinyforms.fields import Field, EmailField


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            form = LoginForm(request.form)
        except:
            flash('Invalid login credentials')

        else:
            user = User.query(((User.username == form.username) | (User.email == form.username)) & check_password_hash(User.password, form.password))
            if user.first() is None:
                flash('Invalid login credentials')

            else:
                return redirect( url_for('index') )

    return render_template('login.html')


@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            form = RegisterForm(request.form)
        except Field.FieldLengthExceeded:
            flash('Maximum username/email length exceeded')

        except Field.MissingFieldData:
            flash('Please complete all fields')

        except EmailField.InvalidEmail:
            flash('Email invalid')

        else:
            check_email_query = User.query(User.email == form.email)
            check_username_query = check_email_query.query(User.username == form.username)
            if check_email_query.first() is not None:
                flash('Email taken')

            elif check_username_query.first() is not None:
                flash('Username taken')

            else:
                user = User(username=form.username, password_hash=form.password, email=form.email)
                db.session.add(user)
                db.session.commit()

                return redirect( url_for('login') )

    return render_template('registration.html')


@app.route('/')
def index():
    return render_template('index.html')