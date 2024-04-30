from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db

general = Blueprint('general', __name__)

@general.route('/')           ### Double check, why double route?
@general.route('/home')
def home():
    
    return render_template('home.html')


@general.route('/flight_status', methods=['GET', 'POST'])
def flight_status():
    form = forms.PublicSearchFlightStatusForm()
    search_results = None

    conn = setup_db()
    cur = conn.cursor(dictionary=True)
    query = """
        SELECT flight_num, departure_time, arrival_time, status
        FROM flight
    """
    conditions = []
    parameters = []

    if form.flight_number.data:
        conditions.append("flight_num = %s")
        parameters.append(form.flight_number.data)
    if form.departure_time.data:
        conditions.append("departure_time = %s")
        parameters.append(form.departure_time.data)
    if form.arrival_time.data:
        conditions.append("arrival_time = %s")
        parameters.append(form.arrival_time.data)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cur.execute(query, parameters)
    search_results = cur.fetchall()
    cur.close()

    if form.validate_on_submit() and not search_results:
        flash('No flights match your search criteria.', 'warning')

    return render_template('flight_status.html', form=form, search_results=search_results)





### Customers and Agents first submit and can view buy tickets here, you will need to add functionalities here that manage this
@general.route('/view_flights', methods=['GET', 'POST'])
def view_flights():
    form = forms.PublicSearchUpcomingFlightForm()
    flights = None

    conn = setup_db()
    cur = conn.cursor(dictionary=True)
    query = """
        SELECT flight_num, departure_airport, arrival_airport, departure_time, arrival_time
        FROM flight
    """
    conditions = []
    parameters = []

    if form.departure_place.data:
        conditions.append("departure_airport = %s")
        parameters.append(form.departure_place.data)
    if form.arrival_place.data:
        conditions.append("arrival_airport = %s")
        parameters.append(form.arrival_place.data)
    if form.departure_time.data:
        conditions.append("departure_time = %s")
        parameters.append(form.departure_time.data)
    if form.arrival_time.data:
        conditions.append("arrival_time = %s")
        parameters.append(form.arrival_time.data)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cur.execute(query, parameters)
    flights = cur.fetchall()
    cur.close()

    if form.validate_on_submit() and not flights:
        flash('No upcoming flights found.', 'warning')

    return render_template('view_flights.html', form=form, flights=flights)





### Purchase ticket for customer and agent
### Check if session is customer or agent, if no one logged in, send them to login page.
### For this I will use SQL procedure to process if there is enough seats for users
@general.route('/purchase_ticket/<flight_num>', methods=['GET', 'POST'])
def purchase_ticket(flight_num):
    
    #double check if it's customer or agent
    if 'type' not in session or session['type'] not in ['customer', 'agent']:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('authentication.login'))

    form = forms.Purchase()
    
    if form.validate_on_submit():
        agent_id = form.agent.data
        customer_email = form.customer.data

        # Here you would call your SQL procedure to attempt the ticket purchase
        conn = setup_db()
        cur = conn.cursor(dictionary=True)
        # Assume you have a stored procedure named 'attempt_purchase' that returns a boolean success value
        cur.callproc('attempt_purchase', [flight_num, customer_email, agent_id])
        success, = cur.fetchone().values()
        cur.close()

        if success:
            flash('Ticket purchased successfully!', 'success')
            return redirect(url_for('general.view_flights'))
        else:
            flash('Purchase failed. Please try again.', 'danger')

    return render_template('purchase_ticket.html', form=form, flight_num=flight_num)



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
        flash('Please log in to see your profile', 'warning')
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

