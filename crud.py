"""CRUD operations."""

from model import db, User, Rating, Favorite, Restaurant, connect_to_db

# User functions start here:

def create_user(email, password, display_name):
    """Create and return a new user with a display name."""

    user = User(email=email, password=password, display_name=display_name)

    return user

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

# Rating functions start here:

def create_rating(score, user_id, unique_restaurant_id):
    """Create and return a restaurant rating"""
    
    rating = Rating(score=score, user_id=user_id, unique_restaurant_id=unique_restaurant_id)

    return rating

# Favorite functions start here:
# Q. In terminal when checking the function, I need to db.add/db.commit before I can check if the object has been created
def create_favorite(user_id, unique_restaurant_id):
    """Create and return a favorite restaurant."""

    favorite = Favorite(user_id=user_id, unique_restaurant_id=unique_restaurant_id)

    return favorite


# Restaurant functions start here: 

def create_restaurant(unique_restaurant_id, name, address, phone_number, rest_photo):
    """Create and return a restaurant."""

    restaurant = Restaurant(unique_restaurant_id=unique_restaurant_id, name=name, address=address, phone_number=phone_number, rest_photo=rest_photo)

    return restaurant

def get_restaurants():
    """Return movies based on user preference."""

    # Make sure the right query for all restaurants that the API returned 
    return Restaurant.query.all()





if __name__ == '__main__':
    from server import app
    connect_to_db(app)