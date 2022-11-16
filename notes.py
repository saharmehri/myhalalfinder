#Database:
# favorite the rest (refer to movie ratings)
# 1. crud functions, but invoking in server...create rest and add/commit to database -> make sure rest is not already in database (if ID already exists return existing rest)
# 2. crud functions, but invoking in server...user_id in session -> pull user_id, use to add favorite and add/commit to database
# 3. crud functions, but invoking in server...query that allows to query all favorites by user_id (will allow to display on user profile page) 
# can use looping to display 

# These are three different functions: create restaurant, get user by id, create favorite
# And then another for displaying the favorites in profile: get all favorites by user id

# 1. User clicks add to favorites 
# 2. Process to create a rest to save unique id begins:
# 3. checks if rest already exists, if yes -> go straight to favorite function & if no -> create a rest 
# 4. Process for create a favorite begins: 
# 5. check if user logged in: if yes -> take user_id to create favorite THEN check if rest already favorited: if yes -> flash(Already in favorites) and redirect to show all favorites... if no -> add to favorites database & if not logged in -> ask user to login 
#**********************************************
# 
#  @app.route("/create_restaurant", methods=["POST"])
# def create_favorite(unique_restaurant_id):
#     """Create a restaurant."""

#     logged_in_email = session.get("user_email")
#     # Get business info:
#     # unique_restaurant_id = Restaurant.query.get(unique_restaurant_id)
#     # name 
#     # address
#     # phone_number
#     # rest_photo 

#     if logged_in_email is None:
#         flash("You must log in to add to favorites.")
#         return redirect("/login_page.html")
#     else:
#         # Figuring out how to get user by user id here to create a favorite. 
#         user = crud.get_user_by_id(session['user_id'])

#         favorite = crud.create_favorite(user, unique_restaurant_id)
#         db.session.add(favorite)
#         db.session.commit()

#         flash(f"Added to favorites!")

#         # Redirects to page (HTML) with all favorites
#         return redirect("/all_favorites")

# Related to ratings
# @app.route("/leave-a-rating", methods=["POST"])
# def create_rating(unique_restaurant_id):
#     """Create a restaurant rating."""

#     logged_in_email = session.get("user_email")
#     rating_score = request.form.get("rating")

#     if logged_in_email is None:
#         flash("You must log in to rate a restaurant.")
#     elif not rating_score:
#         flash("Error: you didn't select a score for your rating.")
#     else:
#         user = crud.get_user_by_email(logged_in_email)
#         movie = crud.get_movie_by_id(movie_id)

#         rating = crud.create_rating(user, movie, int(rating_score))
#         db.session.add(rating)
#         db.session.commit()

#         flash(f"You rated this movie {rating_score} out of 5.")

#     # return redirect(f"/movies/{movie_id}")
#     return redirect("/movies")

# 
# Looping through .json file and getting pertinent information (key:value) pairs
    # for rest in response['businesses']:
    #     for key,value in rest.items():
    #         if key == 'id':
    #             unique_restaurant_id = value
    #         if key == 'name':
    #             name = value
    #         # Tried looping through location to get the display_address but kept getting error
    #         # if key == 'location':
    #         #     # loop through location to get display address
    #         #     for key,value in key.items():
    #         #         address = key['locations']['display_address']
    #         if key == 'dispay_phone':
    #             phone_number = value
    #         if key == 'image_url':
    #             rest_photo = value
    #         # Attemoted this way instead of line 81, but then getting UnboundLocalError: local variable 'phone_number' referenced before assignment
    #         address = rest['location']['display_address']
    


    # search-results looping without hidden tags and sending info via form
    #  <!-- {% for business in businesses %}
    #             <form method="GET" action="/foodfinder/search">
    #             <li>
    #                 <img src="{{ business.image_url }}" alt="Restaurant immage" width="300" height="300"> <br>
    #                 {{ business['name'] }} <br>
    #                 {{ business['location']['display_address'][0] }} <br>
    #                 {{ business['location']['display_address'][1] }} <br>
    #                 {{ business['display_phone'] }}<br>
    #                 Links should be red buttons
    #                 <a class="favorites" href="/add_to_favorites">Add to favorites</a>
    #                 <a class="rate" href="/leave-a-rating">Leave a rating</a>
    #                 <a class="directions" href="/go-to-restaurant">Go to restaurant</a>
    #             </li>
    #             </form>
            
    #             {% endfor %} -->

    #login page 
    <!-- ***************************************** -->
# <!-- <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
# <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
# <script src="//code.jquery.com/jquery-1.11.1.min.js"></script> -->
# <!------ Include the above in your HEAD tag ---------->

# <!-- {% endblock %}

# {% block body %}



# <div class="sidenav">
#          <div class="login-main-text">
#             <h2>Login</h2><br>
#             <p>Find halal restaurants near you.</p><br><br><br>
#             <p>By continuing, you agree to our terms and conditions.</p>
#          </div>
#       </div>
#       <div class="main">
#          <div class="col-md-6 col-sm-12">
#             <div class="create-login-form">
#                <form action="/login" method="POST">
#                   <div class="form-group">
#                      <label>Email</label>
#                      <input type="text" class="form-control" name= "email" placeholder="Email">
#                   </div>
#                   <div class="form-group">
#                      <label>Password</label>
#                      <input type="password" class="form-control" name= "password" placeholder="Password">
#                   </div> -->
#                   <!-- MAY NOT NEED THIS INFORMATION IF DISPLAY NAME IS SAVED ALREADY! -->
#                   <!-- <div class="form-group">
#                     <label>Username</label>
#                     <input type="text" class="form-control" name= "display-name" placeholder="Username">
#                  </div> -->
#                   <!-- <button type="submit" class="btn btn-black">Log in</button> -->
#                   <!-- <button type="submit" class="btn btn-secondary">Register</button> -->
#                <!-- </form>
#             </div>
#          </div>
#       </div>
# {% endblock %} -->



# favorites.html

# {% for i in range(1, 6) %}
#                     {% if average_ratings[favorite.unique_restaurant_id] >= i %}
#                         <span class="fa fa-star checked"></span>
#                     {% else %}
#                         <span class="fa fa-star"></span>
#                     {% endif %}
#                   {% endfor %} 