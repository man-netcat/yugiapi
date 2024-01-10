from flask import Flask, jsonify, render_template, request
from flask_restful import Api, Resource
from waitress import serve
from yugitoolbox import OmegaDB, YugiDB

app = Flask(__name__)
api = Api(app)

db = None
db_type = None

DEBUG = True


class CardResource(Resource):
    def get(self):
        card_id = request.args.get("card_id", type=int)
        card = db.get_card_by_id(card_id)
        return card.to_dict()


class ArchetypeResource(Resource):
    def get(self):
        archetype_id = request.args.get("arch_id", type=int)
        archetype = db.get_archetype_by_id(archetype_id)
        return jsonify(archetype)


class SetResource(Resource):
    def get(self):
        set_id = request.args.get("set_id", type=int)
        set = db.get_set_by_id(set_id)
        return jsonify(set)


api.add_resource(CardResource, "/cards")
api.add_resource(ArchetypeResource, "/archetypes")
api.add_resource(SetResource, "/sets")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/set_connection", methods=["POST"])
def set_connection():
    global db
    db_type = request.form["db_type"]

    if db_type == "yugidb":
        connection_string = request.form["connection_string"]
        db = YugiDB(connection_string)
    elif db_type == "omegadb":
        db = OmegaDB(always_update=True)
    else:
        return render_template("error.html", error="Invalid database type")

    return render_template("dashboard.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
