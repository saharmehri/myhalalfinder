from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
import requests
import urllib
import math

from urllib.parse import quote

app = Flask(__name__)
app.secret_key = os.environ['RANDOM_SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['YELP_KEY']


# Homepage
@app.route('/homepage')
def homepage():
    """View homepage"""

    return render_template('homepage.html')

# Realted to Restaurant Search
@app.route('/foodfinder')
def show_halal_food_finder_form():
    """Form for user to fill out to filter restaurants."""

    return render_template('preferences.html')

@app.route('/foodfinder/search')
def find_halal_food():
    """Search for halal food on Yelp"""

    # Request user input from form
    cuisine = request.args.get('cuisine')
    location = request.args.get('location')
    radius = request.args.get('radius')
    radius = int(radius) * 1609.34 # Converting miles to meters
    radius = math.floor(radius)

    # Setting payload to the values the user inputed to filter search results. Halal is a fixed parameter.
    payload = {'categories': ['halal', 'Halal'],
        'cuisine': cuisine.replace(' ', '+'),
        'location': location.replace(' ', '+'), 
        'radius': radius
        }

    # API key access to allow me to run API calls on Yelp
    url = '{0}{1}'.format('https://api.yelp.com', quote('/v3/businesses/search'.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }

    # Make a get request to GET the information in the params and attach to URL as a query string and save to `response`
    # When call `response` in interactive mode...Should get a `<Response [200]>` message meaning "successful request"! 
    response = requests.request('GET', url, headers=headers, params=payload)
    # Convert response to `.json`
    # # `.json` will parse any JSON contained in the response and return it as a Python dictionary
    response = response.json()

    print(response)

    # if cuisine:
    #     payload["cuisine"] = cuisine

    # if location:
    #     payload["location"] = location

    # if radius:
    #     payload["radius"] = radius

   

    # events = data['_embedded']['events']
    
    # Send information to new page (HTML) to view results.
    return render_template('homepage.html',
                          data=response)







# Related to creating login
@app.route('/create_login')
def create_login():
    """Create a login page. User wants to create a login."""

    return render_template('createlogin.html')

@app.route('/users', methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    display_name = request.form.get("display-name")

    user = crud.get_user_by_email(email)
    
    if user:
        flash(f"The email {email} already exists. Please try again.")
        return redirect("/create_login")
    else: 
        user = crud.create_user(email, password, display_name)
        db.session.add(user)
        db.session.commit()
        flash("Success! Please log in.")
    
        return redirect("/loginpage")

# Related to logging in 
@app.route('/loginpage')
def user_login_page():
    """User login page."""

    return render_template('login_page.html')

@app.route('/login', methods=["POST"])
def user_login():
    """Logs a user in with the information provided."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user: 
        if user.password == password:
            # add email to session to recognize and save
            session['user_email'] = user.email
            # flash message 'logged in'
            flash("Success! You are now logged in.")
            # redirect to user profile
            return render_template('my_profile.html')
        else: 
            flash("The password is incorrect. Please try again.")
            return redirect('/loginpage')
    else: 
        flash("The email is invalid. Please try again.")
        return redirect('/loginpage')






    




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
