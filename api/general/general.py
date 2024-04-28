from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db

general = Blueprint('general', __name__)

@general.route('/')
@general.route('/home')
def home():

    return render_template('home.html')


@general.route('/flight_status')
def flight_status():
    #### Add stuff

    pass

### Customers and Agents can buy tickets here, you will need to add functionalities here that manage this
@general.route('/view_flights')
def view_flights():
    #### Add stuff
    pass

### Purchase ticket for customer and agent
### Check if session is customer or agent, if no one logged in, send them to login page.
@general.route('/purchase/<flight_num>', methods=['GET', 'POST'])


### Every user has thier own profile, this endpoint brings them to their respective profile.
@general.route('/profile')
def profile():
    user_type = session.get('type')       

    if user_type == 'customer':
        return redirect(url_for('customer.customer_profile'))
    elif user_type == 'agent':
        return redirect(url_for('agent.agent_profile'))
    elif user_type == 'staff':
        return redirect(url_for('staff.staff_profile'))
    else:
        flash('Please log in.', 'warning')
        return redirect(url_for('authentication.login'))
    


### we don't need this but don't delete, I will implement this directly into the users dashboard
### leave this here so you know this functionality will not be implemented.
# @general.route('view_my_flights')  XXXXXXx
    #bare bones, but every user can see their flights specific to their needs
    # if user_type == 'customer':
    #     return redirect(url_for('customer.customer_profile'))
    # elif user_type == 'agent':
    #     return redirect(url_for('agent.agent_profile'))
    # elif user_type == 'staff':
    #     return redirect(url_for('staff.staff_profile'))
    # else:
    #     return redirect(url_for('general.home'))

