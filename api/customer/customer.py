from flask import Flask, render_template, request, session, url_for, redirect, Blueprint, flash     #make sure to import from flask
from flask_bcrypt import Bcrypt
import forms
from database import setup_db

import datetime
from dateutil.relativedelta import relativedelta
import json
from matplotlib import pyplot as plt
import io
import base64

customer = Blueprint('customer',__name__)

# Default view will be total amount of money spent in the past year and a bar chart
# showing month wise money spent for last 6 months. He/she will also have option to specify a range of dates to
# view total amount of money spent within that range and a bar chart showing month wise money spent within
# that range. (Bar chart is optional, you can choose to represent the data anyway you like)

### Customer Profile contains all his flight information + spending information
@customer.route('/customer_profile', methods=['GET', 'POST'])
def customer_profile():

    form = forms.TimeInterval()

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
    else:
        # Set default range for the past six months if not specified
        end_date = datetime.date.today()
        start_date = end_date - relativedelta(months=6)

    conn = setup_db()
    cur = conn.cursor(dictionary=True)

    #for customer view flights
    cur.execute("""
        SELECT f.airline_name, f.flight_num, f.departure_airport, f.departure_time, f.arrival_airport, f.arrival_time, f.price, t.ticket_id
        FROM purchases p
        JOIN ticket t ON p.ticket_id = t.ticket_id
        JOIN flight f ON t.flight_num = f.flight_num AND t.airline_name = f.airline_name
        WHERE p.customer_email = %s AND f.departure_time BETWEEN %s AND %s
    """, (session['email'], start_date, end_date))
    flights = cur.fetchall()

    #Get spending data
    cur.execute("""
        SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, SUM(price) AS total_spending
        FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
        WHERE customer_email = %s AND purchase_date BETWEEN %s AND %s
        GROUP BY year, month
        """, (session['email'], start_date, end_date))
    customer_spending = cur.fetchall()
    cur.close()

    #Create matplot lib
    dates = []
    spents = []
    current_date = start_date
    while current_date <= end_date:
        key = f"{current_date.year}-{current_date.month}"
        dates.append(key)
        # Find the spending for each month, defaulting to 0 if no spending recorded
        total_spending = next((item['total_spending'] for item in customer_spending if f"{item['year']}-{item['month']}" == key), 0)
        spents.append(total_spending)
        current_date += relativedelta(months=1)

    fig, ax = plt.subplots()
    ax.bar(dates, spents, color='blue')
    ax.set(title='Monthly Spending', xlabel='Month', ylabel='Spending ($)')
    ax.set_xticklabels(dates, rotation=45)
    plt.tight_layout()

    #Save plot
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('customer_profile.html', flights=flights, form=form, plot_url=plot_url)