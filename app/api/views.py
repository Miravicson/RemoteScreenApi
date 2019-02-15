from flask import render_template, request, jsonify
from app import db
from app.models import (Location, Update, State, Lga)
from app.schema import (state_schema, states_schema,lga_schema, lgas_schema, location_schema, locations_schema)


from . import bp






@bp.route('/api/state', methods=['GET'])
def get_states():
    all_states = State.query.all()
    return jsonify(states_schema.dump(all_states).data)

@bp.route('/api/state/<int:id>', methods=['GET'])
def state_detail(id):
    state = State.query.get(id)
    return jsonify(state_schema.dump(state).data)


@bp.route('/api/lga', methods=['GET'])
def get_lgas():
    all_lgas = Lga.query.all()
    return jsonify(lgas_schema.dump(all_lgas).data)

@bp.route('/api/lga/<int:id>', methods=['GET'])
def lga_detail(id):
    lga = Lga.query.get(id)
    return jsonify(lga_schema.dump(lga).data)

@bp.route('/api/location', methods=['GET'])
def get_locations():
    all_locations = Location.query.all()

    return jsonify(locations_schema.dump(all_locations).data)


@bp.route('/api/location/<int:id>', methods=['GET'])
def location_detail(id):
    location = Location.query.get(id)
    return jsonify(location_schema.dump(location).data)

@bp.route('/api/location', methods=['POST'])
def post_location():
    data = request.get_json(force=True)
    location = Location(name=data['name'], lga_id=data['lga_id'])
    db.session.add(location)
    db.session.commit()
    return jsonify(location_schema.dump(location).data)

@bp.route('/api/location/<int:id>', methods=['PUT'])
def update_location(id):
  location = Location.query.get(id)
  data = request.get_json(force=True)
  location.name = data['name']
  location.lga_id = data['lga_id']
  db.session.add(location)
  db.session.commit()
  return jsonify(location_schema.dump(location).data)

@bp.route('/api/location/<int:id>', methods=['DELETE'])
def delete_location(id):
  location = Location.query.get(id)
  db.session.delete(location)
  db.session.commit()
  return jsonify({'successful': True})
    


@bp.route('/api/update', methods=['GET'])
def get_update():
    all_updates = Update.query.all()
    return jsonify(all_updates)

@bp.route('/api/update', methods=['POST'])
def post_update():
    title = request.get_json()['title']
    PMS = request.get_json()['PMS']
    AGO = request.get_json()['AGO']
    DPK = request.get_json()['DPK']
    location_id = request.get_json()['state_id']
    new_update = Update(title, PMS, DPK, AGO, location_id)

    db.session.add(new_update)
    db.session.commit()
    return jsonify(new_update)


@bp.route('/api/recent', methods=["GET"])
def get_recent():

    return jsonify({"location": "Aba", "PMS": 40, "AGO": 60, "DPK": 80})




