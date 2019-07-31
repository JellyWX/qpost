from app import db
from sqlalchemy.dialects.mysql import BLOB

class Upload(db.Model):
    __tablename__ = 'uploads'

    id = db.Column(db.Integer, unique=True, primary_key=True)

    description = db.Column(db.String(128), nullable=False)
    upload_date = db.Column(db.Integer, nullable=False)

    image = db.Column(BLOB, nullable=False)

    uploader = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, unique=True, primary_key=True)

    username = db.Column(db.String(32), nullable=False)
    bio = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(93), nullable=False)

    posts = db.relationship('Upload', backref='uploaded_by', foreign_key=[Upload.uploader])
