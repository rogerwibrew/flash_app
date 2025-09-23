from flask import Flask, request, jsonify
import numpy as np
from flash.flash import flash_calculation  # from src/flash.py

app = Flask(__name__)


@app.route("/flash", methods=["POST"])
def flash_endpoint():
    """
    Handle flash calculation requests.
    Expects JSON with z, T, P, and components.
    """
    data = request.get_json()

    z = np.array(data["z"], dtype=float)
    T = float(data["T"])
    P = float(data["P"])
    components = data["components"]

    result = flash_calculation(z, T, P, components)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
