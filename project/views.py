from flask import render_template, request, flash, url_for, redirect, session
from project import app, db, api
from project.models import PinGenerator
from flask_restful import Resource, Api
from sqlalchemy import exc
from functools import wraps
from datetime import datetime
import uuid



def random_pin(length):
    stringLength = length
    randomString = str(uuid.uuid4().int) # get a random string in a UUID fromat
    randomString  = randomString[0:stringLength] # trim to stringLength.
    return randomString


class Generate(Resource):
    def get(self):
        try:
            #generate a random uuid 15 digits
            epin = random_pin(15)
            #generate a random uuid 25 digits
            eserial_no = random_pin(25)
            #make an object of the database class
            new_pin = PinGenerator(pin = epin, serial_no = eserial_no)

            #compare the generated digits with database, if any exists, generate again
            if PinGenerator.query.get(epin) or PinGenerator.query.filter_by(serial_no= eserial_no).first():
                db.session.rollback()
                return redirect(url_for('generate'))
            # if they don't exist in db, add to database and return the generated digits
            db.session.add(new_pin)
            db.session.commit()
            return {"pin": epin, "s/n": eserial_no}, 200
        except exc.IntegrityError: #for any other exception, flag error message
            db.session.rollback()
            return {"message": " Oops! try again later"}, 404

api.add_resource(Generate, '/generate')  


class Validate(Resource):
    def post(self):
        #get serial_no and pin from user, and convert to string
        request_data = request.get_json()
        eserial_no = str(request_data['s/n'])
        epin = str(request_data['pin'])
        #check if both serial_no and pin exist in the database
        chkpin = PinGenerator.query.filter_by(pin=epin, serial_no=eserial_no).first()
        if chkpin: # if they exist, return 1 connoting valid
            return {'message':"1"},200
        else: # if they don't exist, return 0 connoting invalid
            return {'message':"0"}, 200

api.add_resource(Validate, '/validate')


class Home(Resource):
    def get(self):
        return {
            'message': '''Welcome, my name is Emeka Nnoruka. The purpose of this project is to build two(2) API. This first endpoint ["/generate"] will return a PIN and a SERIAL_NO, while the second endpoint ["/validate/serial_no/pin"] will validate if the SERIAL_NO and PIN supplied is VALID [1] or NOT [0].Feel free to consume the APIs.'''}
api.add_resource(Home, '/')