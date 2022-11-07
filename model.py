"""All SQLAlchemy classes defined here!"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String, nullable=False)

    ratings = db.relationship("Rating", back_populates = "user")
    favorites = db.relationship("Favorite", back_populates = "user")


    def __repr__(self):
        """Translates the string into useful and readble information."""

        return f"<User user_id={self.user_id} email={self.email}>"

class Rating(db.Model):
    """A restaurant rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    # the unique_restaurant_id will come from the Yelp API return for that specific restaurant
    unique_restaurant_id = db.Column(db.String, db.ForeignKey("restaurants.unique_restaurant_id"))
    comment = db.Column(db.Text)

    user = db.relationship("User", back_populates = "ratings")
    restaurant = db.relationship("Restaurant", back_populates = "ratings")

    def __repr__(self):
        """Translates the string into useful and readble information."""

        return f"<Rating rating_id={self.rating_id} score={self.score}>"

class Favorite(db.Model):
    """A favorited/saved restaurant."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    unique_restaurant_id = db.Column(db.String, db.ForeignKey("restaurants.unique_restaurant_id"))
    

    user = db.relationship("User", back_populates = "favorites")
    restaurant = db.relationship("Restaurant", back_populates = "favorites")

    def __repr__(self):
        """Translates the string into useful and readble information."""

        # Get name of restaurant by using magin key attribute restaurant (line 55) to get name BUT still connecting tables with unique_restaurant_id.
        return f"<Favorite favorite_id={self.favorite_id} name={self.restaurant.name}>"

class Restaurant(db.Model):
    """A restaurant."""

    __tablename__ = "restaurants"

    unique_restaurant_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)   
    address = db.Column(db.String) 
    phone_number = db.Column(db.String)
    rest_photo = db.Column(db.String)

    favorites = db.relationship("Favorite", back_populates = "restaurant")
    ratings = db.relationship("Rating", back_populates = "restaurant")


    def __repr__(self):
        """Translates the string into useful and readble information."""

        return f"<Restaurant unique_restaurant_id={self.unique_restaurant_id} name={self.name}>"
    

def connect_to_db(flask_app, db_uri="postgresql:///project",echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    # TURNED ECHO OFF BC TERMINAL CONFUSING
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
