from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db

agent = Blueprint('booking_agent',__name__)


@agent.route('/agent_profile', methods=['GET', 'POST'])


@agent.route('/view_commissions', methods=['GET', 'POST'])


@agent.route('/top_customers', methods=['GET', 'POST'])