from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db

# Default view will be total amount of money spent in the past year and a bar chart
# showing month wise money spent for last 6 months. He/she will also have option to specify a range of dates to
# view total amount of money spent within that range and a bar chart showing month wise money spent within
# that range. (Bar chart is optional, you can choose to represent the data anyway you like)

customer = Blueprint('customer',__name__)

# Default view will be total amount of money spent in the past year and a bar chart
# showing month wise money spent for last 6 months. He/she will also have option to specify a range of dates to
# view total amount of money spent within that range and a bar chart showing month wise money spent within
# that range. (Bar chart is optional, you can choose to represent the data anyway you like)

@customer.route('/customer_profile', methods=['GET', 'POST'])
def customer_profile():
    return render_template('customer_profile.html')