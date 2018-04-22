from flask import request, jsonify
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, InternalServerError, HTTPException

data = {
    "users": [],
    "polls": {
        "1": {
            "title": "Best fruit",
            "closed": False,
            "options": {
                 "0": "apples",
                 "1": "oranges",
                 "2": "pears"
            },
            "results": {
                 "0": 5,
                 "1": 12,
                 "2": 0
            },
            "voters": []
        },
        "2": {
            "title": "Best car brand",
            "closed": False,
            "options": {
                "0": "Toyota",
                "1": "Audi",
                "2": "Mercedes"
            },
            "results": {
                "0": 2,
                "1": 13,
                "2": 8
            },
            "voters": []
        }
    },
    "current_user": None
}


def api_error_handler(error):
    return jsonify(message=error.description), error.code


def setup_api(app):
    for error in (BadRequest.code, Forbidden.code, NotFound.code, InternalServerError.code):  # or with other http code you consider as error
        app.register_error_handler(error, api_error_handler)

    @app.errorhandler
    def http_error_handler(error):
        return jsonify(message=error.message), error.code

    @app.route("/api/voters", methods=['POST'])
    def predict():
        json = request.get_json()

        if "name" not in json:
            raise BadRequest("Parameter 'name' is missing in json")

        name = json["name"]
        users = data["users"]

        if name in users:
            raise Forbidden("User with this name already exists")

        new_id = len(users)
        users.append(name)

        data["current_user"] = new_id

        return "", 201, {"ETag": str(new_id)}

    @app.route("/api/polls/<string:poll_id>", methods=['GET'])
    def get_poll(poll_id):
        if poll_id not in data["polls"]:
            raise NotFound("Can’t find poll with given id")

        return jsonify(data["polls"][poll_id]["options"])

    @app.route("/api/polls/<string:poll_id>/results", methods=['GET'])
    def get_poll_results(poll_id):
        if poll_id not in data["polls"]:
            raise NotFound("Can’t find poll with given id")

        return jsonify(data["polls"][poll_id]["results"])

    @app.route("/api/polls/<string:poll_id>/vote", methods=['PATCH'])
    def vote(poll_id):
        json = request.get_json()

        if "option" not in json:
            raise BadRequest("Parameter 'option' is missing in json")

        user = data["current_user"]
        polls = data["polls"]

        if user is None:
            raise Forbidden("You should sign in first ([POST] /voters method)")

        if poll_id not in polls:
            raise NotFound("Can’t find poll with given id")

        if polls[poll_id]["closed"]:
            raise Forbidden("The poll is closed!")

        if user in polls[poll_id]["voters"]:
            raise Forbidden("You have already voted in this poll!")

        if json["option"] not in polls[poll_id]["results"]:
            raise Forbidden("Incorrect vote option '" + json["option"] + "'")

        polls[poll_id]["results"][json["option"]] += 1
        polls[poll_id]["voters"].append(user)

        return "", 204

    @app.route("/api/polls/<string:poll_id>/close", methods=['PATCH'])
    def close_poll(poll_id):
        if poll_id not in data["polls"]:
            raise NotFound("Can’t find poll with given id")

        if data["polls"][poll_id]["closed"]:
            raise Forbidden("Poll is already closed")

        data["polls"][poll_id]["closed"] = True

        return "", 204
