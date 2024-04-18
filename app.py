from flask import Flask, render_template, request, session, url_for, redirect, jsonify, Blueprint

#creates connection database
#LOL
from database import setup_db   #function for DB connections

#Initialize the app from Flask
app = Flask(__name__)

#### what is session object???


from api.auth.auth import auth_blueprint
from api.user.user import user_blueprint
from api.agent.agent import agent_blueprint
from api.staff.staff import staff_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(agent_blueprint, url_prefix='/agent')
    app.register_blueprint(staff_blueprint, url_prefix='/staff')
    return app




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
