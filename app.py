from flask import Flask, render_template, request, session, requests, url_for, redirect, jsonify

#creates connection database
from database import setup_db   #function for DB connections

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
    return 'hello world!'

@app.route('/register') 
def register():
    return 'hello world!'

@app.route('/homepage')


### DB test endpoint
@app.route('/db-test')  # Test database connection
def test_db():
    try:
        connection = setup_db()
        cur = connection.cursor()  # All SQL is done through cursor

        # See how many users there are
        cur.execute("SELECT COUNT(*) FROM Users")
        result = cur.fetchone()  # This will be a tuple like (count,)
        cur.close()

        # Good practice to return JSON
        return jsonify({'number_of_users': result[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500






@app.route('logout')
def logout():
    session.pop('username')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
