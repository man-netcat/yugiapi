from abc import abstractmethod
import argparse
import os

import markdown2
from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Api, Resource
from yugitoolbox import OmegaDB

parser = argparse.ArgumentParser(description="Yu-Gi-Oh! Database REST Api")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
args = parser.parse_args()

app = Flask(__name__)
api = Api(app)
app.debug = args.debug

API_VERSION = "/api/v1"


class ObjectResource(Resource):
    def get(self):
        args = {k.casefold(): v.casefold() for k, v in request.args.items()}

        try:
            if not {k: v for k, v in args.items() if k != "get"}:
                items = self.get_all_items()
            else:
                items = self.get_items_by_values(args)
        except Exception as e:
            return jsonify({"error": f"{type(e)}: {e}"})

        if "get" in args:
            keys = args["get"].split(",")
            items_data = [
                {k: v for k, v in item.to_dict().items() if k in keys or k == "name"}
                for item in items
            ]
        else:
            items_data = [item.to_dict() for item in items]

        return jsonify(items_data)

    @abstractmethod
    def get_all_items(self) -> list:
        pass

    @abstractmethod
    def get_items_by_values(self, args) -> list:
        pass


class CardResource(ObjectResource):
    def get_all_items(self):
        return active_db.cards

    def get_items_by_values(self, args):
        return active_db.get_cards_by_values(args)


class ArchResource(ObjectResource):
    def get_all_items(self):
        return active_db.archetypes

    def get_items_by_values(self, args):
        return active_db.get_archetypes_by_values(args)


class SetResource(ObjectResource):
    def get_all_items(self):
        return active_db.sets

    def get_items_by_values(self, args):
        return active_db.get_sets_by_values(args)


class RenderCardResource(Resource):
    def get(self, card_id):
        if not os.path.exists(f"static/renders/{card_id}.png"):
            card = active_db.get_card_by_id(card_id)
            card.render("static/renders")
        return send_from_directory("static", f"renders/{card_id}.png")


api.add_resource(CardResource, f"{API_VERSION}/card_data")
api.add_resource(ArchResource, f"{API_VERSION}/arch_data")
api.add_resource(SetResource, f"{API_VERSION}/set_data")
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
    active_db = OmegaDB(update="auto")

    if args.debug:
        app.run(debug=args.debug, port=args.port)
    else:
        from waitress import serve

        serve(app, host="0.0.0.0", port=args.port)
