from app import ma, db
from app.models import State, Lga, Location, Update


class LgaSchema(ma.ModelSchema):
    class Meta:
        model = Lga
    locations = ma.Nested('LocationSchema', many=True,
                          only=('id', 'slug_name', 'name'))


lgas_schema = LgaSchema(many=True, exclude=('locations', ))
lga_schema = LgaSchema()


class StateSchema(ma.ModelSchema):
    class Meta:
        model = State
    lgas = ma.Nested('LgaSchema', many=True, exclude=('state_id', 'locations'))


states_schema = StateSchema(many=True, exclude=('lgas',))
state_schema = StateSchema()


class LocationSchema(ma.ModelSchema):
    class Meta:
        model = Location
        fields = ('id', 'name', 'lga_id', 'slug_name', 'state', 'updates')
    updates = ma.Nested('UpdateSchema', many=True)
    state = ma.Nested('LgaSchema', only='lga_id.state.name')


locations_schema = LocationSchema(many=True, exclude=('updates', ))
location_schema = LocationSchema()


class UpdateSchema(ma.ModelSchema):
    class Meta:
        model = Update
    location = ma.Nested('LocationSchema', only=('id', 'name'))


updates_schema = UpdateSchema(many=True, exclude=('timestamp',))
update_schema = UpdateSchema()


class RecentSchema(ma.ModelSchema):
    class Meta:
        model = Update
        fields = ('title', 'PMS', 'DPK', 'AGO')


recent_schema = RecentSchema()


class StateLgaSchema(ma.ModelSchema):
    class Meta:
        model = State
    lgas = ma.Nested(LgaSchema, many=True)


class LocationUpdateSchema(ma.ModelSchema):
    class Meta:
        model = Location
    updates = ma.Nested(UpdateSchema, exclude=(
        'timestamp', 'location_id'), many=True)
    lga = ma.Nested('LgaSchema', only=('id', 'name'))


location_updates_schema = LocationUpdateSchema(
    many=True, exclude=('timestamp',))


class LgaLocationSchema(ma.ModelSchema):
    class Meta:
        model = Lga
    locations = ma.Nested(LocationSchema, many=True, exclude=('updates',))
    state = ma.Nested('StateSchema', only=('id', 'name'))


lga_locations_schema = LgaLocationSchema(many=True)


class LgaLocationUpdateSchema(ma.ModelSchema):
    class Meta:
        model = Lga
    locations = ma.Nested(LocationUpdateSchema,
                          many=True, exclude=('timestamp',))
    state = ma.Nested('StateSchema', only=('id', 'name'))


lga_location_updates_schema = LgaLocationUpdateSchema(many=True)
