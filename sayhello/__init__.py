# -*- coding: utf-8 -*-
"""

"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask('sayhello')
app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()

def create_app():
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    return app

from sayhello import views, errors, commands
