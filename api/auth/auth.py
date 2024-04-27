from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db

auth = Blueprint('authentication',__name__)       #html will reference this as authentication
bcrypt = Bcrypt() 

### NOTE: To access this endpoint, you have to have auth/[whatever endpoint]
## Example: http://127.0.0.1:5000/auth/login 

@auth.route('/login', methods= ['GET'])
def login():
    return render_template('login.html')


@auth.route('/login_customer', methods=['GET', 'POST'])
def login_customer():

    form = forms.CustomerLogin()

    # This part checks if it's a POST request and validates the form
    if request.method == 'POST' and form.validate_on_submit():         #validate on submit checks if our inputs are are fitted correctly

        #query
        cur = setup_db.cursor()
        query = "SELECT * FROM customer WHERE email = '{}'"    #first bracket mapped to email

        cur.execute(query.format(form.email.data))     #query for email
        data = cur.fetchone()
        cur.close()

        #check if right password, set session
        if data and bcrypt.check_password_hash(data['password'], form.password.data):       #hash password
            session['email'] = form.email.data
            session['type'] = 'customer'
            
            return redirect(url_for('general.home'))  # Bring back to homepage         
        
        else:  # handle the case when the email does not exist
            flash('Email or Password is incorrect', 'danger')

    # This part is executed on GET request, which is responsible for retrieving the form page to display to the user
    return render_template('login_customer.html', form = form)       #we don't need to render template then???



@auth.route('/login_agent', methods=['GET', 'POST'])
def login_agent():
    form = forms.AgentLogin()

    if form.validate_on_submit():

        cur = setup_db.cursor()
        query = "SELECT * FROM booking_agent WHERE email = %s"

        cur.execute(query, (form.email.data,))
        agent = cur.fetchone()
        cur.close()

        if agent and bcrypt.check_password_hash(agent['password'], form.password.data):
            session['email'] = form.email.data
            session['type'] = 'agent'
            session['agent_id'] = agent['booking_agent_id']
            return redirect(url_for('home'))
        
        else:
            flash('Email or Password is incorrect', 'danger')

    return render_template('login_agent.html', form=form)

    

@auth.route('/login_airline_staff', methods=['GET', 'POST'])
def login_airline_staff():
    form = forms.StaffLogin()

    if form.validate_on_submit():
        cur = setup_db().cursor()  # Ensure the database connection setup is callable
        query = "SELECT * FROM airline_staff WHERE username = %s"
        cur.execute(query, (form.username.data,))
        staff = cur.fetchone()

        if staff and bcrypt.check_password_hash(staff['password'], form.password.data):
            session['username'] = form.username.data
            session['type'] = 'airline_staff'

            # Retrieve permission types and airline name
            query = "SELECT permission_type FROM permission WHERE username = %s"
            cur.execute(query, (form.username.data,))
            permissions = cur.fetchall()

            # Assign a list of permission types to the session
            session['permissions'] = [permission['permission_type'] for permission in permissions]

            query = "SELECT airline_name FROM airline_staff WHERE username = %s"
            cur.execute(query, (form.username.data,))
            airline = cur.fetchone()

            session['airline'] = airline['airline_name']
            cur.close()
            
            flash(f'You have successfully logged in as {form.username.data}!', 'success')
            return redirect(url_for('home'))
        
        else:
            flash('Username or Password is incorrect', 'danger')

    return render_template('login_airline_staff.html', form=form)



@auth.route('/register')
def register():
    return render_template('register.html')



@auth.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    form = forms.CustomerRegister()

    if form.validate_on_submit():    # follow validation rules

        # Use parameterized queries to prevent SQL injection
        conn = setup_db
        cur = conn.cursor()

        #Check for duplicate emails
        query_find_email = "SELECT email FROM customer WHERE email = %s"
        cur.execute(query_find_email, (form.email.data,))
        dup_emails = cur.fetchall()
        
        #first check for duplicate emails
        if dup_emails:
            flash('Email already belongs to an account!', 'danger')                                   ##double check this

        else:
            ### We create hashed_password
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            # Parameterized queries for the insert operation, pass them as a tuple to defend against SQL injections
            query = """
            INSERT INTO customer (
                email, name, password, building_number, street, city, state, 
                phone_number, passport_number, passport_expiration, passport_country, date_of_birth
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (
                form.email.data, form.name.data, hashed_password, 
                form.building_number.data, form.street.data, form.city.data, 
                form.state.data, form.phone_number.data, form.passport_number.data, 
                form.passport_expiration.data, form.passport_country.data, form.date_of_birth.data
            ))
            conn.commit()
            cur.close()

            #return to login page
            flash(f'Hello {form.name.data}!', 'success')
            
            return redirect(url_for('login_customer'))
        
    return render_template('register_customer.html', form=form)



@auth.route('/register_agent', methods=['GET', 'POST'])
def register_agent():
    form = forms.AgentRegister()

    if form.validate_on_submit():
        email = form.email.data
        booking_agent_id = form.booking_agent_id.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        conn = setup_db()
        cur = conn.cursor()
        
        # Check for duplicate email or agent ID using parameterized queries
        cur.execute("SELECT email FROM booking_agent WHERE email = %s OR booking_agent_id = %s", (email, booking_agent_id))
        if cur.fetchone():
            flash('Email or Agent ID already exists!', 'danger')
            
        else:
            cur.execute("INSERT INTO booking_agent (email, password, booking_agent_id) VALUES (%s, %s, %s)",
                        (email, hashed_password, booking_agent_id))
            conn.commit()

            return redirect(url_for('auth.login'))      #redirect to this endpoint
        cur.close()
    return render_template('login.html', form=form, tab='agent')     #bring to agent login tab



@auth.route('/register_airline_staff', methods=['GET', 'POST'])
def register_airline_staff():

    form = forms.StaffRegister()

    if form.validate_on_submit():
        username = form.username.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        first_name = form.first_name.data
        last_name = form.last_name.data
        date_of_birth = form.date_of_birth.data
        airline_name = form.airline_name.data

        conn = setup_db()
        cur = conn.cursor()
        
        # Check for duplicate username using parameterized queries
        cur.execute("SELECT username FROM airline_staff WHERE username = %s", (username,))
        if cur.fetchone():
            flash('User name already exists!', 'danger')

        else:
            cur.execute("INSERT INTO airline_staff (username, password, first_name, last_name, date_of_birth, airline_name) VALUES (%s, %s, %s, %s, %s, %s)",
                        (username, hashed_password, first_name, last_name, date_of_birth, airline_name))
            conn.commit()
            flash(f'Account created for {username}!', 'success')
            return redirect(url_for('login_airline_staff'))       ### redirect user back to login page to login

        cur.close()

    return render_template('login.html', form=form, tab='staff')



@auth.route('/logout')
def logout():
    # Remove all session keys you have set
    session_keys = ['username', 'email', 'type', 'agent_id', 'airline', 'permissions']
    
    for key in session_keys:
        session.pop(key, None) #pop all session keys
    
    flash('You have successfully logged out!', 'info')
    return redirect(url_for('home'))





#contains all register/login/logout details

# think about converting all into one dynamic role selection
# class LoginForm(FlaskForm):
#     role = SelectField('Role', choices=[('customer', 'Customer'), ('agent', 'Agent'), ('staff', 'Staff')])
#     email = StringField('Email', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')
