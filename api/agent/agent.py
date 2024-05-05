from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
matplotlib.use('Agg')  # Runtime error solution
from matplotlib.ticker import MaxNLocator
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from database import setup_db


agent = Blueprint('agent',__name__)

# viewing flights booked for customers
# Defaults will be showing all the upcoming flights operated by the airline he/she works for
# the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline he/she
# works for based range of dates, source/destination airports/city etc. He/she will be able to see all the
# customers of a particular flight.
@agent.route('/agent_profile', methods=['GET', 'POST'])
def agent_profile():
    if 'type' not in session or session['type'] != 'agent':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('authentication.login'))

    form = forms.SearchFlights()  # Assuming the form is adapted for agents too

    # Default time range for the next 30 days
    start_time = datetime.today()
    end_time = datetime.today() + relativedelta(days=30)

    if form.validate_on_submit():
        start_time = form.start_time.data or start_time
        end_time = form.end_time.data or end_time

    # Simplified handling of form data
    departure_airport = form.departure_place.data
    arrival_airport = form.arrival_place.data
   
    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    # Fetch the airline(s) the agent works for
    cur.execute("""
        SELECT airline_name
        FROM booking_agent_work_for
        WHERE email = %s
    """, (session['email'],))
    airlines = [result['airline_name'] for result in cur.fetchall()]

    flights = []
    if airlines:
        # So only display airlines by staff
        airline_placeholders = ', '.join(['%s'] * len(airlines))

        query_parts = [
            "SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, status",
            f"FROM flight WHERE airline_name IN ({airline_placeholders})",
            "AND departure_time BETWEEN %s AND %s"
        ]
        parameters = airlines + [start_time, end_time]

        if departure_airport:
            query_parts.append("AND departure_airport = %s")
            parameters.append(departure_airport)
        if arrival_airport:
            query_parts.append("AND arrival_airport = %s")
            parameters.append(arrival_airport)

        # Join all parts of the query
        final_query = " ".join(query_parts)
        
        cur.execute(final_query, parameters)
        flights.extend(cur.fetchall())
    else:
        flash('No associated airlines found for this agent.', 'warning')

    cur.close()
    conn.close()

    return render_template('agent_profile.html', form=form, flights=flights)



### Click into tab, see customers in that flight
@agent.route('/view_flight_customers/<int:flight_num>', methods=['GET'])
def view_flight_customers(flight_num):
    
    if 'type' not in session or session['type'] != 'agent':
        flash('Unauthorized access. Please log in as an agent.', 'danger')
        return redirect(url_for('authentication.login'))

    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    # Fetch all customers who have purchased tickets for this flight
    query = """
    SELECT c.email, c.name
    FROM customer c
    JOIN purchases p ON c.email = p.customer_email
    JOIN ticket t ON p.ticket_id = t.ticket_id
    JOIN flight f ON t.flight_num = f.flight_num AND t.airline_name = f.airline_name
    WHERE f.flight_num = %s
    """
    cur.execute(query, (flight_num,))
    customers = cur.fetchall()

    cur.close()
    conn.close()

    # Check if there are any customers for this flight
    if not customers:
        flash('No customers found for this flight.', 'warning')
        return redirect(url_for('agent_profile'))

    return render_template('agent_flight_customers.html', customers=customers, flight_num=flight_num)



# View my commission: Default view will be total amount of commission received in the past 30 days and the
# average commission he/she received per ticket booked in the past 30 days and total number of tickets sold by
# him in the past 30 days. He/she will also have option to specify a range of dates to view total amount of
# commission received and total numbers of tickets sold.
### commisions is 10% to 15%, so we do 12.5% then
@agent.route('/agent_view_commissions', methods=['GET', 'POST'])
def view_commissions():
    form = forms.TimeInterval()

    # Set default or form-provided dates
    if form.validate_on_submit():
        start_date = form.start_date.data if form.start_date.data else datetime.now() - relativedelta(days=30)
        end_date = form.end_date.data if form.end_date.data else datetime.now()
    else:
        start_date = datetime.now() - relativedelta(days=30)
        end_date = datetime.now()

    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    try:
        # Calculate total commission and number of tickets sold
        ### Use coalesce for null 
        cur.execute("""
            SELECT
                COUNT(*) AS ticket_count,
                COALESCE(SUM(flight.price * 0.125), 0) AS commissions_sum
            FROM purchases
            JOIN ticket ON purchases.ticket_id = ticket.ticket_id
            JOIN flight ON ticket.flight_num = flight.flight_num
            WHERE purchases.booking_agent_id = %s
            AND purchases.purchase_date BETWEEN %s AND %s
        """, (session['agent_id'], start_date, end_date))

        result = cur.fetchone()
        num_tickets = result['ticket_count'] if result else 0
        sum_commissions = result['commissions_sum'] if result else 0
        avg_commission = sum_commissions / num_tickets if num_tickets > 0 else 0

    finally:
        cur.close()
        conn.close()

    return render_template('agent_view_commissions.html', form=form, num_tickets=num_tickets,sum_commissions=sum_commissions,avg_commission=avg_commission)




# View Top Customers: Top 5 customers based on number of tickets bought from the booking agent in the past 6 months and 
# top 5 customers based on amount of commission received in the last year. 
# chart showing each of these 5 customers in x-axis and number of tickets bought in y-axis. Show another bar
# chart showing each of these 5 customers in x-axis and amount commission received in y- axis. (Again, UI/bar
# chart is optional, the important factor is that you are able to retrieve and display the data.)
@agent.route('/view_top_customers', methods=['GET'])
def view_top_customers():
    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    # Define the time intervals
    six_months_ago = datetime.now() - timedelta(days=180)
    one_year_ago = datetime.now() - timedelta(days=365)

    # Top 5 customers based on number of tickets in the past 6 months
    cur.execute("""
        SELECT customer_email, COUNT(*) AS ticket_count
        FROM purchases
        JOIN ticket ON purchases.ticket_id = ticket.ticket_id
        WHERE booking_agent_id = %s AND purchase_date >= %s
        GROUP BY customer_email
        ORDER BY ticket_count DESC
        LIMIT 5
    """, (session['agent_id'], six_months_ago))
    ticket_counts = cur.fetchall()

    # Top 5 customers based on commission received in the past year
    cur.execute("""
        SELECT customer_email, SUM(flight.price) * 0.125 AS commission_sum
        FROM purchases
        JOIN ticket ON purchases.ticket_id = ticket.ticket_id
        JOIN flight ON ticket.flight_num = flight.flight_num
        WHERE booking_agent_id = %s AND purchase_date >= %s
        GROUP BY customer_email
        ORDER BY commission_sum DESC
        LIMIT 5
    """, (session['agent_id'], one_year_ago))
    commission_sums = cur.fetchall()
    cur.close()
    
    # Prepare data for the bar charts
    tickets_emails = [x['customer_email'] for x in ticket_counts]
    tickets_values = [x['ticket_count'] for x in ticket_counts]

    commission_emails = [x['customer_email'] for x in commission_sums]
    commission_values = [x['commission_sum'] for x in commission_sums]

    # Creating bar charts
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # Tickets bar chart
    ax1.bar(tickets_emails, tickets_values, color='blue')
    ax1.set_title('Top 5 Customers by Tickets Bought')
    ax1.set_xlabel('Customers')
    ax1.set_ylabel('Number of Tickets')

    # Commissions bar chart
    ax2.bar(commission_emails, commission_values, color='green')
    ax2.set_title('Top 5 Customers by Commission')
    ax2.set_xlabel('Customers')
    ax2.set_ylabel('Commission Amount ($)')
    
    # Save the plots to a string buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8')

    return render_template('agent_view_customers.html', plot_url=plot_url, ticket_counts=ticket_counts, commission_sums=commission_sums)