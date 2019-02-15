import os
import re
import json
from pprint import pprint
from app import db, create_app
from app.models import State, Lga


basedir = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(basedir,'state_lga.json'), 'r') as json_file:
    content = json_file.read()
my_collection = json.loads(content)

state_names = [re.sub(' State', '', x['state']['name']) for x in my_collection]

all_lga_object = [x['state']['locals'] for x in my_collection]

all_lga_list = list()

for lga_object in all_lga_object:
    all_lga_list.append([x['name'] for x in lga_object])

state_lga_dict = dict(zip(state_names, all_lga_list))

# creating the application
app = create_app()

# Making a db query inside the application context
with app.app_context():
    for state, lgas in state_lga_dict.items():
        s = State(state)
        s.lgas = [Lga(lga) for lga in lgas]
        db.session.add(s)
    db.session.commit()
    print(State.query.all())