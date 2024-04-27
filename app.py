from flask import Flask, render_template, request, session, url_for, redirect, Blueprint

#creates connection database
#LOL
from database import setup_db   #function for DB connections

#Bring in other endpoints
from api.general.general import general
from api.auth.auth import auth
from api.customer.customer import customer
from api.agent.agent import agent
from api.staff.staff import staff

#Initialize the app from Flask
def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Set secret key for session

    # Register blueprints
    app.register_blueprint(general)  # No prefix, common routes
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(customer, url_prefix='/user')
    app.register_blueprint(agent, url_prefix='/agent')
    app.register_blueprint(staff, url_prefix='/staff')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)































# @app.route('home')
# app.secret_key = 'your_secret_key'
# def home():
#     if 'username' in session:
#         username = session
#         return redirect(url_for('home'))
    
#     return render_template('login.html')   #if user not logged in, direct them to login in page

# @app.route('/flightInfo')
# def flightInfo():
#     connection = setup_db()
#     cur = connection.cursor(dictionary=True)  # All SQL is done through cursor

#     # See how many users there are
#     cur.execute("SELECT * FROM flight WHERE status = 'upcoming'")
#     results = cur.fetchall()  # Use fetchall() to get all rows, fetchone for one row
#     cur.close()

#     return render_template('flight.html', flights = results)


# @app.route('/logout')
# def logout():
#     session.pop('username')
#     return redirect('/')


# if __name__ == '__main__':
#     app.run(debug=True)
