from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db
from datetime import datetime
from dateutil.relativedelta import relativedelta

general = Blueprint('general', __name__)

@general.route('/') 
@general.route('/home')
def home():
    return render_template('home.html')


@general.route('/flight_status', methods=['GET', 'POST'])
def flight_status():
    form = forms.SearchFlightStatus()
    search_results = None

    #Default time range to include a broad range of flights
    start_time = datetime.today() - relativedelta(years=100)
    end_time = datetime.today() + relativedelta(years=100)

    if form.validate_on_submit():
        start_time = form.start_time.data or start_time
        end_time = form.end_time.data or end_time

    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    # Build the query dynamically
    query_parts = [
        "SELECT flight_num, departure_time, arrival_time, status",
        "FROM flight"
    ]
    parameters = []

    # Always filter by the broad or specific time range
    conditions = ["departure_time BETWEEN %s AND %s"]
    parameters += [start_time, end_time]

    if form.flight_number.data:
        conditions.append("flight_num = %s")
        parameters.append(form.flight_number.data)

    if conditions:
        query_parts.append("WHERE " + " AND ".join(conditions))

    final_query = " ".join(query_parts)
    cur.execute(final_query, parameters)
    search_results = cur.fetchall()
    cur.close()

    if not search_results and form.validate_on_submit():
        flash('No flights match your search criteria.', 'warning')

    return render_template('flight_status.html', form=form, search_results=search_results)



### Customers and Agents first submit and can view buy tickets here, you will need to add functionalities here that manage this
@general.route('/view_flights', methods=['GET', 'POST'])
def view_flights():
    form = forms.SearchFlights()
    flights = None

    # Default time range to a very broad range to include all flights if no dates are specified
    start_time = datetime.today() - relativedelta(years=100)
    end_time = datetime.today() + relativedelta(years=100)

    if form.validate_on_submit():
        start_time = form.start_time.data or start_time
        end_time = form.end_time.data or end_time

    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    #We can build SQL query dynamically so that we can make some of the inputs optional (default values)
    query_parts = [
        "SELECT flight_num, departure_airport, arrival_airport, departure_time, arrival_time",
        "FROM flight"
    ]
    parameters = []

    conditions = ["departure_time BETWEEN %s AND %s"]
    parameters += [start_time, end_time]

    if form.departure_place.data:
        conditions.append("departure_airport = %s")
        parameters.append(form.departure_place.data)
    if form.arrival_place.data:
        conditions.append("arrival_airport = %s")
        parameters.append(form.arrival_place.data)

    if conditions:
        query_parts.append("WHERE " + " AND ".join(conditions))

    final_query = " ".join(query_parts)
    cur.execute(final_query, parameters)
    flights = cur.fetchall()
    cur.close()

    if not flights and form.validate_on_submit():
        flash('No flights found matching your criteria.', 'warning')

    return render_template('view_flights.html', form=form, flights=flights)





### Purchase ticket for customer and agent
### Check if session is customer or agent, if no one logged in, send them to login page.
### For this I will use SQL procedure to process if there is enough seats for users

#####DOUBLE CHECK, agents can only purchase flights they work for

##### Assumption: We assume one customer can buy multiple seats, theres a Mr.Beast video where he buys the whole plane :)
@general.route('/purchase_ticket/<int:flight_num>', methods=['GET', 'POST'])
def purchase_ticket(flight_num):
    if 'type' not in session or session['type'] not in ['customer', 'agent']:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('authentication.login'))

    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    left = 0

    # Fetch flight details
    cur.execute("""
    SELECT airline_name, flight_num, departure_airport, departure_time,
    arrival_airport, arrival_time, price
    FROM flight
    WHERE flight_num = %s""", (flight_num,))
    flight = cur.fetchone()

    # Check and return available seats
    cur.execute("""
    SELECT f.airline_name, a.seats - COUNT(t.ticket_id) AS available_seats
    FROM flight f
    JOIN airplane a ON f.airplane_id = a.airplane_id
    LEFT JOIN ticket t ON f.flight_num = t.flight_num
    WHERE f.flight_num = %s
    GROUP BY f.airline_name, a.seats
    """, (flight_num,))
    seat_check = cur.fetchone()

    left = seat_check['available_seats']  #Geet number of seats left over

    form = forms.Purchase()

    
    if form.validate_on_submit():
        customer_email = form.customer.data if 'agent' in session['type'] else session.get('email')

        # Verify customer exists if an agent is booking
        if 'agent' in session['type']:
            #log agent id to input into purchases later
            agent_id = session['agent_id']

            # Verify if agent works for the airline of the flight
            cur.execute("""
                SELECT airline_name FROM booking_agent_work_for
                WHERE email = %s AND airline_name = %s
            """, (session['email'], flight['airline_name']))             #check if email corresponds
            airline_match = cur.fetchone()

            if not airline_match:
                flash("You can only purchase tickets for airlines you represent.", 'danger')
                cur.close()
                return render_template('purchase_ticket.html', form=form, flight=flight, flight_num=flight_num)
            
            cur.execute("SELECT email FROM customer WHERE email = %s", (customer_email,))
            customer_exist = cur.fetchone()
            
            if not customer_exist:
                flash('Customer email does not exist.', 'danger')
                cur.close()
                return render_template('purchase_ticket.html', form=form, flight=flight, flight_num=flight_num)

        # check if we can insert anymore tickets
        if seat_check and left > 0:
            # Insert a ticket
            cur.execute("""
                INSERT INTO ticket (airline_name, flight_num)
                VALUES (%s, %s)
            """, (seat_check['airline_name'], flight_num))
            ticket_id = cur.lastrowid  # Assuming lastrowid retrieves the last inserted ID

            # Record the purchase
            cur.execute("""
                INSERT INTO purchases (ticket_id, customer_email, booking_agent_id, purchase_date)
                VALUES (%s, %s, %s, CURDATE())
            """, (ticket_id, customer_email, agent_id))
            conn.commit()  # Commit

            flash('Ticket purchased successfully!', 'success')
            cur.close()
            return redirect(url_for('general.view_flights'))
        
        else:
            flash('Purchase failed due to no available seats.', 'danger')
        
        cur.close()

    if not flight:
        flash('Flight not found.', 'danger')
        return redirect(url_for('general.view_flights'))

    return render_template('purchase_ticket.html', form=form, flight=flight, flight_num=flight_num, left = left)





# @general.route('/purchase_ticket/<int:flight_num>', methods=['GET', 'POST'])
# def purchase_ticket(flight_num):
#     if 'type' not in session or session['type'] not in ['customer', 'agent']:
#         flash('Please log in to continue.', 'warning')
#         return redirect(url_for('authentication.login'))

#     form = forms.Purchase()
    
#     if form.validate_on_submit():
#         agent_id = form.agent.data or None  # Handle NULL if no agent is involved
#         customer_email = form.customer.data or session.get('email')  # Use session email if customer is logged in

#         conn = setup_db()
#         cur = conn.cursor(dictionary=True)
        
#         print("input values: ", flight_num, customer_email, agent_id)

#         # Call the diagnostic procedure
#         cur.callproc('test_attempt_purchase', [flight_num, 0, 0, 0])
#         cur.execute("SELECT @debug_airline_name AS airline_name, @debug_seats AS seats, @debug_tickets_sold AS tickets_sold;")
#         result = cur.fetchone()
#         cur.close()

#         print(f"Diagnostic results - Airline Rows: {result['airline_name']}, Seat Rows: {result['seats']}, Tickets Sold: {result['tickets_sold']}")

#         # Based on diagnostic results, adjust your main logic or procedure calls

#     return render_template('purchase_ticket.html', form=form, flight_num=flight_num)



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
    


### we don't need this but don't delete, I will implement this directly into the users profiles
### leave this here so you know this functionality will not be implemented.
# @general.route('view_my_flights')  
#     def view_flights():
#     user_type == session.get('type')

#     #Customer can view their own flights they've booked 
#     if user_type == 'customer':
#         return redirect(url_for('customer.customer_profile'))

#     #Agent can see flights they've booked
#     elif user_type == 'agent':
#         return redirect(url_for('agent.agent_profile'))

#     #Staff can see flights operated by their airlines within the next 30 days, but they will also be able to 
#     #Also see all customers of a particular flight
#     elif user_type == 'staff':
#         return redirect(url_for('staff.staff_profile'))
#     else:
#         return redirect(url_for('general.home'))
