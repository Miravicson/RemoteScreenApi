from app import ma, db
from app.models import State, Lga, Location, Update


class StateSchema(ma.ModelSchema):
    class Meta:
        model = State

    # Smart hyperlinking
    links = ma.Hyperlinks({
        'self': ma.URLFor('api.state_detail', id='<id>'),
        'collection': ma.URLFor('api.get_states')
    })


states_schema = StateSchema(many=True)
state_schema = StateSchema()


class LgaSchema(ma.ModelSchema):
    class Meta:
        model = Lga
    links = ma.Hyperlinks({
        'self': ma.URLFor('api.lga_detail', id='<id>'),
        'collection': ma.URLFor('api.get_lgas')
    })


lgas_schema = LgaSchema(many=True)
lga_schema = LgaSchema()


class LocationSchema(ma.ModelSchema):
    class Meta:
        model = Location
        fields = ('id', 'name', 'lga_id', 'updates', 'slug_name')
    # links = ma.Hyperlinks({
    #     'self': ma.URLFor('api.lga_detail', id='<id>'),
    #     'collection': ma.URLFor('api.get_lgas')
    # })


locations_schema = LocationSchema(many=True)
location_schema = LocationSchema()


class UpdateSchema(ma.ModelSchema):
    class Meta:
        model = Update


updates_schema = UpdateSchema(many=True)
update_schema = UpdateSchema()


class RecentSchema(ma.ModelSchema):
    class Meta:
        model = Update
        fields = ('title', 'PMS', 'DPK', 'AGO')


recent_schema = RecentSchema()
