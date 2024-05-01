from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db
from datetime import datetime
from dateutil.relativedelta import relativedelta

### staff dashboard
staff = Blueprint('staff', __name__)

### dashboard contains flight information of airlines its related to the staffs airline
### next to the dashboard will be a box containing all functionalities for all of these methods 
@staff.route('/staff_profile', methods=['GET', 'POST'])
def staff_profile():
    
    form = forms.AirlineStaffSearchForm()  # Assume a specific form for flight searching

    # Default values for start_time and end_time
    start_time = datetime.today() - relativedelta(days=30)
    end_time = datetime.today()

    # Update time range if specified by the user
    if form.validate_on_submit():
        start_time = form.start_time.data or start_time
        end_time = form.end_time.data or end_time

    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    # Build the SQL query dynamically based on the form inputs
    query = """
        SELECT flight_num, departure_airport, arrival_airport, departure_time, arrival_time, status
        FROM flight
        WHERE airline_name = %s AND departure_time BETWEEN %s AND %s
    """
    parameters = [session['airline'], start_time, end_time]

    # Extend the query based on additional search parameters
    if form.flight_number.data:
        query += " AND flight_num = %s"
        parameters.append(form.flight_number.data)

    cur.execute(query, parameters)
    flights = cur.fetchall()
    cur.close()

    # Render the template with the search form and the flight results
    return render_template('staff_profile.html', form=form, flights=flights)                                 ###FIX THIS, Not dispalying if only flight number is searched

@staff.route('/staff_create_flight', methods=['GET', 'POST'])
def staff_create_flight():

    form = forms.CreateFlightForm()
    if form.validate_on_submit():
        try:
            conn = setup_db()
            cur = conn.cursor()
            query = """
                INSERT INTO flight (flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (form.flight_num.data, form.departure_airport.data, form.departure_time.data, form.arrival_airport.data, form.arrival_time.data, form.price.data, form.status.data, form.airplane_id.data))
            conn.commit()
            flash('Flight created successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Failed to create flight. Error: {str(e)}', 'danger')
        finally:
            cur.close()
    return render_template('staff_create_flight.html', form=form)


@staff.route('/staff_add_airplane', methods=['GET', 'POST'])
def staff_add_airplane():

    form = forms.AddAirplaneForm()
    if form.validate_on_submit():
        try:
            conn = setup_db()
            cur = conn.cursor()
            query = "INSERT INTO airplane (airplane_id, seats, identifier) VALUES (%s, %s, %s)"
            cur.execute(query, (form.airplane_id.data, form.seats.data, form.identifier.data))
            conn.commit()
            flash('Airplane added successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Failed to add airplane. Error: {str(e)}', 'danger')
        finally:
            cur.close()
    return render_template('staff_add_airplane.html', form=form)

@staff.route('/staff_add_airport', methods=['GET', 'POST'])
def staff_add_airport():

    form = forms.AddAirportForm()
    if form.validate_on_submit():
        try:
            conn = setup_db()
            cur = conn.cursor()
            query = "INSERT INTO airport (airport_name, airport_city) VALUES (%s, %s)"
            cur.execute(query, (form.airport_name.data, form.airport_city.data))
            conn.commit()
            flash('Airport added successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Failed to add airport. Error: {str(e)}', 'danger')
        finally:
            cur.close()
    return render_template('staff_add_airport.html', form=form)

@staff.route('/staff_grant_permission', methods=['GET', 'POST'])
def staff_grant_permission():

    form = forms.GrantNewPermissionForm()
    if form.validate_on_submit():
        try:
            conn = setup_db()
            cur = conn.cursor()
            query = "INSERT INTO permission (email, permission) VALUES (%s, %s) ON DUPLICATE KEY UPDATE permission = VALUES(permission)"
            cur.execute(query, (form.email.data, form.permission.data))
            conn.commit()
            flash('Permission granted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Failed to grant permission. Error: {str(e)}', 'danger')
        finally:
            cur.close()
    return render_template('staff_grant_permission.html', form=form)

@staff.route('/staff_add_booking_agent', methods=['GET', 'POST'])
def staff_add_booking_agent():

    form = forms.AddBookingAgentToAirlineForm()
    if form.validate_on_submit():
        try:
            conn = setup_db()
            cur = conn.cursor()
            query = "INSERT INTO booking_agent_work_for (email, airline_name) VALUES (%s, %s)"
            cur.execute(query, (form.email.data, form.airline_name.data))
            conn.commit()
            flash('Booking agent added successfully to the airline!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Failed to add booking agent. Error: {str(e)}', 'danger')
        finally:
            cur.close()
    return render_template('staff_add_booking_agent.html', form=form)




# ### Admin only tool box, contains all functionalities for admin

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
def change_flight_status():
    pass

###Create seperate endpoints for these

@staff.route('/view_booking_agents')
def view_booking_agents():
    pass

@staff.route('/view_frequent_customers')
def view_frequent_customers():
    pass

@staff.route('/view_reports', methods=['GET', 'POST'])
def view_reports():
    pass

@staff.route('/compare_revenue', methods=['GET', 'POST'])
def compare_revenue():
    pass

@staff.route('/view_top_destinations')
def view_top_destinations():
    pass




# @staff.route('/staff_admin', methods=['GET', 'POST'])
# def staff_admin():

#     ###First check if admin perms

#     create_flight_form = forms.CreateFlightForm()
#     add_airplane_form = forms.AddAirplaneForm()
#     add_airport_form = forms.AddAirportForm()
#     grant_permission_form = forms.GrantNewPermissionForm()
#     add_booking_agent_form = forms.AddBookingAgentToAirlineForm()

#     if create_flight_form.validate_on_submit():
#         flight_num = create_flight_form.flight_num.data
#         departure_airport = create_flight_form.departure_airport.data
#         departure_time = create_flight_form.departure_time.data
#         arrival_airport = create_flight_form.arrival_airport.data
#         arrival_time = create_flight_form.arrival_time.data
#         price = create_flight_form.price.data
#         status = create_flight_form.status.data
#         airplane_id = create_flight_form.airplane_id.data

#         # Database connection
#         conn = setup_db()
#         cur = conn.cursor(dictionary=True)

#         # SQL Insert Query
#         query = """
#             INSERT INTO flight (flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         # Executing the query
#         cur.execute(query, (flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id))
#         conn.commit()  # Committing the transaction
#         cur.close()  # Close the cursor

#         flash('Flight created successfully!', 'success')

#     if add_airplane_form.validate_on_submit():
#         try:
#             # Extracting form data
#             airplane_id = add_airplane_form.airplane_id.data
#             seats = add_airplane_form.seats.data
#             identifier = add_airplane_form.identifier.data  # Assuming 'identifier' is some meaningful field for the airplane

#             # Database connection
#             conn = setup_db()
#             cur = conn.cursor(dictionary=True)

#             # SQL Insert Query
#             query = """
#                 INSERT INTO airplane (airplane_id, seats, identifier)
#                 VALUES (%s, %s, %s)
#             """
#             # Executing the query
#             cur.execute(query, (airplane_id, seats, identifier))
#             conn.commit()  # Committing the transaction
#             cur.close()  # Close the cursor

#             flash('Airplane added successfully!', 'success')

#         except Exception as e:
#             conn.rollback()  # Rollback in case of any error
#             flash(f'Failed to add airplane. Error: {str(e)}', 'danger')


#     if add_airport_form.validate_on_submit():
#         try:
#             # Extract data from the form
#             airport_name = add_airport_form.airport_name.data
#             airport_city = add_airport_form.airport_city.data

#             # Setup database connection
#             conn = setup_db()
#             cur = conn.cursor(dictionary=True)

#             # Prepare the SQL insert statement
#             query = """
#                 INSERT INTO airport (airport_name, airport_city)
#                 VALUES (%s, %s)
#             """
#             # Execute the query with parameters
#             cur.execute(query, (airport_name, airport_city))
#             conn.commit()  # Commit the transaction
#             cur.close()  # Close the cursor

#             flash('Airport added successfully!', 'success')
#         except Exception as e:
#             # Roll back the transaction in case of an error
#             conn.rollback()
#             flash(f'Failed to add airport. Error: {str(e)}', 'danger')

#     if grant_permission_form.validate_on_submit():
#         try:
#             # Extract data from the form
#             email = grant_permission_form.email.data
#             permission = grant_permission_form.permission.data

#             # Setup database connection
#             conn = setup_db()
#             cur = conn.cursor(dictionary=True)

#             # Prepare the SQL statement to insert or update permission
#             query = """
#                 INSERT INTO permission (email, permission)
#                 VALUES (%s, %s)
#                 ON DUPLICATE KEY UPDATE
#                 permission = VALUES(permission)  # Assumes you handle permissions as updatable
#             """
#             # Execute the query with parameters
#             cur.execute(query, (email, permission))
#             conn.commit()  # Commit the transaction
#             cur.close()  # Close the cursor

#             flash('Permission granted successfully!', 'success')
#         except Exception as e:
#             # Roll back the transaction in case of an error
#             conn.rollback()
#             flash(f'Failed to grant permission. Error: {str(e)}', 'danger')


#     if add_booking_agent_form.validate_on_submit():
#         try:
#             # Extract data from the form
#             email = add_booking_agent_form.email.data
#             airline_name = 'Name_of_Airline'  # This should be dynamically set or retrieved from session or another form

#             # Setup database connection
#             conn = setup_db()
#             cur = conn.cursor(dictionary=True)

#             # Prepare the SQL statement to insert a new booking agent for an airline
#             query = """
#                 INSERT INTO booking_agent_work_for (email, airline_name)
#                 VALUES (%s, %s)
#             """
#             # Execute the query with parameters
#             cur.execute(query, (email, airline_name))
#             conn.commit()  # Commit the transaction
#             cur.close()  # Close the cursor

#             flash('Booking agent added successfully to the airline!', 'success')
#         except Exception as e:
#             # Roll back the transaction in case of an error
#             conn.rollback()
#             flash(f'Failed to add booking agent. Error: {str(e)}', 'danger')

#     return render_template('staff_admin.html', 
#                            create_flight_form=create_flight_form, 
#                            add_airplane_form=add_airplane_form,
#                            add_airport_form=add_airport_form,
#                            grant_permission_form=grant_permission_form,
#                            add_booking_agent_form=add_booking_agent_form)

