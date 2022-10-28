"""Script to seed database"""

import os
from random import choice, randint
import json

import crud
import model
import server

os.system('dropdb project')
os.system('createdb project')

model.connect_to_db(server.app)
model.db.create_all()

# Crate 10 users and each user will make 10 ratings 
for n in range(10):
    email = f"user{n}@test.com"
    password = "test"
    display_name = f"_test{n}"

    user = crud.create_user(email, password, display_name)
    model.db.session.add(user)

    
model.db.session.commit()