"""A tiny Flask web API that exposes the calculator.

Run locally with:  python -m app.main
Then visit:         http://localhost:5000/
"""
from flask import Flask, jsonify, request

from app.calculator import calculate

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(
        {
            "service": "calculator-api",
            "status": "ok",
            "usage": "/calc?op=add&a=2&b=3",
            "operations": ["add", "subtract", "multiply", "divide"],
        }
    )


@app.route("/health")
def health():
    # A health endpoint is handy for deployments to check the app is alive.
    return jsonify({"status": "healthy"}), 200


@app.route("/calc")
def calc():
    op = request.args.get("op", "")
    try:
        a = float(request.args.get("a", ""))
        b = float(request.args.get("b", ""))
    except ValueError:
        return jsonify({"error": "a and b must be numbers"}), 400

    try:
        result = calculate(op, a, b)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"operation": op, "a": a, "b": b, "result": result})


if __name__ == "__main__":
    # host=0.0.0.0 so it also works inside a Docker container.
    app.run(host="0.0.0.0", port=5000, debug=True)
