from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db

### staff dashboard
staff = Blueprint('staff', __name__)