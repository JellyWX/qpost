from flask import render_template, request, flash, abort, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.models import User, Upload
from app.forms import RegisterForm, LoginForm

from tinyforms.fields import Field, EmailField

from wand.image import Image

@app.route('/create_post/', methods=['POST'])
def create_post():
    try:
        f = request.files['image']
    except KeyError:
        return abort(400)

    else:
        try:
            with Image(file=f.stream) as img:
                img.format = 'jpeg'
                img.transform('', '{0}x{0}>'.format(app.config['MAX_IMAGE_SIZE']))

                upload = Upload(image=img.make_blob(), uploader=session.get('user'))
                db.session.add(upload)
                db.session.commit()
        except:
            flash('Invalid image')

        return redirect( url_for('index') )


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            form = LoginForm(request.form)
        except:
            print('e')
            flash('Invalid login credentials')

        else:
            user = User.query.filter((User.username == form.username) | (User.email == form.username))
            if user.first() is None:
                flash('Invalid login credentials')

            else:
                user = user.first()
                if check_password_hash(user.password_hash, form.password):
                    session['user'] = user.id
                    return redirect( url_for('index') )
                else:
                    flash('Invalid login credentials')

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
            check_email_query = User.query.filter(User.email == form.email)
            check_username_query = User.query.filter(User.username == form.username)
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