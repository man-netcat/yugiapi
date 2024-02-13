import argparse
import os

from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Api, Resource
from yugitoolbox import OmegaDB, YugiDB

parser = argparse.ArgumentParser(description="Yu-Gi-Oh! Database REST Api")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
args = parser.parse_args()

app = Flask(__name__)
api = Api(app)
app.debug = args.debug


class CardResource(Resource):
    def get(self):
        request.args = {k.casefold(): v.casefold() for k, v in request.args.items()}
        cards = active_db.get_cards_by_values(request.args)
        cards_data = [card.to_dict() for card in cards]
        return jsonify(cards_data)


class ArchResource(Resource):
    def get(self):
        request.args = {k.casefold(): v.casefold() for k, v in request.args.items()}
        archetypes = active_db.get_archetypes_by_values(request.args)
        archetypes_data = [archetype.to_dict() for archetype in archetypes]
        return jsonify(archetypes_data)


class SetResource(Resource):
    def get(self):
        request.args = {k.casefold(): v.casefold() for k, v in request.args.items()}
        sets = active_db.get_sets_by_values(request.args)
        sets_data = [set.to_dict() for set in sets]
        return jsonify(sets_data)


class RenderCardResource(Resource):
    def get(self, card_id):
        if not os.path.exists(f"static/renders/{card_id}.png"):
            card = active_db.get_card_by_id(card_id)
            card.render("static/renders")
        return send_from_directory("static", f"renders/{card_id}.png")


class NameResource(Resource):
    def get(self):
        jsondata = {
            "card_names": active_db.card_names,
            "arch_names": active_db.archetype_names,
            "set_names": active_db.set_names,
        }
        return jsonify(jsondata)


class ConnectionResource(Resource):
    def get(self):
        return jsonify({"active_db_name": active_db.name})

    def post(self):
        global active_db

        db_uri = request.args.get("db_uri")
        active_db = YugiDB(db_uri)
        return jsonify({"message": "Database connection successful"})


api.add_resource(CardResource, "/card_data")
api.add_resource(ArchResource, "/arch_data")
api.add_resource(SetResource, "/set_data")
api.add_resource(NameResource, "/names")
api.add_resource(RenderCardResource, "/render/<int:card_id>")
api.add_resource(ConnectionResource, "/connection")

if __name__ == "__main__":
    active_db = OmegaDB(update="auto")

    if args.debug:
        app.run(debug=args.debug, port=args.port)
    else:
        from waitress import serve

        serve(app, host="0.0.0.0", port=args.port)
