from app import db, ma
from datetime import datetime


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    lgas = db.relationship('Lga', backref=db.backref(
        'state', lazy=True), cascade='all, delete-orphan', lazy=True)

    def __init__(self, name, lga=None):
        self.name = name
        if lga is None:
            self.lga = []
        else:
            self.lga = lga

    def __repr__(self):
        return '<State %r>' % self.name


class Lga(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    name = db.Column(db.String(16))
    locations = db.relationship('Location', backref=db.backref(
        'lga', lazy=True), cascade='all, delete-orphan', lazy=True)

    def __init__(self, name, locations=None, state_id=None):
        self.name = name
        self.state_id = state_id
        if locations is None:
            self.locations = []
        else:
            self.locations = locations

    def __repr__(self):
        return '<Lga %r>' % self.name


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lga_id = db.Column(db.Integer, db.ForeignKey('lga.id'), nullable=False)
    name = db.Column(db.String(200), unique=True)
    updates = db.relationship('Update', backref=db.backref(
        'location', lazy=True), cascade='all, delete-orphan', lazy=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name, updates=None, lga_id=None):
        self.name = name
        self.lga_id = lga_id
        if updates is None:
            self.updates = []
        else:
            self.updates = updates

    def __repr__(self):
        return '<Location %r>' % self.name


class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(db.Integer, db.ForeignKey(
        'location.id'), nullable=False)
    title = db.Column(db.String(16))
    PMS = db.Column(db.Integer)
    DPK = db.Column(db.Integer)
    AGO = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, title, PMS, DPK, AGO, location_id=1):
        self.title = title
        self.PMS = PMS
        self.DPK = DPK
        self.AGO = AGO
        self.location_id = location_id

    def __repr__(self):
        return '<Message %r>' % self.title


class UpdateSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('title', 'PMS', 'DPK', 'AGO')


update_schema = UpdateSchema()
updates_schema = UpdateSchema(many=True)


class StateSchema(ma.Schema):
    class Meta:
        fields = ('name', 'lgas')


state_schema = StateSchema()
states_schema = StateSchema(many=True)


class LocationSchema(ma.Schema):
    class Meta:
        fields = ('name', 'updates')


location_schema = LocationSchema()
locations_schema = LocationSchema()
