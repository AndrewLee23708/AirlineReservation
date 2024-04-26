from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length, Email

#####
# Define Forms Here
#####

# Customer Registration Form
class CustomerRegister(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    name = StringField('Full Name', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])
    building_number = StringField('Building Number', validators=[DataRequired(), Length(max=30)])
    street = StringField('Street', validators=[DataRequired(), Length(max=30)])
    city = StringField('City', validators=[DataRequired(), Length(max=30)])
    state = StringField('State', validators=[DataRequired(), Length(max=30)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=11)])
    passport_number = StringField('Passport Number', validators=[DataRequired(), Length(max=30)])
    passport_expiration = StringField('Passport Expiration Date', validators=[DataRequired()])
    passport_country = StringField('Passport Country', validators=[DataRequired(), Length(max=50)])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])

    #submit

# Staff Registration Form
class StaffRegister(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])
    airline_name = StringField('Airline Name', validators=[DataRequired(), Length(max=50)])

# Agent Registration Form
class AgentRegister(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])
    booking_agent_id = StringField('Booking Agent ID', validators=[DataRequired(), Length(max=11)])

# Customer Login Form
class CustomerLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])

# Booking Agent Login Form
class AgentLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])

# Staff Login Form
class StaffLogin(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])


