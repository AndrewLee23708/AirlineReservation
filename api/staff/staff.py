from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db

### staff dashboard
staff = Blueprint('staff', __name__)

### dashboard 
### next to the dashboard will be a box containing all functionalities for all of these methods
@staff.route('/staff_dashboard')
def staff_dashboard():
    pass

@staff.route('/create_flight', methods=['GET', 'POST'])
def create_flight():
    pass

@staff.route('/change_flight_status', methods=['GET', 'POST'])
def change_flight_status():
    pass

@staff.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    pass

@staff.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
    pass

@staff.route('/view_booking_agents')
def view_booking_agents():
    pass

@staff.route('/view_frequent_customers')
def view_frequent_customers():
    pass

@staff.route('/view_reports', methods=['GET', 'POST'])
def view_reports():
    pass

@staff.route('/compare_revenue', methods=['GET', 'POST'])
def compare_revenue():
    pass

@staff.route('/view_top_destinations')
def view_top_destinations():
    pass

@staff.route('/grant_permissions', methods=['GET', 'POST'])
def grant_permissions():
    pass

@staff.route('/add_booking_agents', methods=['GET', 'POST'])
def add_booking_agents():
    pass
