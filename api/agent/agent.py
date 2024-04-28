from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt

import mysql.connector

def setup_db():
    connection = mysql.connector.connect(host="localhost", port="3306", 
                            user = "root", password ="",
                            database = "airticket_system")
    return connection


agent = Blueprint('booking_agent',__name__)


@agent.route('/agent_profile', methods=['GET', 'POST'])
def agent_profile():
    pass

@agent.route('/view_commissions', methods=['GET', 'POST'])
def view_commissions():
    pass

@agent.route('/top_customers', methods=['GET', 'POST'])
def top_customer():
    pass