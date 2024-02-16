import argparse
import os

import markdown2
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

API_VERSION = "/api/v1"


class CardResource(Resource):
    def get(self):
        request.args = {k.casefold(): v.casefold() for k, v in request.args.items()}
        if not request.args:
            cards = active_db.cards
        else:
            cards = active_db.get_cards_by_values(request.args)
        cards_data = [card.to_dict() for card in cards]
        return jsonify(cards_data)


class ArchResource(Resource):
    def get(self):
        request.args = {k.casefold(): v.casefold() for k, v in request.args.items()}
        if not request.args:
            archetypes = active_db.archetypes
        else:
            archetypes = active_db.get_archetypes_by_values(request.args)
        archetypes_data = [archetype.to_dict() for archetype in archetypes]
        return jsonify(archetypes_data)


class SetResource(Resource):
    def get(self):
        request.args = {k.casefold(): v.casefold() for k, v in request.args.items()}
        if not request.args:
            sets = active_db.sets
        else:
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


api.add_resource(CardResource, f"{API_VERSION}/card_data")
api.add_resource(ArchResource, f"{API_VERSION}/arch_data")
api.add_resource(SetResource, f"{API_VERSION}/set_data")
api.add_resource(NameResource, f"{API_VERSION}/names")
api.add_resource(RenderCardResource, f"{API_VERSION}/render/<int:card_id>")


@app.route("/")
def homepage():
    with open("README.md", "r") as readme_file:
        readme_content = readme_file.read()

    readme_html = markdown2.markdown(readme_content)

    footer_html = '<footer><p>For more information, visit the <a href="https://github.com/man-netcat/yugiapi">official GitHub page</a>.</p></footer>'

    full_html = f"{readme_html}\n{footer_html}"
    return full_html


if __name__ == "__main__":
    active_db = OmegaDB(update="auto", debug=args.debug)

    if args.debug:
        app.run(debug=args.debug, port=args.port)
    else:
        from waitress import serve

        serve(app, host="0.0.0.0", port=args.port)
