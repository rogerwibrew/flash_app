# app.py
from flask import Flask, request, jsonify
from src.flash.flash import flash_calculation  # ✅ use your real function

app = Flask(__name__)


@app.route("/flash", methods=["POST"])
def flash_endpoint():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    # Required fields
    required_fields = ["z", "T", "P", "components"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    z = data.get("z")
    T = data.get("T")
    P = data.get("P")
    components = data.get("components")

    # --- Validation ---
    if not isinstance(z, list) or not all(isinstance(v, (int, float)) for v in z):
        return jsonify({"error": "z must be a list of numbers"}), 400

    if not isinstance(T, (int, float)):
        return jsonify({"error": "T must be a number"}), 400

    if not isinstance(P, (int, float)):
        return jsonify({"error": "P must be a number"}), 400

    if not isinstance(components, list) or not all(
        isinstance(c, dict) for c in components
    ):
        return jsonify({"error": "components must be a list of dicts"}), 400

    if len(z) != len(components):
        return jsonify({"error": "z length must equal number of components"}), 400

    try:
        # --- Call the actual solver ---
        result = flash_calculation(z, T, P, components)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500
