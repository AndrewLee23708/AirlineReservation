from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db

general = Blueprint('general', __name__)

@general.route('/')
def home():
    return render_template('home.html')


@general.route('/flight_status')
def flight_status():
    #### Add stuff

    return 10

### Customers and Agents can buy tickets here, you will need to add functionalities here that manage this
@general.route('/view_flights')
def view_flights():
    #### Add stuff
    return 10

### Purchase ticket for customer and agent
### Check if session is customer or agent, if no one logged in, send them to login page.
@general.route('/purchase/<flight_num>', methods=['GET', 'POST'])



@general.route('/profile')
def profile():
    ### Barebomes, but based on session type, route to other endpoints, add stuff
    user_type = session.get('user_type')

    if user_type == 'customer':
        return redirect(url_for('customer.customer_profile'))
    elif user_type == 'agent':
        return redirect(url_for('agent.agent_profile'))
    elif user_type == 'staff':
        return redirect(url_for('staff.staff_profile'))
    else:
        return redirect(url_for('auth.login'))
    

# @general.route('view_my_flights')
    #bare bones, but every user can see their flights specific to their needs
    # if user_type == 'customer':
    #     return redirect(url_for('customer.customer_profile'))
    # elif user_type == 'agent':
    #     return redirect(url_for('agent.agent_profile'))
    # elif user_type == 'staff':
    #     return redirect(url_for('staff.staff_profile'))
    # else:
    #     return redirect(url_for('general.home'))




# # Optionally you mayinclude a wayfor the user to specify a
# # range of dates, specify destination and/or source airport name or city name etc.
# # Check the session object to see what type of user is checking for flights
