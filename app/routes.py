from flask import render_template, request, flash, abort, redirect, url_for, session, send_file, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.models import User, Upload
from app.forms import RegisterForm, LoginForm

from tinyforms.fields import Field, EmailField

from bootstrap_alert import Warning, Danger 

from wand.image import Image

import typing
import io


def logged_in_as() -> typing.Optional[User]:
    uid = session.get('user', None)

    if uid is not None:
        return User.query.get(uid)

    else:
        return None


@app.route('/create_post/', methods=['POST'])
def create_post():
    user: typing.Optional[User] = logged_in_as()

    if user is None:
        return abort(403)

    else:
        try:
            f = request.files['image']
            description = request.form['description']
        except KeyError:
            return abort(400)

        else:
            try:
                with Image(file=f.stream) as img:
                    img.format = 'jpeg'
                    img.transform('', '{0}x{0}>'.format(app.config['MAX_IMAGE_SIZE']))

                    upload = Upload(image=img.make_blob(), uploader=user.id, description=description)
                    db.session.add(upload)
                    db.session.commit()
            except:
                Warning('Invalid image')

            return redirect( url_for('index') )


@app.route('/post/<int:id>/img')
def view_post_image(id: int):
    img = Upload.query.get(id)

    if img is None:
        return abort(404)

    else:
        return send_file(io.BytesIO(img.image), mimetype='image/jpeg', attachment_filename='{}.jpeg'.format(id))


@app.route('/fetch_feed/<int:page>')
def fetch_feed(page: int):
    user: typing.Optional[User] = logged_in_as()

    if user is None:
        return abort(401)

    else:
        return jsonify({x: d for x, d in map(lambda u: (u.id, u.description), user.fetch_feed())})


@app.route('/toggle_follow/<int:id>/')
def toggle_follow(id: int):
    user_a = logged_in_as()
    user_b = User.query.get(id)

    if user_a is None:
        return abort(403)

    elif user_b is None:
        return abort(404)

    else:
        user_a.toggle_follow(user_b)
        db.session.commit()

    return redirect( url_for('view_user', id=id) )


@app.route('/user/<int:id>/')
def view_user(id: int):
    current_user = logged_in_as()
    viewing = User.query.get(id)

    if viewing is None:
        return abort(404)

    else:
        return render_template('profile.html',
            logged_in = current_user is not None,
            user = current_user,
            profile = viewing,
            title = viewing.username
        )


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            form = LoginForm(request.form)
        except:
            Danger('Invalid login credentials')

        else:
            user = User.query.filter((User.username == form.username) | (User.email == form.username))
            if user.first() is None:
                Danger('Invalid login credentials')

            else:
                user = user.first()
                if check_password_hash(user.password_hash, form.password):
                    session['user'] = user.id
                    return redirect( url_for('index') )
                else:
                    Danger('Invalid login credentials')

    return render_template('login.html',
        logged_in = logged_in_as() is not None,
        user = logged_in_as(),
        title = 'Login',
    )


@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            form = RegisterForm(request.form)
        except Field.FieldLengthExceeded:
            Danger('Maximum username/email length exceeded')

        except Field.MissingFieldData:
            Danger('Please complete all fields')

        except EmailField.InvalidEmail:
            Danger('Email invalid')

        else:
            check_email_query = User.query.filter(User.email == form.email)
            check_username_query = User.query.filter(User.username == form.username)
            if check_email_query.first() is not None:
                Info('Email taken')

            elif check_username_query.first() is not None:
                Info('Username taken')

            else:
                user = User.create_from_form(form)
                db.session.add(user)
                db.session.commit()

                session['user'] = user.id

                return redirect( url_for('index') )

    return render_template('registration.html',
        logged_in = logged_in_as() is not None,
        user = logged_in_as(),
        title = 'Register'
    )

@app.route('/anonymize/')
def anonymize():
    session.pop('user')

    return redirect( url_for('index') )


@app.route('/')
def index():
    return render_template('index.html',
        logged_in = logged_in_as() is not None,
        user = logged_in_as(),
        title = 'Home'
    )