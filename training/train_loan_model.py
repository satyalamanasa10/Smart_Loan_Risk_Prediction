# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# FINAL LOAN APPROVAL MODEL TRAINING
# ============================================================

import sys
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


# ============================================================
# PROJECT PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "Loan.csv"

MODELS_PATH = BASE_DIR / "models"

OUTPUT_PATH = BASE_DIR / "training" / "outputs"

MODELS_PATH.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# IMPORT CUSTOM MODULES
# ============================================================

sys.path.append(
    str(BASE_DIR)
)

from src.feature_engineering import (
    USER_INPUT_FEATURES,
    create_engineered_features,
    validate_input_features
)

from src.preprocessing import (
    create_preprocessor,
    get_feature_types
)


# ============================================================
# PROJECT HEADER
# ============================================================

print("\n" + "=" * 75)

print(
    "SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM"
)

print(
    "FINAL LOAN APPROVAL MODEL TRAINING"
)

print("=" * 75)


# ============================================================
# LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(
    DATA_PATH
)

print(
    "Dataset loaded successfully!"
)

print(
    "Dataset Shape:",
    df.shape
)


# ============================================================
# DEFINE TARGET
# ============================================================

TARGET = "LoanApproved"


if TARGET not in df.columns:

    raise ValueError(
        f"Target column '{TARGET}' not found!"
    )


# ============================================================
# VALIDATE INPUT FEATURES
# ============================================================

validate_input_features(
    df
)

print(
    "\nAll required user input features found!"
)


# ============================================================
# SELECT USER INPUT FEATURES
# ============================================================

X = df[
    USER_INPUT_FEATURES
].copy()

y = df[
    TARGET
].copy()


print(
    "\nOriginal User Features:",
    len(USER_INPUT_FEATURES)
)

print(
    "Training Samples:",
    X.shape[0]
)


# ============================================================
# FEATURE ENGINEERING
# ============================================================

print(
    "\nApplying feature engineering..."
)

X = create_engineered_features(
    X
)


print(
    "Feature engineering completed!"
)

print(
    "Total Features After Engineering:",
    X.shape[1]
)


# ============================================================
# FEATURE TYPE INFORMATION
# ============================================================

numerical_features, categorical_features = get_feature_types(
    X
)


print(
    "\nNumerical Features:"
)

for feature in numerical_features:

    print(
        "-",
        feature
    )


print(
    "\nCategorical Features:"
)

for feature in categorical_features:

    print(
        "-",
        feature
    )


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print(
    "\n" + "=" * 75
)

print(
    "TRAIN / TEST SPLIT"
)

print(
    "=" * 75
)


X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print(
    "Training Samples:",
    X_train.shape[0]
)

print(
    "Testing Samples:",
    X_test.shape[0]
)


# ============================================================
# CREATE PREPROCESSOR
# ============================================================

print(
    "\nCreating preprocessing pipeline..."
)

preprocessor = create_preprocessor(
    X_train
)


# ============================================================
# CREATE RANDOM FOREST MODEL
# ============================================================

print(
    "Creating Random Forest model..."
)

model = RandomForestClassifier(

    n_estimators=300,

    max_depth=18,

    min_samples_split=5,

    min_samples_leaf=2,

    class_weight="balanced",

    random_state=42,

    n_jobs=-1
)


# ============================================================
# CREATE COMPLETE ML PIPELINE
# ============================================================

pipeline = Pipeline(

    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            model
        )

    ]

)


# ============================================================
# TRAIN MODEL
# ============================================================

print(
    "\n" + "=" * 75
)

print(
    "TRAINING FINAL RANDOM FOREST MODEL"
)

print(
    "=" * 75
)


pipeline.fit(
    X_train,
    y_train
)


print(
    "\nModel training completed successfully!"
)


# ============================================================
# MAKE PREDICTIONS
# ============================================================

print(
    "\nMaking predictions..."
)

predictions = pipeline.predict(
    X_test
)

probabilities = pipeline.predict_proba(
    X_test
)[:, 1]


# ============================================================
# MODEL EVALUATION
# ============================================================

print(
    "\n" + "=" * 75
)

print(
    "MODEL PERFORMANCE"
)

print(
    "=" * 75
)


accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    probabilities
)


print(
    f"\nAccuracy  : {accuracy * 100:.2f}%"
)

print(
    f"Precision : {precision * 100:.2f}%"
)

print(
    f"Recall    : {recall * 100:.2f}%"
)

print(
    f"F1 Score  : {f1 * 100:.2f}%"
)

print(
    f"ROC-AUC   : {roc_auc * 100:.2f}%"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print(
    "\n" + "=" * 75
)

print(
    "CLASSIFICATION REPORT"
)

print(
    "=" * 75
)

print(

    classification_report(
        y_test,
        predictions
    )

)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print(
    "\nGenerating confusion matrix..."
)

cm = confusion_matrix(
    y_test,
    predictions
)


display = ConfusionMatrixDisplay(

    confusion_matrix=cm,

    display_labels=[
        "Rejected",
        "Approved"
    ]

)


fig, ax = plt.subplots(
    figsize=(7, 5)
)

display.plot(
    ax=ax
)

plt.title(
    "Loan Approval Model - Confusion Matrix"
)

plt.tight_layout()


confusion_matrix_path = (

    OUTPUT_PATH

    / "loan_confusion_matrix.png"

)


plt.savefig(
    confusion_matrix_path,
    dpi=300
)

plt.close()


print(
    "Confusion matrix saved!"
)

print(
    "Location:",
    confusion_matrix_path
)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

print(
    "\nCalculating feature importance..."
)


# Get feature names after preprocessing

feature_names = pipeline.named_steps[
    "preprocessor"
].get_feature_names_out()


# Get importance scores

importances = pipeline.named_steps[
    "model"
].feature_importances_


# Create DataFrame

importance_df = pd.DataFrame({

    "Feature": feature_names,

    "Importance": importances

})


# Sort

importance_df = importance_df.sort_values(

    by="Importance",

    ascending=False

)


print(
    "\nTOP 15 IMPORTANT FEATURES"
)

print(
    importance_df.head(15).to_string(
        index=False
    )
)


# Save feature importance

importance_csv_path = (

    OUTPUT_PATH

    / "loan_feature_importance.csv"

)


importance_df.to_csv(

    importance_csv_path,

    index=False

)


# Plot Top 15

top_features = importance_df.head(15)


plt.figure(
    figsize=(10, 7)
)

plt.barh(

    top_features["Feature"],

    top_features["Importance"]

)

plt.xlabel(
    "Importance Score"
)

plt.ylabel(
    "Features"
)

plt.title(
    "Top 15 Feature Importances - Loan Approval Model"
)

plt.gca().invert_yaxis()

plt.tight_layout()


feature_importance_plot_path = (

    OUTPUT_PATH

    / "loan_feature_importance.png"

)


plt.savefig(
    feature_importance_plot_path,
    dpi=300
)

plt.close()


print(
    "\nFeature importance files saved!"
)


# ============================================================
# SAVE MODEL PIPELINE
# ============================================================

print(
    "\n" + "=" * 75
)

print(
    "SAVING FINAL MODEL"
)

print(
    "=" * 75
)


model_path = (

    MODELS_PATH

    / "loan_approval_model.pkl"

)


joblib.dump(

    pipeline,

    model_path
)


print(
    "\nFinal model saved successfully!"
)

print(
    "Model Location:",
    model_path
)


# ============================================================
# SAVE MODEL METRICS
# ============================================================

metrics = pd.DataFrame({

    "Metric": [

        "Accuracy",

        "Precision",

        "Recall",

        "F1 Score",

        "ROC-AUC"

    ],

    "Score": [

        accuracy,

        precision,

        recall,

        f1,

        roc_auc

    ]

})


metrics_path = (

    OUTPUT_PATH

    / "loan_model_metrics.csv"

)


metrics.to_csv(

    metrics_path,

    index=False
)


print(
    "\nMetrics saved!"
)


# ============================================================
# COMPLETION
# ============================================================

print(
    "\n" + "=" * 75
)

print(
    "LOAN APPROVAL MODEL TRAINING COMPLETED SUCCESSFULLY"
)

print(
    "=" * 75
)


print("""

Generated Files:

models/
    loan_approval_model.pkl

training/outputs/
    loan_model_metrics.csv
    loan_confusion_matrix.png
    loan_feature_importance.csv
    loan_feature_importance.png

NEXT STEP:
We will verify the saved model and then begin
STEP 4 — RISK SCORE MODEL DEVELOPMENT.

""")