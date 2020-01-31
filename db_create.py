## The db_create.py creates the database when run

from project import db

from project.models import PinGenerator

db.drop_all()

db.create_all()

db.session.commit()