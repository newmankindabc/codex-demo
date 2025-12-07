import os
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024  # cap request size to 1MB


class ValidationError(ValueError):
    """Raised when request payload fails validation."""


def make_json_response(code=0, message="", data=None, status=200):
    """Return a unified JSON response with explicit status."""
    return jsonify({"code": code, "message": message, "data": data}), status


def parse_operands():
    """Parse and validate operands a and b from JSON body."""
    if not request.is_json:
        raise ValidationError("Request must be JSON with application/json content type.")

    payload = request.get_json(silent=True)
    if payload is None:
        raise ValidationError("Invalid JSON payload.")

    try:
        a = payload["a"]
        b = payload["b"]
    except KeyError as exc:
        raise ValidationError(f"Missing required field: {exc.args[0]}")

    for name, value in (("a", a), ("b", b)):
        if not isinstance(value, (int, float)):
            raise ValidationError(f"Field '{name}' must be a number.")

    return a, b


@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return make_json_response(code=400, message=str(err), status=400)


@app.errorhandler(HTTPException)
def handle_http_exception(err):
    return make_json_response(code=err.code, message=err.description, status=err.code)


@app.errorhandler(Exception)
def handle_unexpected_error(err):
    # In production you might log err here.
    return make_json_response(code=500, message="Internal server error."), 500


def compute_operation(operation):
    a, b = parse_operands()
    return operation(a, b)


@app.route("/sum", methods=["POST"])
def sum_api():
    """Add two numbers."""
    result = compute_operation(lambda a, b: a + b)
    return make_json_response(data=result)


@app.route("/multiply", methods=["POST"])
def multiply_api():
    """Multiply two numbers."""
    result = compute_operation(lambda a, b: a * b)
    return make_json_response(data=result)


if __name__ == "__main__":
    debug = os.getenv("APP_DEBUG", "").lower() in {"1", "true", "yes", "on"}
    app.run("0.0.0.0", 5000, debug=debug)
