import argparse

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_restful import Api, Resource
from yugitoolbox import OmegaDB, YugiDB

parser = argparse.ArgumentParser(description="YuGiOh API Application")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
parser.add_argument(
    "--port", type=int, default=5000, help="Port number to run the server on"
)
args = parser.parse_args()

app = Flask(__name__)
api = Api(app)
app.debug = args.debug

omegadb = OmegaDB(update="auto", debug=args.debug)
currentdb = omegadb


class CardResource(Resource):
    def get(self):
        cards = currentdb.get_cards_by_values(request.args)
        cards_data = [card.to_dict() for card in cards]
        return jsonify(cards_data)


class ArchResource(Resource):
    def get(self):
        archetypes = currentdb.get_archetypes_by_values(request.args)
        archetypes_data = [archetype.to_dict() for archetype in archetypes]
        return jsonify(archetypes_data)


class SetResource(Resource):
    def get(self):
        sets = currentdb.get_sets_by_values(request.args)
        sets_data = [set.to_dict() for set in sets]
        return jsonify(sets_data)


class ConnectionResource(Resource):
    def post(self):
        global currentdb
        db_type = request.form.get("db_type")
        active_db_name = None
        error_message = None

        try:
            if db_type == "yugidb":
                connection_string = request.form.get("connection_string")
                currentdb = YugiDB(connection_string)
                active_db_name = connection_string.split("/")[-1]
            else:
                currentdb = omegadb
                active_db_name = "omega.db"
        except Exception as e:
            error_message = str(e)

        kwargs = {"active_db_name": active_db_name}
        if error_message:
            kwargs["error_message"] = error_message

        return redirect(url_for("index", **kwargs))


api.add_resource(CardResource, "/card_data")
api.add_resource(ArchResource, "/arch_data")
api.add_resource(SetResource, "/set_data")
api.add_resource(ConnectionResource, "/set_connection")


@app.route("/static/renders/<path:filename>")
def static_renders(filename):
    return send_from_directory("static/renders", filename)


@app.route("/render/<int:card_id>")
def render_card(card_id):
    card = currentdb.get_cards_by_values({"id": card_id})[0]
    card.render("static/renders")
    filename = f"{card.id}.png"
    return render_template("card.html", filename=filename)


@app.route("/")
def index():
    card_dropdown_options = currentdb.get_card_name_id_map().items()
    archetype_dropdown_options = currentdb.get_archetype_name_id_map().items()
    set_dropdown_options = currentdb.get_set_name_id_map().items()
    active_db_name = request.args.get("active_db_name", None) or "omega.db"
    error_message = request.args.get("error_message")

    return render_template(
        "index.html",
        card_dropdown_options=card_dropdown_options,
        archetype_dropdown_options=archetype_dropdown_options,
        set_dropdown_options=set_dropdown_options,
        active_db_name=active_db_name,
        error_message=error_message,
    )


if __name__ == "__main__":
    if args.debug:
        app.run(debug=args.debug, port=args.port)
    else:
        from waitress import serve

        serve(app, host="0.0.0.0", port=args.port)
