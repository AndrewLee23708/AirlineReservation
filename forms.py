from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email

'''

Define Forms Here


'''

################
# Authentication
################

# Customer Registration Form
class CustomerRegister(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=100)])
    building_number = StringField('Building Number', validators=[DataRequired(), Length(max=100)])
    street = StringField('Street', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    passport_number = StringField('Passport Number', validators=[DataRequired(), Length(max=30)])
    passport_expiration = DateField('Passport Expiration Date', validators=[DataRequired()])
    passport_country = StringField('Passport Country', validators=[DataRequired(), Length(max=100)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])

    submit = SubmitField('Customer Registeration')


# Agent Registration Form
class AgentRegister(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=100)])
    booking_agent_id = StringField('Booking Agent ID', validators=[DataRequired(), Length(max=20)])

    submit = SubmitField('Agent Registeration')


# Staff Registration Form
class StaffRegister(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=100)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=100)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    airline_name = StringField('Airline Name', validators=[DataRequired(), Length(max=20)])

    submit = SubmitField('Staff Registeration')


# Customer Login Form
class CustomerLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=100)])

    submit = SubmitField('Customer Login')


# Booking Agent Login Form
class AgentLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=100)])

    submit = SubmitField('Agent Login')


# Staff Login Form
class StaffLogin(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=100)])

    submit = SubmitField('Staff Login')


################
# General Forms
################

### Used for general flights, also for user-specific flights (ie agent search)
class SearchFlights(FlaskForm):
    departure_place = StringField('Departure Airport', validators=[])
    arrival_place = StringField('Arrival Airport', validators=[])
    end_time = DateField('Departure Time', validators=[])               #time field is not importing correctly
    start_time = DateField('Arrival Time', validators=[])               ##### THIS IS NOT DEP/APARTURE, this is the values Departure time can be between in.

    submit = SubmitField('Search')

# Same thing here, updated it so it's departure in between certain values
class SearchFlightStatus(FlaskForm):
    flight_number = StringField('Flight Number', validators=[])
    start_time = DateField('Departure Time', validators=[])
    end_time = DateField('Arrival Time', validators=[])

    submit = SubmitField('Search')


#for searching between time intervals for spending (Customer, Agent)
class TimeInterval(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')

    submit = SubmitField('Search')


#For customers and agents purchasing things
class Purchase(FlaskForm):
    customer = StringField('Customer_Email', validators=[])
    
    submit = SubmitField('Purchase')


################
# Staff-related Forms
################

#Airline search
class StaffSearchFlight(FlaskForm):
    flight_number = StringField('Flight_number', validators=[])
    start_time = DateField('Start Time', validators=[])
    end_time = DateField('End Time', validators=[])
    departure_airport = StringField('Departure Airport', validators=[])
    arrival_airport = StringField('Arrival Airport', validators=[])

    submit = SubmitField('Search')


### Admin forms
# We validate it using javascript form for arrival time, wtf-form is lacking some features
class CreateFlight(FlaskForm):
    flight_num = IntegerField('Flight Number', validators=[DataRequired()])
    departure_airport = StringField('Departure Airport', validators=[DataRequired(), Length(max=20)])
    departure_time = StringField('Departure Time ', validators=[DataRequired()])
    arrival_airport = StringField('Arrival Airport', validators=[DataRequired(), Length(max=20)])
    arrival_time = StringField('Arrival Time ', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    status = SelectField('Status', choices=['upcoming', 'in_progress', 'delayed'])
    airplane_id = IntegerField('Airplane ID', validators=[DataRequired()])
    submit = SubmitField('Create')


class AddAirplane(FlaskForm):
    airplane_id = IntegerField('Airplane ID', validators=[DataRequired()])
    seats = IntegerField('Seats', validators=[DataRequired()])

    submit = SubmitField('Add')


class AddAirport(FlaskForm):
    airport_name = StringField('Airport Name', validators=[DataRequired(), Length(max=20)])
    airport_city = StringField('Airport City', validators=[DataRequired(), Length(max=20)])

    submit = SubmitField('Add')


class GrantPermissions(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    permission = SelectField('Permission', choices=['Operator', 'Admin'])

    submit = SubmitField('Confirm')


class AddAgent(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=20)])

    submit = SubmitField('Add')


### Operator form
class ChangeFlightStatus(FlaskForm):

    flight_num = IntegerField('Flight Number', validators=[DataRequired()])
    status = SelectField('New Status', choices=['', 'upcoming', 'in_progress', 'delayed'])

    submit = SubmitField('Confirm')

