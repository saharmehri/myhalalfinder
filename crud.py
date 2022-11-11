"""CRUD operations."""

from model import db, User, Rating, Favorite, Restaurant, connect_to_db

# User functions start here:

def create_user(email, password, display_name):
    """Create and return a new user with a display name."""

    user = User(
            email=email, 
            password=password, 
            display_name=display_name
    )

    return user

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_by_id(user_id):
    """Return a user by that ID."""

    return User.query.get(user_id)

# *******************************************************************

# Rating functions start here:

def create_rating(score, comment, user_id, unique_restaurant_id):
    """Create and return a restaurant rating"""
    
    existing_rating = Rating.query.filter_by(user_id=user_id, unique_restaurant_id=unique_restaurant_id).first()

    if existing_rating:
        return existing_rating

    rating = Rating(
            score=score, 
            comment=comment,
            user_id=user_id, 
            unique_restaurant_id=unique_restaurant_id
    )

    db.session.add(rating)
    db.session.commit()
    
    return rating

def get_ratings(unique_restaurant_id):
    """Get all ratings for restaurant."""

    return Rating.query.filter_by(unique_restaurant_id=unique_restaurant_id).all()


# *******************************************************************

# Favorite functions start here:

def create_favorite(user_id, unique_restaurant_id):
    """Create and return a favorite restaurant."""

    existing_favorite = Favorite.query.filter_by(user_id=user_id, unique_restaurant_id=unique_restaurant_id).first()
    
    if existing_favorite:
        return existing_favorite

    favorite = Favorite(
            user_id=user_id, 
            unique_restaurant_id=unique_restaurant_id
    )

    db.session.add(favorite)
    db.session.commit()

    return favorite

def get_favorites(email):
    """Return all favorites for that email."""

    user = User.query.filter_by(email=email).first()

    return Favorite.query.filter_by(user_id=user.user_id).all()

# Related to line 125 of server.py
def delete_favorite(user_id, unique_restaurant_id):
    """Remove the favorite."""

    # user is not recognized on line 87
    # user = User.query.filter_by(user_id=user_id).first()

    restaurant = Favorite.query.filter_by(user_id=user_id, unique_restaurant_id=unique_restaurant_id).first()


    db.session.delete(restaurant)
    db.session.commit()

    return restaurant
    
# *******************************************************************

# Restaurant functions start here: 

def create_restaurant(unique_restaurant_id, name, address, phone_number, rest_photo):
    """Create and return a restaurant."""

    existing_restaurant = Restaurant.query.filter_by(unique_restaurant_id=unique_restaurant_id).first()
    
    if existing_restaurant:
        return existing_restaurant

    restaurant = Restaurant(
            unique_restaurant_id=unique_restaurant_id, 
            name=name, 
            address=address, 
            phone_number=phone_number, 
            rest_photo=rest_photo
    )

    db.session.add(restaurant)
    db.session.commit()

    return restaurant

def get_restaurants():
    """Return restaurants based on user preference."""

    # Make sure the right query for all restaurants that the API returned 
    return Restaurant.query.all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)