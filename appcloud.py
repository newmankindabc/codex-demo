import os
from flask import Flask, request, jsonify, abort
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


def _parse_numbers(payload):
    """Validate and extract a/b as floats."""
    if payload is None:
        abort(400, description="Request body must be JSON")
    try:
        a = payload["a"]
        b = payload["b"]
    except KeyError as exc:
        abort(400, description=f"Missing field: {exc.args[0]}")
    try:
        return float(a), float(b)
    except (TypeError, ValueError):
        abort(400, description="fields a and b must be numberst")


def _compute(op):
    data = request.get_json(silent=True)
    a, b = _parse_numbers(data)
    result = op(a, b)
    return jsonify({"result": result}), 200


@app.route("/sum", methods=["POST"])
def sum_api():
    """Add two numbers."""
    return _compute(lambda x, y: x + y)


@app.route("/multiply", methods=["POST"])
def multiply_api():
    """Multiply two numbers."""
    return _compute(lambda x, y: x * y)


@app.errorhandler(HTTPException)
def handle_http_error(exc: HTTPException):
    response = {
        "error": exc.description or exc.name,
    }
    return jsonify(response), exc.code


@app.errorhandler(Exception)
def handle_unexpected_error(exc: Exception):
    response = {"error": "Internal Server Error"}
    return jsonify(response), 500


if __name__ == "__main__":
    debug_flag = os.getenv("APP_DEBUG", "").lower() == "true"
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "5000"))
    app.run(host=host, port=port, debug=debug_flag)
