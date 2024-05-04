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

    #Append query if details inputted:
    query = """
        SELECT flight_num, departure_time, arrival_time, status
        FROM flight
    """
    conditions = []
    parameters = []

    ### We want to build it, since sometimes user dosen't put in that data
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
##### Assumption: We assume one customer can buy multiple seats, theres a Mr.Beast video where he buys the whole plane :)
@general.route('/purchase_ticket/<int:flight_num>', methods=['GET', 'POST'])
def purchase_ticket(flight_num):
    if 'type' not in session or session['type'] not in ['customer', 'agent']:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('authentication.login'))

    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    # Fetch flight details
    cur.execute("""
    SELECT airline_name, flight_num, departure_airport, departure_time,
    arrival_airport, arrival_time, price
    FROM flight
    WHERE flight_num = %s""", (flight_num,))
    flight = cur.fetchone()

    form = forms.Purchase()
    
    if form.validate_on_submit():
        agent_id = form.agent.data if 'agent' in session['type'] else None
        customer_email = form.customer.data if 'agent' in session['type'] else session.get('email')

        # Verify customer exists if an agent is booking
        if 'agent' in session['type']:
            cur.execute("SELECT email FROM customer WHERE email = %s", (customer_email,))
            customer_exist = cur.fetchone()
            if not customer_exist:
                flash('Customer email does not exist.', 'danger')
                cur.close()
                return render_template('purchase_ticket.html', form=form, flight=flight, flight_num=flight_num)

        # Check for available seats
        cur.execute("""
            SELECT f.airline_name, a.seats - COUNT(t.ticket_id) AS available_seats
            FROM flight f
            JOIN airplane a ON f.airplane_id = a.airplane_id
            LEFT JOIN ticket t ON f.flight_num = t.flight_num
            WHERE f.flight_num = %s
            GROUP BY f.airline_name, a.seats
        """, (flight_num,))
        seat_check = cur.fetchone()

        if seat_check and seat_check['available_seats'] > 0:
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

    return render_template('purchase_ticket.html', form=form, flight=flight, flight_num=flight_num)





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
    


### we don't need this but don't delete, I will implement this directly into the users dashboard
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
