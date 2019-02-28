from flask import render_template, request, jsonify
from app import db
from app.models import (Location, Update, State, Lga)
from app.schema import (state_schema, states_schema, lga_schema, lgas_schema,
                        location_schema, locations_schema, update_schema, updates_schema, recent_schema, location_updates_schema, lga_locations_schema,
                        lga_location_updates_schema)


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
    return jsonify(updates_schema.dump(all_updates).data)


@bp.route('/api/update', methods=['POST'])
def post_update():
    title = request.get_json()['title']
    PMS = request.get_json()['PMS']
    AGO = request.get_json()['AGO']
    DPK = request.get_json()['DPK']
    location_id = request.get_json()['location_id']
    new_update = Update(title, PMS, DPK, AGO, location_id)

    db.session.add(new_update)
    db.session.commit()
    return jsonify(update_schema.dump(new_update).data)


@bp.route('/api/update/<int:id>', methods=['DELETE'])
def delete_update(id):
    update = Update.query.get(id)
    db.session.delete(update)
    db.session.commit()
    return jsonify({'successful': True})


@bp.route('/api/recent/<string:location_slug>', methods=["GET"])
def get_recent(location_slug):
    location = Location.query.filter(
        Location.slug_name == location_slug).first()
    update = location.updates[-1]
    return jsonify(recent_schema.dump(update).data)


@bp.route('/api/lga-locations', methods=['GET'])
def lga_with_locations():
    lga_locations = Lga.query.all()

    return jsonify(lga_locations_schema.dump(lga_locations).data)


@bp.route('/api/location-updates', methods=['GET'])
def location_with_updates():
    location_updates = Location.query.all()
    return jsonify(location_updates_schema.dump(location_updates).data)


@bp.route('/api/lga-location-updates', methods=['GET'])
def lga_location_update():
    lga_location_updates = Lga.query.all()
    return jsonify(lga_location_updates_schema.dump(lga_location_updates).data)


@bp.route('/api/average-price', methods=['GET'])
def average_price():
    locations = Location.query.all()
    last_update_per_location = (
        location.updates[-1] for location in locations if len(location.updates) > 0)
    prices = ((update.PMS, update.AGO, update.DPK)
              for update in last_update_per_location)
    PMS = 0
    AGO = 0
    DPK = 0
    n = 0
    for price in prices:
        PMS = PMS + price[0]
        AGO = AGO + price[1]
        DPK = DPK + price[2]
        n = n + 1
    average = {}
    if n != 0:
        average = {'PMS': round(PMS / n, 2),
                   'AGO': round(AGO / n), 'DPK': round(DPK / n, 2)}

    return jsonify(average)


@bp.route('/api/location-recent', methods=['GET'])
def location_recent_update():
    locations = Location.query.all()
    recents = (l.updates[-1] for l in locations if len(l.updates) > 0)

    return jsonify(updates_schema.dump(recents).data)
