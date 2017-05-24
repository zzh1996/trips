#!/usr/bin/env python3
# encoding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://trips:trips@localhost/trips?charset=utf8'
app.config['SECRET_KEY'] = 'key'
db = SQLAlchemy(app)
Bootstrap(app)

from app.views import *
