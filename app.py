from flask import Flask, render_template, request, jsonify

import pandas as pd
import joblib
import json

app = Flask(__name__)

# Load trained ML model

saved = joblib.load(
    "models/quality_model.joblib"
)

model = saved["model"]

features = saved["features"]


# Home page

@app.route("/")
def home():

    return render_template("index.html")


# Prediction API

@app.route("/api/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        values = {}

        for feature in features:

            values[feature] = float(data[feature])

        # Validate sensor input ranges

        limits = {
            "temperature_c": (0, 150),
            "vibration_mm_s": (0, 20),
            "spindle_speed_rpm": (0, 3000),
            "pressure_bar": (0, 15),
            "operating_hours": (0, 24),
            "power_consumption_kw": (0, 30)
        }

        for feature, (low, high) in limits.items():

            if not low <= values[feature] <= high:

                return jsonify({
                    "error": f"{feature} must be between {low} and {high}"
                }), 400

        # Convert input into DataFrame

        input_data = pd.DataFrame(
            [values],
            columns=features
        )

        # Predict defect

        prediction = model.predict(input_data)[0]

        probabilities = model.predict_proba(input_data)[0]

        confidence = max(probabilities) * 100

        probability_map = {
            str(label): round(float(prob), 4)
            for label, prob in zip(
                model.classes_,
                probabilities
            )
        }

        return jsonify({

            "prediction": str(prediction),

            "confidence": round(
                float(confidence), 2
            ),

            "status": (
                "Normal"
                if prediction == "Normal"
                else "Defect detected"
            ),

            "probabilities": probability_map

        })

    except (ValueError, TypeError, KeyError) as error:

        return jsonify({
            "error": str(error)
        }), 400

# Model evaluation API

@app.route("/api/metrics")
def metrics():

    with open("models/metrics.json") as file:

        result = json.load(file)

    return jsonify(result)


if __name__ == "__main__":

    app.run(debug=True, port=5000)