# app.py
from flask import Flask, request, jsonify, g
from src.flash.flash import flash_calculation  # ✅ use your real function
from db.database import init_db, SessionLocal
from db.models import Component

app = Flask(__name__)


@app.before_request
def setup_database():
    """
    Initilise datbase and seed with default components if empty.
    """
    init_db()
    db = SessionLocal()
    if db.query(Component).count() == 0:
        # Add ethanol and water as defaults
        db.add_all(
            [
                Component(name="ethanol", A=8.20417, B=1642.89, C=230.300),
                Component(name="water", A=8.07131, B=1730.63, C=233.426),
            ]
        )
        db.commit()
    db.close()
    g._db_initialized = True


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
    component_names = data.get("components")

    # --- Validation ---
    if not isinstance(z, list) or not all(isinstance(v, (int, float)) for v in z):
        return jsonify({"error": "z must be a list of numbers"}), 400

    if not isinstance(T, (int, float)):
        return jsonify({"error": "T must be a number"}), 400

    if not isinstance(P, (int, float)):
        return jsonify({"error": "P must be a number"}), 400

    if not isinstance(component_names, list) or not all(
        isinstance(c, str) for c in component_names
    ):
        return jsonify({"error": "components must be a list of names (strings)"}), 400

    if len(z) != len(component_names):
        return jsonify({"error": "z length must equal number of components"}), 400

    try:
        # --- Fetch Antoine constants from DB ---
        db = SessionLocal()
        db_components = (
            db.query(Component).filter(Component.name.in_(component_names)).all()
        )
        db.close()

        # Ensure all requested components exist
        if len(db_components) != len(component_names):
            return (
                jsonify({"error": "One or more components not found in database"}),
                404,
            )

        # Convert DB results into list of dicts {A, B, C}
        constants = [{"A": c.A, "B": c.B, "C": c.C} for c in db_components]

        # --- Call the actual solver (unchanged) ---
        result = flash_calculation(z, T, P, constants)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500
