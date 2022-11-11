from flask import Flask, render_template, request, flash, session, redirect
from model import Favorite, User, Restaurant, Rating, connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
import requests
import urllib
import math
import functools

from urllib.parse import quote

app = Flask(__name__)
app.secret_key = os.environ['RANDOM_SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['YELP_KEY']

# *********************************************************************

# Homepage
@app.route('/homepage')
def homepage():
    """View homepage"""

    return render_template('homepage.html')

# *********************************************************************

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

    # To send ALL information use:
    businesses = response['businesses']
    
    # Send information to new page (HTML) to view results.
    return render_template('search-results.html', businesses = businesses, results = response)


# *********************************************************************

# Related to Ratings:

@app.route("/leave_a_rating/<unique_restaurant_id>") 
def rating_form(unique_restaurant_id):
    """Form to leave a rating."""

    return render_template('rating_form.html', unique_restaurant_id=unique_restaurant_id)

@app.route("/add_a_rating", methods=["POST"])
def create_rating():
    """Create a rating for restaurant."""

    logged_in_email = session['user_email']
    
    if logged_in_email is None:
        flash("You must log in to add to favorites.", "error")
        return redirect("/loginpage")

    score = request.form.get("score")
    comment = request.form.get("comment")
    unique_restaurant_id = request.form.get("unique_restaurant_id")

    # query into session to get the user information 
    user = User.query.filter_by(email=session['user_email']).first()

    if crud.rating_exists(user.user_id, unique_restaurant_id):
        flash("Restaurant already rated.", "error")
    else:
        crud.create_rating(score, comment, user.user_id, unique_restaurant_id)

        flash("Rating added!", "success")

    return redirect("/all_favorites")

@app.route("/all_ratings/<unique_restaurant_id>")
def view_all_ratings(unique_restaurant_id):
    """View all the ratings for restaurant."""

    # user = User.query.filter_by(email=session['user_email']).first()

    restaurant = Restaurant.query.filter_by(unique_restaurant_id=unique_restaurant_id).first()

    all_ratings = crud.get_ratings(unique_restaurant_id)
    print(all_ratings)

    return render_template('view_ratings.html', all_ratings=all_ratings, unique_restaurant_id=unique_restaurant_id, restaurant=restaurant)

# *********************************************************************

# Related to Favorites:
# Create favorite
@app.route("/add_to_favorites", methods=["POST"]) 
def create_favorite():
    """Create a favorite."""
    
    logged_in_email = session['user_email']
    
    if logged_in_email is None:
        flash("You must log in to add to favorites.", "error")
        return redirect("/loginpage")
    
    
    name = request.form.get("name")
    address = request.form.get("location") 
    address2 = request.form.get("location2")
    address = address + address2 
    phone_number = request.form.get("phone")
    rest_photo = request.form.get("rest_photo")
    unique_restaurant_id = request.form.get("unique_restaurant_id")
    
    crud.create_restaurant(unique_restaurant_id, name, address, phone_number, rest_photo)
    # taking session user email 
    user = User.query.filter_by(email=session['user_email']).first()
    # user is user object from database (the session user email) and keying to get user_id

    if crud.favorite_exists(user.user_id, unique_restaurant_id):
        flash("Restaurant already in favorites.", "error")
    else:
        crud.create_favorite(user.user_id, unique_restaurant_id)
        flash(f"Added to favorites!", "success")

    return redirect("/all_favorites")

@app.route("/all_favorites")
def show_favorites(): 
    """Show all favorites."""

    logged_in_email = session.get('user_email')
    
    if logged_in_email is None:
        flash("You must log in to view favorites.", "error")
        return redirect("/loginpage")

    favorites = crud.get_favorites(session['user_email'])
    
    
    average_ratings = {}
    
    for favorite in favorites:
        average_ratings[favorite.unique_restaurant_id]=[]
        ratings = favorite.restaurant.ratings
        for rating in ratings:
            average_ratings[favorite.unique_restaurant_id].append(rating.score)

    for unique_restaurant_id in average_ratings:
        total_scores = len(average_ratings[unique_restaurant_id])
        if total_scores == 0:
            average_ratings[unique_restaurant_id] = "No ratings yet"
        else:
            sum_of_scores = functools.reduce(lambda a,b: a+b, average_ratings[unique_restaurant_id])
            average = sum_of_scores/total_scores
            average_ratings[unique_restaurant_id]= average
    print(average_ratings)

    return render_template("favorites.html", favorites=favorites, average_ratings=average_ratings)

# Related to line 72 of crud.py
@app.route("/remove-favorite/<unique_restaurant_id>")
def remove_favorite(unique_restaurant_id):
    """Removes a favorite from list of favorites."""
   
    user = User.query.filter_by(email=session['user_email']).first()

    crud.delete_favorite(user.user_id, unique_restaurant_id) 
    flash("Favorite removed!", "success")

    return redirect('/all_favorites')

# *********************************************************************

# Related to creating login
# @app.route('/create_login')
# def create_login():
#     """Create a login page. User wants to create a login."""

#     return render_template('createlogin.html')

@app.route('/users', methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    display_name = request.form.get("display-name")

    user = crud.get_user_by_email(email)
    
    if user:
        flash(f"The email {email} already exists. Please try again.", "error")
        return redirect("/create_login")
    else: 
        user = crud.create_user(email, password, display_name)
        db.session.add(user)
        db.session.commit()
        flash("Success! Please log in.", "success")
    
        return redirect("/loginpage")

# *********************************************************************

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
            flash("Success! You are now logged in.", "success")
            # redirect to user profile
            return redirect('/homepage')
        else: 
            flash("The password is incorrect. Please try again.", "error")
            return redirect('/loginpage')
    else: 
        flash("The email is invalid. Please try again.", "error")
        return redirect('/loginpage')

# *********************************************************************

# Related to logging out

@app.route('/logout')
def logging_out():
    """Logs user out of account."""
    
    if 'user_email' in session:
        flash("You have been logged out succesfully!", "success")
        session.pop('user_email')
    
    return redirect('/homepage')






if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)







# USE WHEN TRYING TO NEST THROUGH businesses DICTIONARY 
    # print(response) -> see what the .json file holds
    # print(response.keys()) -> see the keys within the response data
    # print('********' *10) -> helpdul divider 
# for rest in response['businesses']:
#         for key,value in rest.items():
#             if rest.keys() == 'id':
#                 unique_restaurant_id = rest['id']
#             elif rest.keys() == 'name':
#                 name = rest['name']
#             elif rest.keys() == ''
#             print(key,value)