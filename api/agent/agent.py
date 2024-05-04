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

agent = Blueprint('agent',__name__)

# viewing flights booked for customers
# Defaults will be showing all the upcoming flights operated by the airline he/she works for
# the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline he/she
# works for based range of dates, source/destination airports/city etc. He/she will be able to see all the
# customers of a particular flight.
@agent.route('/agent_profile', methods = ['GET', 'POST'])
def agent_profile():
    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    #query
    query = f"SELECT * FROM booking_agent NATURAL JOIN ticket WHERE booking_agent_id = '{session['agent_id']}'"
    cur.execute(query)
    purchased_for = cur.fetchall()
    cur.close()
    print(purchased_for)
    
    return render_template('agent_profile.html', purchased_for = purchased_for)

# view agent's commissions
@agent.route('/agent_view_commissions', methods = ['GET', 'POST'])
def view_commissions():
#     form_view_commissions = forms.ViewCommissionsForm()
    
#     # getting dates
#     if form_view_commissions.start.data == None:
#         start = datetime.date.today() - relativedelta(years = 1)
#     else:
#         start = form_view_commissions.start.data

#     if form_view_commissions.end.data == None:
#         end = datetime.date.today()
#     else:
#         end = form_view_commissions.end.data

#     # total amount of commission 
#     cur = conn.cursor(dictionary=True)  
#     query = f"SELECT SUM(price)*0.1 AS commissions_sum FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id = '{session['agent_id']} AND purchase_date >= '{start_date}' AND purchase_date <= '{end_date}'"
#     cur.execute(query)
#     sum_commissions = cur.fetchone()['commmissions_sum']
#     cur.close()
    
#     # total number of commissions
#     cur = conn.cursor(dictionary=True)  
#     query = f"SELECT COUNT(*) AS ticket_count FROM purchases NATURAL JOIN ticket WHERE booking_agent_id = '{session['agent_id']}' AND purchase_date >= '{start_date}' AND purchase_date <= '{end_date}'"
#     cur.execute(query)
#     num_tickets = cur.fetchone()['ticket_count']
#     cur.close()

#     # avg commission
#     if commissions_sum == 0:
#         print("No commissions")
#     else:
#         commissions_avg = float(sum_commissions)/float(num_tickets)
    
    # print(num_tickets, sum_commissions, commissions_avg)
    return render_template('agent_view_comissions.html') #form_view_commissions = form_view_commissions, num_tickets = num_tickets, sum_commissions = sum_commissions, commissions_avg = commissions_avg)

# view top customers
@agent.route('/view_top_customers', methods = ['GET', 'POST'])
def view_top_customers():
#     # top 5: # of tickets purchased in last 6 months from this booking agent
#     cur = conn.cursor(dictionary=True)  
#     query - f"SELECT customer_email, COUNT(*) AS ticket_count FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id = '{session['agent_id']} AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) GROUP BY customer_email ORDER BY ticket_count DESC LIMIT 5"
#     cur.execute(query)
#     top_5_ticket_count = cur.fetchall()
#     cur.close()

#     temp = {'customer_email': [], 'ticket_count': []}
#     for i in range(5):
#         if i < len(top_5_ticket_count):
#             customer = top_5_ticket_count[i]
#             temp['customer_email'].append(customer['customer_email'])
#             temp['ticket_count'].append(customer['ticket_count'])
#         else:
#             temp['customer_email'].append("Null")
#             temp['ticket_count'].append(0)
#     top_5_ticket_count = temp
#     print(top_5_ticket_count)

#     # top 5: amount of commission received in last yr
#     cur = conn.cursor(dictionary=True)  
#     query = f"SELECT custoemr_email, SUM(price)*0.1 AS commission_amt FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id = '{session['agent_id']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTHS) GROUP BY customer_email ORDER BY commission_amt DESC LIMIT 5"
#     cur.execute(query)
#     top_5_commission_amt = cur.fetchall()
#     cur.close()

#     temp = {'customer_email': [], 'commission_amt': []}
#     for i in range(5):
#         if i < len(top_5_commission_amt):
#             customer = top_5_commission_amt[i]
#             temp['customer_email'].append(customer['customer_email'])
#             temp['commission_amt'].append(customer['commission_amt'])
#         else:
#             temp['customer_email'].append("Null")
#             temp['commission_amt'].append(0)
#         top_5_commission_amt = temp
#         print(top_5_commission_amt)

    return render_template('agent_view_customers.html') #top_5_ticket_count = json.dumps(top_5_ticket_count), top_5_commission_amt = json.dumps(top_5_commission_amt))