
import pandas as pd
import joblib
import json

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# 1. Load dataset

df = pd.read_csv(
    "data/manufacturing_quality.csv"
)

# 2. Separate features and target

X = df.drop("defect_type", axis=1)

y = df["defect_type"]

# 3. Split dataset

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# 4. Create Random Forest model

rf = RandomForestClassifier(
    random_state=42,
    class_weight="balanced"
)

# 5. Apply GridSearchCV

param_grid = {
    "n_estimators": [50, 100, 150],
    "max_depth": [5, 10, None],
    "min_samples_split": [2, 4],
    "min_samples_leaf": [1, 2]
}

grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5,
    scoring="f1_macro",
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

# Select best model

model = grid_search.best_estimator_

print("\nBest Parameters:")
print(grid_search.best_params_)

print("\nBest Cross Validation F1 Score:")
print(round(grid_search.best_score_ * 100, 2), "%")

# 6. Make predictions

y_pred = model.predict(X_test)

# 7. Calculate evaluation metrics

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    average="macro",
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average="macro",
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    average="macro",
    zero_division=0
)

# 8. Display results

print("\nMODEL PERFORMANCE")

print("Accuracy:", round(accuracy * 100, 2), "%")

print("Precision:", round(precision * 100, 2), "%")

print("Recall:", round(recall * 100, 2), "%")

print("F1 Score:", round(f1 * 100, 2), "%")

print("\nClassification Report:")

print(classification_report(y_test, y_pred))

# 9. Confusion matrix

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=model.classes_
)

# 10. Save model

joblib.dump(
    {
        "model": model,
        "features": X.columns.tolist()
    },
    "models/quality_model.joblib"
)

# 11. Save metrics

metrics = {
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1_score": f1,
    "labels": model.classes_.tolist(),
    "confusion_matrix": cm.tolist()
}

with open("models/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("\nModel saved successfully!")
