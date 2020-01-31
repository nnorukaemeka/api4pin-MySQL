from project import db
from datetime import date, time

class PinGenerator(db.Model):
    
    __tablename__ = 'pinGenerator'

    pin = db.Column(db.String(15), primary_key=True, nullable=False, autoincrement=False, unique =True)
    serial_no = db.Column(db.String(25), nullable=False, unique =True)


    def __init__(self, pin, serial_no):
        self.pin = pin
        self.serial_no = serial_no


    def __repr__(self):
        return '<title {}'.format(self.serial_no)