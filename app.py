from flask import Flask, render_template, request, session, url_for, redirect, jsonify

#creates connection database
from database import setup_db   #function for DB connections

#Initialize the app from Flask
app = Flask(__name__)

#### what is session object???

@app.route('/')
def index():
    if 'username' in session:
        username = session
        return redirect(url_for('home'))
    
    return render_template('login.html')   #if user not logged in, direct them to login in page

@app.route('/login')    
def login():
    return 'login!'

@app.route('/register') 
def register():
    return 'register!'

@app.route('/homepage')
def homepage():
    return 'homepage'

@app.route('/flightInfo')
def flightInfo():
    connection = setup_db()
    cur = connection.cursor(dictionary=True)  # All SQL is done through cursor

    # See how many users there are
    cur.execute("SELECT * FROM flight WHERE status = 'upcoming'")
    results = cur.fetchall()  # Use fetchall() to get all rows, fetchone for one row
    cur.close()

    return render_template('flight.html', flights = results)


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
