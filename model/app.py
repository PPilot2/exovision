import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import model

app = Flask(__name__)
CORS(app)

# Preload Kepler dataset for training
td_df = pd.read_csv("TD_2024.12.26_14.02.59.csv", comment="#")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        # Load TESS input CSV
        toi_df = pd.read_csv(file, comment="#")

        # Rename columns for consistency
        column_mapping = {
            "toi": "pl_name",
            "pl_trandurh": "pl_trandur",
            "st_tmag": "sy_vmag",
            "st_tmagerr1": "sy_vmagerr1",
            "st_tmagerr2": "sy_vmagerr2",
        }
        toi_df = toi_df.rename(columns=column_mapping)

        # Align columns between datasets
        common_cols = list(set(toi_df.columns).intersection(set(td_df.columns)))
        toi_filtered = toi_df[common_cols].dropna()
        td_filtered = td_df[common_cols].dropna()

        # Run model once — get predictions + accuracy
        predictions, val_accuracy = model(toi_filtered, td_filtered)

        # Sort and select top 20
        top_planets = predictions.sort_values("rf_probability", ascending=False).head(20)

        # Return results
        return jsonify({
            "accuracy": round(val_accuracy, 4),
            "planets": top_planets[["pl_name", "rf_probability"]].to_dict(orient="records"),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
