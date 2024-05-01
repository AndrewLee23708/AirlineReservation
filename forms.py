from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email

'''

Define Forms Here


'''

################
# Authentication
################

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
    passport_expiration = DateField('Passport Expiration Date', validators=[DataRequired()])
    passport_country = StringField('Passport Country', validators=[DataRequired(), Length(max=50)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])

    submit = SubmitField('Customer Registeration')

# Agent Registration Form
class AgentRegister(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])
    booking_agent_id = StringField('Booking Agent ID', validators=[DataRequired(), Length(max=11)])

    submit = SubmitField('Agent Registeration')


# Staff Registration Form
class StaffRegister(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    airline_name = StringField('Airline Name', validators=[DataRequired(), Length(max=50)])

    submit = SubmitField('Staff Registeration')


# Customer Login Form
class CustomerLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])

    submit = SubmitField('Customer Login')


# Booking Agent Login Form
class AgentLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])

    submit = SubmitField('Agent Login')


# Staff Login Form
class StaffLogin(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])

    submit = SubmitField('Staff Login')


################
# General Forms
################

### Used for general flights, also for user-specific flights (ie agent or staff search
class PublicSearchUpcomingFlightForm(FlaskForm):
    departure_place = StringField('Departure Airport/City', validators=[])
    arrival_place = StringField('Arrival Airport/City', validators=[])
    departure_time = StringField('Departure Time', validators=[])               #time field is not importing correctly, use string field
    arrival_time = StringField('Arrival Time', validators=[])

    submit = SubmitField('Search')

class PublicSearchFlightStatusForm(FlaskForm):
    flight_number = StringField('Flight Number', validators=[])
    departure_time = StringField('Departure Time', validators=[])
    arrival_time = StringField('Arrival Time', validators=[])

    submit = SubmitField('Search')

#for searching between time intervals for spending (Customer, Agent)
class TimeInterval(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')

    submit = SubmitField('Search')

#For customers and agents purchasing things
class Purchase(FlaskForm):
    agent = StringField('Agent_ID', validators=[])
    customer = StringField('Customer_Email', validators=[])
    
    submit = SubmitField('Purchase')

################
# Customer-related Forms
################








################
# Agent-related Forms
################





################
# Staff-related Forms
################

#Airline search
class AirlineStaffSearchForm(FlaskForm):
    flight_number = StringField('Flight_number', validators=[])
    start_time = DateField('Start Time', validators=[])
    end_time = DateField('End Time', validators=[])
    departure_place = StringField('Departure Airport/City', validators=[])
    arrival_place = StringField('Arrival Airport/City', validators=[])

    submit = SubmitField('Search Flight')

### Admin forms
class CreateFlightForm(FlaskForm):
    flight_num = IntegerField('Flight Number', validators=[DataRequired()])
    departure_airport = StringField('Departure Airport', validators=[DataRequired(), Length(min=1, max=50)])
    departure_time = DateTimeField('Departure Time', validators=[DataRequired()])
    arrival_airport = StringField('Arrival Airport', validators=[DataRequired(), Length(min=1, max=50)])
    arrival_time = DateTimeField('Arrival Time', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    status = SelectField('Status', choices=['upcoming', 'in_progress', 'delayed'])
    airplane_id = IntegerField('Airplane ID', validators=[DataRequired()])

    submit = SubmitField('Create')


class AddAirplaneForm(FlaskForm):
    identifier = StringField('Identifier')
    airplane_id = IntegerField('Airplane ID', validators=[DataRequired()])
    seats = IntegerField('Seats', validators=[DataRequired()])

    submit = SubmitField('Add')


class AddAirportForm(FlaskForm):
    identifier = StringField('Identifier')
    airport_name = StringField('Airport Name', validators=[DataRequired(), Length(min=1, max=50)])
    airport_city = StringField('Airport City', validators=[DataRequired(), Length(min=1, max=50)])

    submit = SubmitField('Add')


class GrantNewPermissionForm(FlaskForm):
    identifier = StringField('Identifier')
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])
    permission = SelectField('Permission', choices=['Operator', 'Admin'])

    submit = SubmitField('Grant Permission')


class AddBookingAgentToAirlineForm(FlaskForm):
    identifier = StringField('Identifier')
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])

    submit = SubmitField('Add Booking Agent to Airline')


### Operator form
class ChangeFlightStatusForm(FlaskForm):
    identifier = StringField('Identifier')
    flight_num = IntegerField('Flight Number', validators=[DataRequired()])
    status = SelectField('New Status', choices=['', 'upcoming', 'in_progress', 'delayed'])

    submit = SubmitField('Submit Change')


class ViewTicketReportsForm(FlaskForm):
    identifier = StringField('Identifier')
    start_date = DateField('Start Date', validators=[])
    end_date = DateField('End Date', validators=[])

    submit = SubmitField('View Reports')


class ViewCommissionsForm(FlaskForm):
    identifier = StringField('Identifier')
    start_date = DateField('Start Date', validators=[])
    end_date = DateField('End Date', validators=[])

    submit = SubmitField('View Reports')


