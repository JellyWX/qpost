from app import db
from app.forms import RegisterForm
from sqlalchemy.dialects.mysql import MEDIUMBLOB, INTEGER
from time import time as unix_time
from werkzeug.security import generate_password_hash, check_password_hash

followers_table = db.Table('following',
    db.Column('follower_id', INTEGER(unsigned=True), db.ForeignKey('users.id', ondelete='cascade')),
    db.Column('followed_id', INTEGER(unsigned=True), db.ForeignKey('users.id', ondelete='cascade'))
)

class Upload(db.Model):
    __tablename__ = 'uploads'

    id = db.Column(INTEGER(unsigned=True), unique=True, primary_key=True)

    description = db.Column(db.String(128), nullable=False, default='')
    upload_date = db.Column(INTEGER(unsigned=True), nullable=False, default=unix_time)

    image = db.Column(MEDIUMBLOB, nullable=False)

    uploader = db.Column(INTEGER(unsigned=True), db.ForeignKey('users.id', ondelete='cascade'))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(INTEGER(unsigned=True), unique=True, primary_key=True)

    username = db.Column(db.String(32), nullable=False)
    bio = db.Column(db.String(256), nullable=False, default='')
    email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(93), nullable=False)

    posts = db.relationship('Upload', backref='uploaded_by', foreign_keys=[Upload.uploader])

    followed = db.relationship(
        'User', secondary=followers_table,
        primaryjoin=(followers_table.c.follower_id == id),
        secondaryjoin=(followers_table.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create_from_form(cls, form: RegisterForm):
        return cls(username=form.username, email=form.email, password_hash=form.password)