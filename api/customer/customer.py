from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db

# Default view will be total amount of money spent in the past year and a bar chart
# showing month wise money spent for last 6 months. He/she will also have option to specify a range of dates to
# view total amount of money spent within that range and a bar chart showing month wise money spent within
# that range. (Bar chart is optional, you can choose to represent the data anyway you like)

customer = Blueprint('customer',__name__)


@customer.route('/customer_profile', methods=['GET', 'POST'])
def customer_profile():
    # Fetch general profile data
    profile_data = get_customer_profile_data()

    # Fetch spending data
    spending_data = get_customer_spending_data()

    # Fetch own flights data
    flights_data = get_customer_own_flights_data()

    return render_template('customer_profile.html', 
                           profile=profile_data, 
                           spending=spending_data, 
                           flights=flights_data)


# Default view will be total amount of money spent in the past year and a bar chart
# showing month wise money spent for last 6 months. He/she will also have option to specify a range of dates to
# view total amount of money spent within that range and a bar chart showing month wise money spent within
# that range. (Bar chart is optional, you can choose to represent the data anyway you like)
@customer.route('/customer_profile/spending')


@customer.route('/customer_profile/own_flights')

