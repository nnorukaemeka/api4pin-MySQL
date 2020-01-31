##initial all library and modules

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_uuid import FlaskUUID
from flask_restful import Resource, Api
import uuid

#Instanciate the flask app
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
FlaskUUID(app)
api = Api(app)

from . import views

