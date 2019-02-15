from flask_restful import Resource
from flask import jsonify


class LgaResource(Resource):
    def get(self):
        return jsonify(Lga.query.all())
