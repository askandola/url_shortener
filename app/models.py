from . import db

class User(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    urls = db.relationship('Url', cascade='all, delete', backref='user', lazy=True)

class Url(db.Model) :
    id = db.Column(db.Integer, primary_key=True, unique=True)
    slug = db.Column(db.Text, nullable=False, default="#")
    original_url = db.Column(db.Text, nullable=False)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    created = db.Column(db.DateTime, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id))
