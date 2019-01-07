import os

import numpy
from flask import Flask, jsonify
from flask.json import JSONEncoder

from salicml.middleware.middleware import Middleware
from salicml.utils.utils import is_valid_pronac


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.bool_):
            return "True" if obj else "False"

        return super(CustomJSONEncoder, self).default(obj)


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.json_encoder = CustomJSONEncoder

is_production = os.environ.get("SALICML_PRODUCTION", False)
if is_production:
    app.middleware = Middleware()
    app.middleware.load_all()


@app.route("/metric/number_of_items/<string:pronac>", methods=["GET"])
def get_metric_number_of_items(pronac):
    if is_valid_pronac(pronac):
        middleware = app.middleware
        result = middleware.get_metric_number_of_items(pronac)
        return jsonify(result), 200
    else:
        INVALID_PRONAC_MESSAGE = "Invalid PRONAC"
        return jsonify(INVALID_PRONAC_MESSAGE), 400


@app.route("/metric/verified_approved/<string:pronac>", methods=["GET"])
def get_metric_verified_vs_approved(pronac):
    if is_valid_pronac(pronac):
        middleware = app.middleware
        result = middleware.get_metric_verified_approved(pronac)
        return jsonify(result), 200
    else:
        INVALID_PRONAC_MESSAGE = "Invalid PRONAC"
        return jsonify(INVALID_PRONAC_MESSAGE), 400
