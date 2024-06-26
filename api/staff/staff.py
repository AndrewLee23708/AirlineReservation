from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Runtime error solution
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import base64
from database import setup_db
from datetime import datetime
from dateutil.relativedelta import relativedelta

### staff dashboard
staff = Blueprint('staff', __name__)

### dashboard contains flight information of airlines its related to the staffs airline
### next to the dashboard will be a box containing all functionalities for all of these methods 
@staff.route('/staff_profile', methods=['GET', 'POST'])
def staff_profile():
    form = forms.StaffSearchFlight()  # This form needs to handle validation appropriately

    # Default time range for next 30 days
    start_time = datetime.today() 
    end_time = datetime.today() + relativedelta(days=30)

    if form.validate_on_submit():
        start_time = form.start_time.data or start_time
        end_time = form.end_time.data or end_time

    departure_airport = form.departure_airport.data
    arrival_airport = form.arrival_airport.data
    flight_number = form.flight_number.data

    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    # Start building the SQL query dynamically
    query_parts = [
        "SELECT flight_num, departure_airport, arrival_airport, departure_time, arrival_time, status",
        "FROM flight",
        "WHERE airline_name = %s",
        "AND departure_time BETWEEN %s AND %s"
    ]
    parameters = [session['airline'], start_time, end_time]

    # Append conditions based on provided form data
    if flight_number:
        query_parts.append("AND flight_num = %s")
        parameters.append(flight_number)
    if departure_airport:
        query_parts.append("AND departure_airport = %s")
        parameters.append(departure_airport)
    if arrival_airport:
        query_parts.append("AND arrival_airport = %s")
        parameters.append(arrival_airport)

    # Join all parts of the query
    final_query = " ".join(query_parts)
    
    cur.execute(final_query, parameters)
    flights = cur.fetchall()
    cur.close()

    return render_template('staff_profile.html', form=form, flights=flights)


# ### Admin only tool box, contains all functionalities for admin
# Includes 5 functionalities
# Create flight, insert one-by-one not all onto flight table 
@staff.route('/staff_create_flight', methods=['GET', 'POST'])
def staff_create_flight():

    if 'permissions' not in session or 'Admin' not in session['permissions']:
        flash('You do not have administrative access to this page.', 'warning')
        return redirect(url_for('general.home'))
    
    form = forms.CreateFlight()
    if form.validate_on_submit():
        conn = setup_db()
        cur = conn.cursor(dictionary=True)

        # Check for duplicate flight number 
        cur.execute("SELECT * FROM flight WHERE flight_num = %s AND airline_name = %s", (form.flight_num.data, session['airline']))
        if cur.fetchone():
            flash('The flight already exists!', 'danger')
            return render_template('staff_create_flight.html', form=form)

        # Check if the airplane exists and get the number of seats
        cur.execute("SELECT seats FROM airplane WHERE airplane_id = %s AND airline_name = %s", (form.airplane_id.data, session['airline']))
        airplane = cur.fetchone()
        if not airplane:
            flash('Airplane does not exist!', 'danger')
            return render_template('staff_create_flight.html', form=form)

        try:
            # Add the new flight
            query = """
                INSERT INTO flight (airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (session['airline'], form.flight_num.data, form.departure_airport.data, form.departure_time.data, form.arrival_airport.data, form.arrival_time.data, form.price.data, form.status.data, form.airplane_id.data))
            conn.commit()

            flash('Flight created successfully!', 'success')
        except Exception as e:
            flash(f'Failed to create flight. Error: {str(e)}', 'danger')

        finally:
            cur.close()
    return render_template('staff_create_flight.html', form=form)


### Looks good
## Add airplane
@staff.route('/staff_add_airplane', methods=['GET', 'POST'])
def staff_add_airplane():

    if 'permissions' not in session or 'Admin' not in session['permissions']:
        flash('You do not have administrative access to this page.', 'warning')
        return redirect(url_for('general.home'))

    form = forms.AddAirplane()
    if form.validate_on_submit():
        conn = setup_db()
        cur = conn.cursor(dictionary=True)

        # Check if the airplane already exists in the database
        cur.execute("SELECT * FROM airplane WHERE airplane_id = %s AND airline_name = %s", (form.airplane_id.data, session['airline']))
        if cur.fetchone():
            flash('This airplane already exists!', 'danger')
            return render_template('staff_add_airplane.html', form=form)

        try:
            # Insert the new airplane
            query = "INSERT INTO airplane (airplane_id, seats, airline_name) VALUES (%s, %s, %s)"
            cur.execute(query, (form.airplane_id.data, form.seats.data, session['airline']))
            conn.commit()
            flash('Airplane added successfully!', 'success')
        except Exception as e:
            flash(f'Failed to add airplane. Error: {str(e)}', 'danger')
        finally:
            cur.close()

    return render_template('staff_add_airplane.html', form=form)

#Works
@staff.route('/staff_add_airport', methods=['GET', 'POST'])
def staff_add_airport():

    if 'permissions' not in session or 'Admin' not in session['permissions']:
        flash('You do not have administrative access to this page.', 'warning')
        return redirect(url_for('general.home'))

    form = forms.AddAirport()
    if form.validate_on_submit():
        conn = setup_db()
        cur = conn.cursor(dictionary=True)

        # Check if  airport already exists
        cur.execute("SELECT * FROM airport WHERE airport_name = %s", (form.airport_name.data,))
        existing_airport = cur.fetchone()
        
        if existing_airport:
            flash('This airport already exists!', 'danger')
        else:
            try:
                # Insert the new airport
                query = "INSERT INTO airport (airport_name, airport_city) VALUES (%s, %s)"
                cur.execute(query, (form.airport_name.data, form.airport_city.data))
                conn.commit()
                flash('Airport added successfully!', 'success')
            except Exception as e:
                flash(f'Failed to add airport. Error: {str(e)}', 'danger')
            finally:
                cur.close()
                
    return render_template('staff_add_airport.html', form=form)

### Make sure to add constraint that staff has to be in the same airline as staff being changed.
#Works
@staff.route('/staff_grant_permission', methods=['GET', 'POST'])
def staff_grant_permission():

    if 'permissions' not in session or 'Admin' not in session['permissions']:
        flash('You do not have administrative access to this page.', 'warning')
        return redirect(url_for('general.home'))

    form = forms.GrantPermissions()
    if form.validate_on_submit():
        conn = setup_db()
        cur = conn.cursor(dictionary=True)

        try:
            # Fetch the airline name of the staff being updated
            cur.execute("SELECT airline_name FROM airline_staff WHERE username = %s", (form.username.data,))
            target_airline = cur.fetchone()
            
            # Check if the staff being updated is in the same airline
            if target_airline and target_airline['airline_name'] == session.get('airline'):
                # Perform update if they are in the same airline
                query = """
                    INSERT INTO permission (username, permission_type)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE permission_type = VALUES(permission_type)
                """
                cur.execute(query, (form.username.data, form.permission.data))
                conn.commit()
                flash('Permission granted successfully!', 'success')
            else:
                flash('Cannot update staff from different airline.', 'danger')
                
        except Exception as e:
            flash(f'Failed to grant permission. Error: {str(e)}', 'danger')
        finally:
            cur.close()

    return render_template('staff_grant_permission.html', form=form)


### Make sure to add constraint that staff has to be in the same airline as agent being changed.
# Works
@staff.route('/staff_add_agent', methods=['GET', 'POST'])
def staff_add_agent():

    if 'permissions' not in session or 'Admin' not in session['permissions']:
        flash('You do not have administrative access to this page.', 'warning')
        return redirect(url_for('general.home'))

    form = forms.AddAgent()
    if form.validate_on_submit():
        conn = setup_db()
        cur = conn.cursor()

        try:
            # Use staff's airline from the session
            airline_name = session.get('airline')
            query = "INSERT INTO booking_agent_work_for (email, airline_name) VALUES (%s, %s)"
            cur.execute(query, (form.email.data, airline_name))
            conn.commit()
            flash('Booking agent added successfully to the airline!', 'success')

        except Exception as e:
            flash(f'Failed to add booking agent. Error: {str(e)}', 'danger')

        finally:
            cur.close()
    return render_template('staff_add_agent.html', form=form)

# ### Admin only
# @staff.route('/create_flight', methods=['GET', 'POST'])
# def create_flight():
#     pass

# ### Admin only
# @staff.route('/add_airplane', methods=['GET', 'POST'])
# def add_airplane():
#     pass

# ### Admin only
# @staff.route('/add_airport', methods=['GET', 'POST'])
# def add_airport():
#     pass

# ### Admin
# @staff.route('/grant_permissions', methods=['GET', 'POST'])
# def grant_permissions():
#     pass

# ### Admin
# @staff.route('/add_booking_agents', methods=['GET', 'POST'])
# def add_booking_agents():
#     pass


### Operator only
# Change Flight_status
@staff.route('/staff_operator', methods=['GET', 'POST'])
def staff_operator():

    if 'permissions' not in session or 'Operator' not in session['permissions']:
        flash('You do not have administrative access to this page.', 'warning')
        return redirect(url_for('general.home'))

    form = forms.ChangeFlightStatus()
    if form.validate_on_submit():
        conn = setup_db()
        cur = conn.cursor()

        try:
            #check if the flight number exists in the airline the staff belongs to
            cur.execute("SELECT * FROM flight WHERE flight_num = %s AND airline_name = %s", (form.flight_num.data, session['airline']))
            flight = cur.fetchone()
            
            if flight:
                # Update  flight status
                query = "UPDATE flight SET status = %s WHERE flight_num = %s"
                cur.execute(query, (form.status.data, form.flight_num.data))
                conn.commit()
                flash('Flight status updated successfully!', 'success')
            else:
                #Not under same airline
                flash('Flight number does not exist in your airline.', 'danger')
                
        except Exception as e:
            flash(f'Failed to update flight status. Error: {str(e)}', 'danger')

        finally:
            cur.close()
        
        return redirect(url_for('staff.staff_operator'))

    return render_template('staff_operator.html', form=form)



#####

### Endpoints for staffs in general:

#####

# View all the booking agents: Top 5 booking agents based on number of tickets sales for the past month and
# past year. Top 5 booking agents based on the amount of commission received for the last year.
@staff.route('/staff_view_booking_agents')
def view_booking_agents():
    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    def get_top_agents(metric, period, metric_name="num_tickets"):
        interval = "1 MONTH" if period == 'month' else "1 YEAR"
        # Adjust to count each ticket by referencing the ticket table directly
    
        column = "COUNT(ticket.ticket_id)" if metric == 'tickets' else "SUM(flight.price)"
        query = f"""
            SELECT purchases.booking_agent_id, {column} AS {metric_name}
            FROM purchases
            JOIN ticket ON purchases.ticket_id = ticket.ticket_id
            JOIN flight ON ticket.flight_num = flight.flight_num  # Join flight table to access the price
            WHERE flight.airline_name = %s AND purchases.purchase_date >= DATE_SUB(CURDATE(), INTERVAL {interval})
              AND purchases.booking_agent_id IS NOT NULL
            GROUP BY purchases.booking_agent_id
            ORDER BY {metric_name} DESC
            LIMIT 5
        """
        cur.execute(query, (session['airline'],))
        return cur.fetchall()

    top_5_agents_past_month = get_top_agents('tickets', 'month')
    top_5_agents_past_year = get_top_agents('tickets', 'year')
    top_5_agents_commission_past_year = get_top_agents('commission', 'year', "commission")

    # Get all booking agents in this airline
    cur.execute("""
        SELECT booking_agent.email, booking_agent.booking_agent_id
        FROM booking_agent
        JOIN booking_agent_work_for ON booking_agent.email = booking_agent_work_for.email
        WHERE booking_agent_work_for.airline_name = %s
    """, (session['airline'],))
    booking_agents = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        'staff_view_agents.html',
        top_5_agents_past_month=top_5_agents_past_month,
        top_5_agents_past_year=top_5_agents_past_year,
        top_5_agents_commission_past_year=top_5_agents_commission_past_year,
        booking_agents=booking_agents
    )




# View frequent customers: Airline Staff will also be able to see the most frequent customer within the last
# year. In addition, Airline Staff will be able to see a list of all flights a particular Customer has taken only on
# that particular airline
@staff.route('/view_frequent_customers', methods=['GET'])
def view_frequent_customers():
    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    # See all customers and their all their flights regardless of airline
    query = """
        SELECT customer_email, COUNT(*) AS num_tickets
        FROM purchases
        JOIN ticket ON purchases.ticket_id = ticket.ticket_id
        JOIN flight ON ticket.flight_num = flight.flight_num
        WHERE purchases.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        GROUP BY customer_email
        ORDER BY num_tickets DESC
    """
    cur.execute(query)
    customers = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('staff_view_customers.html', customers=customers)


# each individual customer tickets (for that airline specifcally)
@staff.route('/view_customer_tickets/<customer_email>', methods=['GET'])
def view_customer_tickets(customer_email):
    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    query = """
        SELECT ticket.ticket_id, flight.flight_num, flight.departure_airport, flight.arrival_airport,
               flight.departure_time, flight.arrival_time, flight.price
        FROM purchases
        JOIN ticket ON purchases.ticket_id = ticket.ticket_id
        JOIN flight ON ticket.flight_num = flight.flight_num
        WHERE purchases.customer_email = %s AND flight.airline_name = %s
        ORDER BY flight.departure_time
    """
    cur.execute(query, (customer_email, session['airline']))
    tickets = cur.fetchall()

    ### Need to format date object into strings
    for ticket in tickets:
        ticket['departure_time'] = ticket['departure_time'].strftime('%Y-%m-%d %H:%M')
        ticket['arrival_time'] = ticket['arrival_time'].strftime('%Y-%m-%d %H:%M')

    cur.close()
    conn.close()

    return render_template('staff_view_customer_ticket.html', tickets=tickets, customer_email=customer_email, airline = session['airline'])




# View reports: Total amounts of ticket sold based on range of dates/last year/last month etc. Month wise
# tickets sold in a bar chart.
@staff.route('/view_reports', methods=['GET', 'POST'])
def view_reports():
    form = forms.TimeInterval()
    if form.validate_on_submit():
        start_date = form.start_date.data or (datetime.date.today() - relativedelta(years=1))
        end_date = form.end_date.data or datetime.date.today()

        connection = setup_db()
        cursor = connection.cursor(dictionary=True)

        # Query to fetch month-wise ticket sales
        query = """
            SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, COUNT(*) AS num_tickets
            FROM purchases
            JOIN ticket ON purchases.ticket_id = ticket.ticket_id
            WHERE airline_name = %s AND purchase_date BETWEEN %s AND %s
            GROUP BY year, month
            ORDER BY year, month
        """
        cursor.execute(query, (session['airline'], start_date, end_date))
        tickets_report = cursor.fetchall()
        cursor.close()
        connection.close()

        labels = [f"{row['year']}-{row['month']:02d}" for row in tickets_report]
        values = [row['num_tickets'] for row in tickets_report]

        fig, ax = plt.subplots()
        ax.bar(labels, values, color='blue')
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Tickets Sold')
        ax.set_title('Monthly Ticket Sales')
        ax.xaxis.set_major_locator(MaxNLocator(nbins=len(labels))) 
        plt.xticks(rotation=45)
        
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        plot_url = base64.b64encode(buf.read()).decode('utf-8')

        return render_template('staff_view_reports.html', form=form, plot_url=plot_url)

    return render_template('staff_view_reports.html', form=form)


# Comparison of Revenue earned: Draw a pie chart for showing total amount of revenue earned from direct
# sales (when customer bought tickets without using a booking agent) and total amount of revenue earned from
# indirect sales (when customer bought tickets using booking agents) in the last month and last year.
# It works
@staff.route('/compare_revenue', methods=['GET'])
def compare_revenue():
    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    # Function to fetch revenue and ticket count
    def fetch_data(sales_type, period):
        interval = "1 MONTH" if period == "month" else "1 YEAR"
        booking_condition = "IS NULL" if sales_type == "direct" else "IS NOT NULL"
        query = f"""
            SELECT
                COALESCE(SUM(flight.price), 0) AS revenue,
                COUNT(ticket.ticket_id) AS tickets_sold
            FROM purchases
            JOIN ticket ON purchases.ticket_id = ticket.ticket_id
            JOIN flight ON ticket.flight_num = flight.flight_num
            WHERE flight.airline_name = %s
            AND purchases.purchase_date >= DATE_SUB(CURDATE(), INTERVAL {interval})
            AND purchases.booking_agent_id {booking_condition}
        """
        cur.execute(query, (session['airline'],))
        return cur.fetchone()

    data = {
        'direct_month': fetch_data('direct', 'month'),
        'direct_year': fetch_data('direct', 'year'),
        'indirect_month': fetch_data('indirect', 'month'),
        'indirect_year': fetch_data('indirect', 'year')
    }

    cur.close()
    conn.close()

    # Generate and send plots
    month_image = generate_plot(data, 'month')
    year_image = generate_plot(data, 'year')

    # Send the detailed data to the template
    return render_template(
        'staff_view_revenue.html', 
        month_image=month_image, year_image=year_image,
        month_data=data['direct_month'], year_data=data['direct_year'],
        month_indirect_data=data['indirect_month'], year_indirect_data=data['indirect_year']
    )

## For plot generation
def generate_plot(data, period):
    labels = ['Direct Sales', 'Indirect Sales']
    sizes = [data[f'direct_{period}']['revenue'], data[f'indirect_{period}']['revenue']]
    colors = ['#87ceeb','#ff474c']  # Blue for direct, red for indirect
    explode = (0.1, 0)  # Only "explode" the first slice

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
           shadow=True, startangle=90, colors=colors)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Convert plot to PNG image
    png_image = BytesIO()
    plt.savefig(png_image, format='png')
    plt.close(fig)
    png_image.seek(0)
    uri = 'data:image/png;base64,' + base64.b64encode(png_image.getvalue()).decode('utf-8')
    return uri



# ViewTop destinations: Find the top 3 most popular destinations for last 3 months and last year.
##### !!! NOT AIRLINE SPECIFIC
# It works
@staff.route('/view_top_destinations', methods=['GET'])
def view_top_destinations():

    connection = setup_db()
    cursor = connection.cursor(dictionary=True)

    # last 3 month
    month_query = """
        SELECT a.airport_name AS place, COUNT(*) AS ticket_count
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        JOIN flight f ON t.flight_num = f.flight_num
        JOIN airport a ON f.arrival_airport = a.airport_name
        WHERE p.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
        GROUP BY place
        ORDER BY ticket_count DESC
        LIMIT 3
    """
    cursor.execute(month_query,)
    month = cursor.fetchall()

    # last year
    year_query = """
        SELECT a.airport_name AS place, COUNT(*) AS ticket_count
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        JOIN flight f ON t.flight_num = f.flight_num
        JOIN airport a ON f.arrival_airport = a.airport_name
        WHERE p.purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        GROUP BY place
        ORDER BY ticket_count DESC
        LIMIT 3
    """
    cursor.execute(year_query, )
    year = cursor.fetchall()

    print(month) 
    print(year)   

    cursor.close()
    connection.close()

    return render_template('staff_view_top_destinations.html', 
                           month=month, 
                           year=year)