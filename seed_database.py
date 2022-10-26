"""Script to seed database"""

import os
import json

import crud
import model
import server

os.system('dropdb project')
os.system('createdb project')

model.connect_to_db(server.app)
model.db.create_all()

