import traceback

import flask
import pandas as pd


app = flask.Flask(__name__)


@app.route("/v0/get_metadata", methods=["GET"])
def get_metadata():
    return flask.jsonify(meta)


@app.route("/v0/predict", methods=["POST"])
def predict():
    try:
        validate_predict_input(flask.request.json)
        # get preds
        return flask.jsonify(
            {
                "preds": preds,
                "prediction_generated_at": utils.get_current_timestamp_as_pretty_string(),
                "original_request": flask.request.json,
                "error": None,
            }
        )
    except Exception:
        traceback.print_exc()
        return flask.jsonify(
            {
                "preds": None,
                "prediction_generated_at": utils.get_current_timestamp_as_pretty_string(),
                "original_request": flask.request.json,
                "error": traceback.format_exc(),
            }
        )


def validate_predict_input(input_request):
    pass


def setup_model():
    global model
    global meta
    pass


def run_app():
    setup_model()
    app.run(host=host, port=port)


if __name__ == "__main__":
    run_app()
