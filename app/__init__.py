from flask import Flask, render_template
from hashids import Hashids
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os

db = SQLAlchemy()
sess = Session()

def create_app() :
    app = Flask(__name__)
    
    app.config['SECRET_KEY']=os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    db.init_app(app)

    app.config['SESSION_TYPE']='sqlalchemy'
    app.config['SESSION_SQLALCHEMY']=db

    sess.init_app(app)

    from .main import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('page_not_found.html'), 404

    from . import models

    return app
