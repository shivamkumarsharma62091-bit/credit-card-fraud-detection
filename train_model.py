
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

print("Loading Dataset...")

# Step 1: Load Dataset
df = pd.read_csv("dataset/creditcard.csv")

print("Dataset Loaded Successfully!")
print("Dataset Shape:", df.shape)

# Step 2: Separate Features and Target
X = df.drop("Class", axis=1)
y = df["Class"]

# Step 3: Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training Data:", X_train.shape)
print("Testing Data:", X_test.shape)

# Step 4: Create Machine Learning Pipeline
model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=42
    ))
])

# Step 5: Train Model
print("\nTraining Machine Learning Model...")

model.fit(X_train, y_train)

print("Model Trained Successfully!")

# Step 6: Make Predictions
y_pred = model.predict(X_test)

# Step 7: Evaluate Model
print("\n----- MODEL PERFORMANCE -----")

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, zero_division=0))
print("Recall:", recall_score(y_test, y_pred, zero_division=0))
print("F1 Score:", f1_score(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# Step 8: Save Trained Model
joblib.dump(model, "fraud_model.pkl")

print("\nModel Saved Successfully!")
print("File Name: fraud_model.pkl")
