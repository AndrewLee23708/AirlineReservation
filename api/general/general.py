from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db

general = Blueprint('general', __name__)

@general.route('/')
def home():
    return render_template('home.html')


# # Optionally you mayinclude a wayfor the user to specify a
# # range of dates, specify destination and/or source airport name or city name etc.
# # Check the session object to see what type of user is checking for flights

# @general_blueprint.route('/viewFlights')


# other endpoints multiple users would have access too


