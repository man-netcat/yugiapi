import argparse

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from yugitoolbox import OmegaDB, YugiDB

parser = argparse.ArgumentParser(description="Yu-Gi-Oh! Database REST Api")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
args = parser.parse_args()

app = Flask(__name__)
api = Api(app)
app.debug = args.debug

omegadb = OmegaDB(update="auto", debug=args.debug)
active_db: YugiDB = omegadb


class CardResource(Resource):
    def get(self):
        cards = active_db.get_cards_by_values(request.args)
        cards_data = [card.to_dict() for card in cards]
        return jsonify(cards_data)


class ArchResource(Resource):
    def get(self):
        archetypes = active_db.get_archetypes_by_values(request.args)
        archetypes_data = [archetype.to_dict() for archetype in archetypes]
        return jsonify(archetypes_data)


class SetResource(Resource):
    def get(self):
        sets = active_db.get_sets_by_values(request.args)
        sets_data = [set.to_dict() for set in sets]
        return jsonify(sets_data)


class RenderResource(Resource):
    def get(self, card_id):
        try:
            card = active_db.get_card_by_id(card_id)
            out_path = card.render("static/renders")
            return jsonify({"path": out_path})
        except Exception as e:
            return jsonify({"error": str(e)})


class ConnectionResource(Resource):
    def get(self):
        return jsonify({"active_db_name": active_db.name})

    def post(self):
        global active_db

        try:
            print(request.args)
            db_uri = request.args.get("db_uri")
            print(db_uri)
            active_db = YugiDB(db_uri)
            return jsonify({"message": "Database connection successful"})
        except Exception as e:
            return jsonify({"error": str(e)})


api.add_resource(CardResource, "/card_data")
api.add_resource(ArchResource, "/arch_data")
api.add_resource(SetResource, "/set_data")
api.add_resource(RenderResource, "/render/<int:card_id>")
api.add_resource(ConnectionResource, "/set_connection")

if __name__ == "__main__":
    if args.debug:
        app.run(debug=args.debug, port=args.port)
    else:
        from waitress import serve

        serve(app, host="0.0.0.0", port=args.port)