# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# RISK SCORE MODEL EXPERIMENT
# ============================================================

import sys
import pandas as pd

from pathlib import Path

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder
)

from sklearn.impute import SimpleImputer

from sklearn.linear_model import LinearRegression

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# PROJECT PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "Loan.csv"

OUTPUT_PATH = BASE_DIR / "training" / "outputs"

OUTPUT_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# IMPORT CUSTOM FEATURE ENGINEERING
# ============================================================

sys.path.append(
    str(BASE_DIR)
)

from src.feature_engineering import (
    USER_INPUT_FEATURES,
    create_engineered_features,
    validate_input_features
)


# ============================================================
# PROJECT HEADER
# ============================================================

print("\n" + "=" * 75)

print(
    "SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM"
)

print(
    "RISK SCORE MODEL EXPERIMENT"
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
# TARGET
# ============================================================

TARGET = "RiskScore"

if TARGET not in df.columns:

    raise ValueError(
        f"Target column '{TARGET}' not found!"
    )


# ============================================================
# VALIDATE USER INPUT FEATURES
# ============================================================

validate_input_features(
    df
)


# ============================================================
# SELECT BASE FEATURES
# ============================================================

X = df[
    USER_INPUT_FEATURES
].copy()

y = df[
    TARGET
].copy()


print(
    "\nBase User Input Features:",
    len(USER_INPUT_FEATURES)
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
    "Total Features:",
    X.shape[1]
)


# ============================================================
# ADDITIONAL RISK-SPECIFIC FEATURES
# ============================================================

print(
    "\nAdding risk-specific features..."
)


# ------------------------------------------------------------
# CREDIT SCORE RISK
# Lower credit score = Higher risk
# ------------------------------------------------------------

X["CreditScoreRisk"] = (

    850 - X["CreditScore"]

)


# ------------------------------------------------------------
# DEBT BURDEN
# ------------------------------------------------------------

X["DebtBurden"] = (

    X["MonthlyDebtPayments"]

    *

    12

)


# ------------------------------------------------------------
# LOAN PAYMENT BURDEN
# ------------------------------------------------------------

X["LoanPaymentBurden"] = (

    X["LoanAmount"]

    /

    (X["AnnualIncome"] + 1)

)


# ------------------------------------------------------------
# FINANCIAL BUFFER
# ------------------------------------------------------------

X["FinancialBuffer"] = (

    X["SavingsAccountBalance"]

    /

    (
        X["MonthlyDebtPayments"]
        +
        1
    )

)


print(
    "Risk-specific features created!"
)


# ============================================================
# FEATURE TYPE DETECTION
# ============================================================

numerical_features = X.select_dtypes(

    include=["int64", "float64"]

).columns.tolist()


categorical_features = X.select_dtypes(

    include=["object", "category"]

).columns.tolist()


print(
    "\nTotal Numerical Features:",
    len(numerical_features)
)

print(
    "Total Categorical Features:",
    len(categorical_features)
)


# ============================================================
# PREPROCESSING PIPELINE
# ============================================================

numerical_transformer = Pipeline(

    steps=[

        (
            "imputer",
            SimpleImputer(
                strategy="median"
            )
        ),

        (
            "scaler",
            StandardScaler()
        )

    ]

)


categorical_transformer = Pipeline(

    steps=[

        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            )
        ),

        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )

    ]

)


preprocessor = ColumnTransformer(

    transformers=[

        (
            "numerical",
            numerical_transformer,
            numerical_features
        ),

        (
            "categorical",
            categorical_transformer,
            categorical_features
        )

    ]

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

    random_state=42
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
# DEFINE MODELS
# ============================================================

models = {

    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(

        n_estimators=300,

        max_depth=18,

        min_samples_split=5,

        min_samples_leaf=2,

        random_state=42,

        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(

        n_estimators=300,

        learning_rate=0.05,

        max_depth=4,

        random_state=42
    )

}


# ============================================================
# MODEL TRAINING & EVALUATION
# ============================================================

results = []


for model_name, model in models.items():

    print(
        "\n" + "-" * 75
    )

    print(
        f"Training {model_name}"
    )

    print(
        "-" * 75
    )


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


    # Train

    pipeline.fit(

        X_train,
        y_train
    )


    # Predict

    predictions = pipeline.predict(
        X_test
    )


    # Metrics

    mae = mean_absolute_error(
        y_test,
        predictions
    )


    mse = mean_squared_error(
        y_test,
        predictions
    )


    rmse = mse ** 0.5


    r2 = r2_score(
        y_test,
        predictions
    )


    print(
        f"MAE  : {mae:.4f}"
    )

    print(
        f"RMSE : {rmse:.4f}"
    )

    print(
        f"R² Score : {r2:.4f}"
    )


    results.append({

        "Model": model_name,

        "MAE": mae,

        "RMSE": rmse,

        "R2 Score": r2

    })


# ============================================================
# RESULTS DATAFRAME
# ============================================================

results_df = pd.DataFrame(
    results
)


# Sort by R²

results_df = results_df.sort_values(

    by="R2 Score",

    ascending=False

)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print(
    "\n" + "=" * 75
)

print(
    "FINAL RISK SCORE MODEL RESULTS"
)

print(
    "=" * 75
)


print(

    results_df.to_string(
        index=False
    )

)


# ============================================================
# SAVE RESULTS
# ============================================================

results_path = (

    OUTPUT_PATH

    / "risk_score_experiment_results.csv"

)


results_df.to_csv(

    results_path,

    index=False

)


print(
    "\nResults saved successfully!"
)

print(
    "Location:",
    results_path
)


# ============================================================
# BEST MODEL
# ============================================================

best_model = results_df.iloc[0]


print(
    "\n" + "=" * 75
)

print(
    "BEST MODEL"
)

print(
    "=" * 75
)


print(
    "Model:",
    best_model["Model"]
)

print(
    f"MAE: {best_model['MAE']:.4f}"
)

print(
    f"RMSE: {best_model['RMSE']:.4f}"
)

print(
    f"R² Score: {best_model['R2 Score']:.4f}"
)


print(
    "\n" + "=" * 75
)

print(
    "RISK SCORE EXPERIMENT COMPLETED SUCCESSFULLY"
)

print(
    "=" * 75
)


print("""

Next Step:

We will analyze the regression results and then:

1. Select the best Risk Score model
2. Create a final reusable Risk Score training pipeline
3. Save the model
4. Connect both models to the backend

""")