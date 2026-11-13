"""
app.py

Flask Web Application — Fake Review Detection System
=====================================================
Routes:
  GET  /          → Serve the main page (index.html)
  POST /predict   → Accept JSON review, return prediction JSON

Usage:
  python app.py

Then open:
  http://127.0.0.1:5000
"""

import os
import sys
from flask import Flask, request, jsonify, render_template

# Add project root to path so predict.py can import preprocessing
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from predict import predict_review

# ─────────────────────────────────────────────────────────────
# Flask application setup
# ─────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# Maximum allowed review length (characters)
MAX_REVIEW_LENGTH = 2000


# ═════════════════════════════════════════════════════════════
# ROUTE: GET /
# ═════════════════════════════════════════════════════════════
@app.route("/", methods=["GET"])
def index():
    """Serve the main review-input page."""
    return render_template("index.html")


# ═════════════════════════════════════════════════════════════
# ROUTE: POST /predict
# ═════════════════════════════════════════════════════════════
@app.route("/predict", methods=["POST"])
def predict():
    """
    Accept a JSON body with a 'review' field and return a prediction.

    Request body:
    {
        "review": "This product is absolutely amazing!"
    }

    Response (success, HTTP 200):
    {
        "prediction":          "Fake Review",
        "confidence":          87.5,
        "fake_probability":    0.875,
        "genuine_probability": 0.125,
        "reasons": [
            "Promotional language detected (e.g., 'buy now')"
        ]
    }

    Response (error, HTTP 400 / 503):
    {
        "error": "Review cannot be empty."
    }
    """

    # ── Parse request ─────────────────────────────────────────
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    review_text = data.get("review", "")

    # ── Validate length ───────────────────────────────────────
    if len(str(review_text)) > MAX_REVIEW_LENGTH:
        return jsonify({
            "error": (
                f"Review is too long ({len(review_text)} characters). "
                f"Maximum allowed is {MAX_REVIEW_LENGTH} characters."
            )
        }), 400

    # ── Run prediction ────────────────────────────────────────
    try:
        result = predict_review(review_text)
    except ValueError as e:
        # Input validation errors (empty, too short, etc.)
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        # Model/tokenizer loading errors
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        # Unexpected errors — log internally but don't expose stack trace
        app.logger.error(f"Prediction error: {e}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred during prediction."}), 500

    # ── Build response ────────────────────────────────────────
    return jsonify({
        "prediction":          result["prediction"],
        "confidence":          result["confidence"],
        "fake_probability":    result["fake_probability"],
        "genuine_probability": result["genuine_probability"],
        "reasons":             result["reasons"],
    }), 200


# ═════════════════════════════════════════════════════════════
# ENTRY POINT
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  Fake Review Detection — Flask Server")
    print("=" * 60)
    print("  Open: http://127.0.0.1:5000")
    print("  Press CTRL+C to stop.")
    print()

    # debug=False in production; set True only during development
    app.run(host="127.0.0.1", port=5000, debug=False)
