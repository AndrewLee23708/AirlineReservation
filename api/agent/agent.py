from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt

from ..database import setup_db

# viewing flights booked for customers
@agent.route('/purchased_flights', methods = ['GET', 'POST'])
def purchased_flights():
    conn = setup_db()
    cur = conn.cursor(dictionary=True)
    #query
    query = f"SELECT * FROM booking_agent NATURAL JOIN ticket WHERE booking_agent_id = '{session['agent_id']}'"
    cur.execute(query)
    purchased_for = cur.fetchall()
    cur.close()
    print(purchased_for)
    
    return render_template('purchased_flights.html', purchased_for = purchased_for)

# searching for upcoming flights for customers
@agent.route('/upcoming_flights/<search_result>', methods = ['GET'])
def upcoming_flights(search_result):
    search_result = json.loads(search_result)

    return render_template('upcoming_flights.html', search_result = search_result)

# purchasing tickets for customers
@agent.route('/purchasing_tickets_for/<flight_num>', methods = ['GET', 'POST'])
def purchasing_tickets_for(flight_num):
    print(form)
    # first get flight information
    cur = conn.cursor(dictionary=True)    
    query = f"SELECT * FROM ticket NATURAL JOIN flight WHERE flight_num = '{flight_num}'"
    cur.execute(query)
    flight = cur.fetchone()
    cur.close()

    # second get seat info for that flight
    cur = conn.cursor(dictionary=True)
    query = f"SELECT count(ticket_id) as remaining_seats FROM ticket NATURAL JOIN flight WHERE flight_num = '{flight_num}' AND NOT EXISTS (SELECT * FROM purchases WHERE purchases.ticket_id = ticket.ticket_id)"
    cur.execute(query)
    remaining_seats = cur.fetchone()
    cur.close()

    # show all num of tickets by flight (including purchased) DO WE NEED THIS?
    cur = conn.cursor(dictionary=True)
    query = f"SELECT count(ticket_id) as all FROM ticket NATURAL JOIN flight WHERE flight_num = '{flight_num}' GROUP BY flight_num;"
    cur.execute(query)
    all = cur.fetchone()
    cur.close()

    # if there are still seats, we need to update seat information
    if form.validate_on_submit():
        cur = conn.cursor(dictionary=True)  
        query = f"SELECT count(ticket_id) as seat_total FROM ticket NATURAL JOIN flight where flight_num = '{flight_num}' and NOT EXISTS(SELECT * FROM purchases WHERE purchases.ticket_id = ticket.ticket_id)"
        cur.execute(query)
        seat_total = cur.fetchone()
        cur.close()
        
        # this is the newly updated seat info
        cur = conn.cursor(dictionary=True)  
        query = f"SELECT count(ticket_id) as all2 FROM ticket NATURAL JOIN flight WHERE flight_num = '{flight_num}' GROUP BY flight_num"
        cur.execute(query)
        all2 = cur.fetchone()
        cur.close()
        print("Updated")

        # update customer and agent instances from this session
        customer = form.customer.data
        form.agent.data = agent = session['agent_id']

        # displaying all available flights
        cur = conn.cursor(dictionary=True)  
        query_available = "SELECT * FROM ticket WHERE flight_num = '{}' AND NOT EXISTS (SELECT * FROM purchases WHERE purchases.ticket_id = ticket.ticket_id)"
        cur.execute(query_available.format(flight_num))
        result = cur.fetchall()

        # successfully purchased ticket UI result
        if len(result) == 0:
            flash("Ticket not available", "Danger")
            cur.close()
        else:
            airline_name = result[0]["airline_name"]
            flight_num = result[1]["flight_num"]
            ticket_id = result[2]["ticket_id"]

            # grab agent
            cur = conn.cursor(dictionary=True)  
            query_agent_airline = "SELECT * FROM booking_Agent NATURAL JOIN ba_works_For WHERE booking_agent_id = '{}' AND airline_name = '{}'"
            cur.execute(query_agent_airline.format(agent, airline_name))
            works_for = cur.fetchall()
            print(works_for)

            # do I need to verify customer?
            cur = conn.cursor(dictionary=True)  
            query_find_customer = "SELECT * FROM customer WHERE email = '{}'"
            cur.execute(query_find_customer.format(customer))
            found_customer = cur.fetchall()

            if agent is not None and len(works_for) == 0:
                flash("You are not a verified Booking Agent for this airline.", "Danger")
            else:
                if len(found_customer) == 0:
                    flash("Customer ID not found.", "Danger")
                else:
                    date = datetime.date.today()
                    query = f"INSERT INTO purchases VALUES ('{ticket_id}', '{flight_num}', '{customer_email}', '{booking_agent_email}', '{date}')"
                    cur.execute(query)
                    conn.commit()
                    flash(f'User {session["email"]} purchased ticket No. {ticket_id} from {flight_num} at {airline_name} through booking agent {booking_agent_email}.', 'Success')
                    cur.close()
                    return redirect(url_for('home'))
    return render_template("purchasing_tickets_for.html", form = form, flight = flight, remaining_seats = remaining_seats, all2 = all2)

# view agent's commissions
@agent.route('/view_commissions', methods = ['GET', 'POST'])
def view_commissions():
    form_view_commissions = forms.ViewCommissionsForm()
    
    # getting dates
    if form_view_commissions.start.data == None:
        start = datetime.date.today() - relativedelta(years = 1)
    else:
        start = form_view_commissions.start.data

    if form_view_commissions.end.data == None:
        end = datetime.date.today()
    else:
        end = form_view_commissions.end.data

    # total amount of commission 
    cur = conn.cursor(dictionary=True)  
    query = f"SELECT SUM(price)*0.1 AS commissions_sum FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id = '{session['agent_id']} AND purchase_date >= '{start_date}' AND purchase_date <= '{end_date}'"
    cur.execute(query)
    sum_commissions = cur.fetchone()['commmissions_sum']
    cur.close()
    
    # total number of commissions
    cur = conn.cursor(dictionary=True)  
    query = f"SELECT COUNT(*) AS ticket_count FROM purchases NATURAL JOIN ticket WHERE booking_agent_id = '{session['agent_id']}' AND purchase_date >= '{start_date}' AND purchase_date <= '{end_date}'"
    cur.execute(query)
    num_tickets = cur.fetchone()['ticket_count']
    cur.close()

    # avg commission
    if commissions_sum = 0:
        print("No commissions")
    else:
        commissions_avg = float(sum_commissions)/float(num_tickets)
    
    print(num_tickets, sum_commissions, commissions_avg)
    return render_template('view_comissions.html', form_view_commissions = form_view_commissions, num_tickets = num_tickets, sum_commissions = sum_commissions, commissions_avg = commissions_avg)

# view top customers
@agent.route('/view_top_customers', methods = ['GET', 'POST'])
def view_top_customers():
    # top 5: # of tickets purchased in last 6 months from this booking agent
    cur = conn.cursor(dictionary=True)  
    query - f"SELECT customer_email, COUNT(*) AS ticket_count FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id = '{session['agent_id']} AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) GROUP BY customer_email ORDER BY ticket_count DESC LIMIT 5"
    cur.execute(query)
    top_5_ticket_count = cur.fetchall()
    cur.close()

    temp = {'customer_email': [], 'ticket_count': []}
    for i in range(5):
        if i < len(top_5_ticket_count):
            customer = top_5_ticket_count[i]
            temp['customer_email'].append(customer['customer_email'])
            temp['ticket_count'].append(customer['ticket_count'])
        else:
            temp['customer_email'].append("Null")
            temp['ticket_count'].append(0)
    top_5_ticket_count = temp
    print(top_5_ticket_count)

    # top 5: amount of commission received in last yr
    cur = conn.cursor(dictionary=True)  
    query = f"SELECT custoemr_email, SUM(price)*0.1 AS commission_amt FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id = '{session['agent_id']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTHS) GROUP BY customer_email ORDER BY commission_amt DESC LIMIT 5"
    cur.execute(query)
    top_5_commission_amt = cur.fetchall()
    cur.close()

    temp = {'customer_email': [], 'commission_amt': []}
    for i in range(5):
        if i < len(top_5_commission_amt):
            customer = top_5_commission_amt[i]
            temp['customer_email'].append(customer['customer_email'])
            temp['commission_amt'].append(customer['commission_amt'])
        else:
            temp['customer_email'].append("Null")
            temp['commission_amt'].append(0)
        top_5_commission_amt = temp
        print(top_5_commission_amt)

    return render_template('view_top_customers.html', top_5_ticket_count = json.dumps(top_5_ticket_count), top_5_commission_amt = json.dumps(top_5_commission_amt))
