![Logo](/static/css/logo.JPG)
By Sahar Mehri | sahar.mehri.ca@gmail.com | [Watch the demo!](https://www.youtube.com/watch?v=lUfTB5bF_xg)

GIF of app (GIF)

Table of Contents 
List all of the headings 
Tech Stack 
About 
Features
Data Model
Looking Ahead

#Tech Stack 
Frontend: JavaScript | jQuery | HTML5 | CSS | Bootstrap
Backend: Python3 | Flask | SQLAlchemy | Jinja2
APIs: Cloudinary | Twilio | GoogleMaps | Chart.js
Database: PostgreSQL

#About 
Do you also struggle finding halal restaurants? My Halal Finder is a halal restaurant search engine created to make the hunt for halal restaurants easy, concise, and in one location. Focusing on user experience, My Halal Finder filters search results based on cuisine, location and radius. Users also have the option to save restaurants and leave a rating to help out other fellow halal eaters! 

#Testing 

#Features
##Login and Registration 
The user has the option to create an account to favorite restaurants for future reference and to leave a rating. I used SQL and postgreSQL to create users, then SQLAlchemy to query for each user to make sure there are no existing users. 

INSERT GIF OF REGISTERING/LOGGING IN 

##Search Halal Foods
To search for halal restaurants, I used the Yelp API with a “halal” default category to ensure only the return of halal restaurants. Users are required to indicate the cuisine, location and distance which I used to filter the rest of the content. 

##Favorite A Restaurant
After logging in, a user can also favorite a restaurant for future reference. I used the Yelp API and Yelp business ID to create favorites for each favorite restaurant and displayed them as cards using Jinja. Then I used a query to ensure the restaurant is not a repeat add to favorites. 

##Leave Rating
Logged in users also have the ability to leave a rating for a restaurant. The user fills out the form, creating a rating. Using SQLAlchemy, I filter through all user ratings for the specific restaurant to ensure there are no duplicates. I also used Jinja to display the average ratings of each restaurant in a star format. 

##Update Rating
Finally, a user can update a restaurant rating. Here I used an event listener to create an AJAX call. When a user clicks the “update review” button, it triggers a modal popup and the user can update the review without refreshing the page.  

#Data Model
Picture of data model

#Looking Ahead
Moving forward, I plan to make edits to my API call to ensure only the cuisine indicated by the user is resulting. I also want to add an option where users can invite friends to visit the restaurant. A link would be sent to the friend group via text and everyone inputs their current location. A map will then display everyone's location in relation to the restaurant. 

#Meet the Developer
Previously a pre-Physician Assistant candidate, I was initially planning on pursuing a career as an advanced provider in healthcare. After hitting a few career bumps in 2021, I finally decided to cave in and explore my passion for tech and web development. 

Aside from coding and healthcare, in my free time I love to travel, shop, eat, and sing Afghan songs!

Connect with [Sahar Mehri](https://www.linkedin.com/in/saharmehri/) on Linkedin! 

#Install
##Running My Halal Finder
1. Clone this repository:
`git clone https://github.com/saharmehri/myhalalfinder.git`

2. Optional: Create and activate a virtual environment:
```
pip3 install virtualenv
virtualenv env
source env/bin/activate
```

3. Install dependencies:
`pip3 install -r requirements.txt`

4. Create environmental variables to hold your API keys in a secrets.sh file. You'll need to create your own Yelp API key:
```
export YELP_CLIENT_ID="after creating an account on the Yelp developer website, you'll be given a client id, paste that here"
export YELP_KEY="you'll also be given a Yelp key, paste that here for safe keeps"
```

5. Create your database & seed sample data:
```
createdb myhalalfinder
python3 seed.py
```

6. Run the app on localhost:
```
source secrets.sh
python3 server.py
```
