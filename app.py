
import os
import joblib
import pandas as pd

from flask import Flask, render_template, request

app = Flask(__name__)

# Load trained machine learning model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "fraud_model.pkl"
)

model = joblib.load(MODEL_PATH)

# Get model feature names
FEATURES = list(model.feature_names_in_)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return render_template(
            "index.html",
            error="Please upload a CSV file."
        )

    file = request.files["file"]

    if file.filename == "":
        return render_template(
            "index.html",
            error="Please select a CSV file."
        )

    if not file.filename.lower().endswith(".csv"):
        return render_template(
            "index.html",
            error="Only CSV files are allowed."
        )

    try:
        # Read uploaded CSV
        df = pd.read_csv(file)

        # Remove actual Class column if present
        if "Class" in df.columns:
            df = df.drop(columns=["Class"])

        # Check required columns
        missing_columns = [
            col for col in FEATURES if col not in df.columns
        ]

        if missing_columns:
            return render_template(
                "index.html",
                error="CSV is missing required columns: "
                + ", ".join(missing_columns)
            )

        # Select features in training order
        X = df[FEATURES].apply(pd.to_numeric, errors="coerce")

        if X.isnull().any().any():
            return render_template(
                "index.html",
                error="CSV contains missing or invalid values."
            )

        # Predict transactions
        predictions = model.predict(X)

        # Create results table
        results = pd.DataFrame({
            "Amount": X["Amount"].values,
            "Prediction": [
                "FRAUD" if p == 1 else "GENUINE"
                for p in predictions
            ]
        })

        # Calculate totals
        total = len(results)
        fraud = int((predictions == 1).sum())
        genuine = total - fraud

        # Show first 100 transactions
        table = results.head(100).to_dict(orient="records")

        return render_template(
            "index.html",
            total=total,
            genuine=genuine,
            fraud=fraud,
            table=table
        )

    except Exception as e:
        return render_template(
            "index.html",
            error=f"Error processing file: {str(e)}"
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
