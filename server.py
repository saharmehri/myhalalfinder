from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
import requests

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
