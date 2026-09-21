# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# STEP 2A: FEATURE SELECTION EXPERIMENT
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "Loan.csv"
OUTPUT_PATH = BASE_DIR / "training" / "outputs"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("\n" + "=" * 75)
print("SMART LOAN PROJECT - FEATURE SELECTION EXPERIMENT")
print("=" * 75)

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully!")
print("Dataset Shape:", df.shape)


# ============================================================
# REMOVE COLUMNS THAT SHOULD NOT BE USED
# ============================================================

# These columns are targets, identifiers, or potentially
# post-decision / leakage features.

leakage_columns = [
    "ApplicationDate",
    "RiskScore",
    "InterestRate",
    "BaseInterestRate",
    "MonthlyLoanPayment",
    "TotalDebtToIncomeRatio"
]

print("\nRemoving leakage / post-decision columns:")
print(leakage_columns)

df_model = df.drop(
    columns=leakage_columns,
    errors="ignore"
)


# ============================================================
# TARGET VARIABLE
# ============================================================

TARGET = "LoanApproved"

X = df_model.drop(columns=[TARGET])
y = df_model[TARGET]

print("\nTarget Variable:", TARGET)
print("Feature Count:", X.shape[1])


# ============================================================
# DEFINE FEATURE SET A
# FULL REALISTIC FEATURES
# ============================================================

full_features = [
    "Age",
    "AnnualIncome",
    "CreditScore",
    "EmploymentStatus",
    "EducationLevel",
    "Experience",
    "LoanAmount",
    "LoanDuration",
    "MaritalStatus",
    "NumberOfDependents",
    "HomeOwnershipStatus",
    "MonthlyDebtPayments",
    "CreditCardUtilizationRate",
    "NumberOfOpenCreditLines",
    "NumberOfCreditInquiries",
    "DebtToIncomeRatio",
    "BankruptcyHistory",
    "LoanPurpose",
    "PreviousLoanDefaults",
    "PaymentHistory",
    "LengthOfCreditHistory",
    "SavingsAccountBalance",
    "CheckingAccountBalance",
    "TotalAssets",
    "TotalLiabilities",
    "JobTenure",
    "NetWorth"
]

# Keep only columns that actually exist
full_features = [
    col for col in full_features
    if col in df.columns
]

print("\n" + "-" * 75)
print("FEATURE SET A - FULL REALISTIC MODEL")
print("-" * 75)

print("Number of Features:", len(full_features))
print(full_features)


# ============================================================
# DEFINE FEATURE SET B
# SIMPLIFIED USER-FRIENDLY FEATURES
# ============================================================

simple_features = [
    "Age",
    "AnnualIncome",
    "CreditScore",
    "EmploymentStatus",
    "Experience",
    "LoanAmount",
    "LoanDuration",
    "MonthlyDebtPayments",
    "SavingsAccountBalance",
    "LoanPurpose"
]

simple_features = [
    col for col in simple_features
    if col in df.columns
]

print("\n" + "-" * 75)
print("FEATURE SET B - SIMPLIFIED MODEL")
print("-" * 75)

print("Number of Features:", len(simple_features))
print(simple_features)


# ============================================================
# FEATURE ENGINEERING FOR SIMPLIFIED MODEL
# ============================================================

df_simple = df[simple_features].copy()

# Prevent division by zero
monthly_income = df_simple["AnnualIncome"] / 12

df_simple["MonthlyIncome_Calculated"] = monthly_income

df_simple["DebtToIncome_Calculated"] = (
    df_simple["MonthlyDebtPayments"]
    / (monthly_income + 1)
)

df_simple["LoanToIncomeRatio"] = (
    df_simple["LoanAmount"]
    / (df_simple["AnnualIncome"] + 1)
)

df_simple["SavingsToLoanRatio"] = (
    df_simple["SavingsAccountBalance"]
    / (df_simple["LoanAmount"] + 1)
)


print("\nEngineered Features Added:")
print([
    "MonthlyIncome_Calculated",
    "DebtToIncome_Calculated",
    "LoanToIncomeRatio",
    "SavingsToLoanRatio"
])


# ============================================================
# PREPROCESSING FUNCTION
# ============================================================

def create_preprocessor(X_data):

    numerical_features = X_data.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_features = X_data.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


    numerical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    )


    categorical_transformer = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent")
            ),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore")
            )
        ]
    )


    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                numerical_transformer,
                numerical_features
            ),
            (
                "cat",
                categorical_transformer,
                categorical_features
            )
        ]
    )

    return preprocessor


# ============================================================
# MODEL EVALUATION FUNCTION
# ============================================================

def evaluate_model(
    X_data,
    y_data,
    feature_set_name
):

    print("\n" + "=" * 75)
    print(f"EVALUATING: {feature_set_name}")
    print("=" * 75)


    # Train/Test Split

    X_train, X_test, y_train, y_test = train_test_split(
        X_data,
        y_data,
        test_size=0.20,
        random_state=42,
        stratify=y_data
    )


    # Create preprocessor

    preprocessor = create_preprocessor(X_train)


    # Models

    models = {
        "Logistic Regression":
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced"
            ),

        "Random Forest":
            RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                random_state=42,
                class_weight="balanced"
            )
    }


    results = []


    # ========================================================
    # TRAIN AND EVALUATE MODELS
    # ========================================================

    for model_name, model in models.items():

        print(f"\nTraining {model_name}...")


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


        pipeline.fit(
            X_train,
            y_train
        )


        predictions = pipeline.predict(
            X_test
        )


        probabilities = pipeline.predict_proba(
            X_test
        )[:, 1]


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


        results.append({
            "Feature Set":
                feature_set_name,

            "Model":
                model_name,

            "Accuracy":
                round(
                    accuracy * 100,
                    2
                ),

            "Precision":
                round(
                    precision * 100,
                    2
                ),

            "Recall":
                round(
                    recall * 100,
                    2
                ),

            "F1 Score":
                round(
                    f1 * 100,
                    2
                ),

            "ROC-AUC":
                round(
                    roc_auc * 100,
                    2
                )
        })


        print(
            f"Accuracy  : {accuracy * 100:.2f}%"
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


    return results


# ============================================================
# EXPERIMENT A
# FULL FEATURE MODEL
# ============================================================

X_full = df[full_features].copy()

results_full = evaluate_model(
    X_full,
    y,
    "Full Realistic Features"
)


# ============================================================
# EXPERIMENT B
# SIMPLIFIED + ENGINEERED FEATURES
# ============================================================

results_simple = evaluate_model(
    df_simple,
    y,
    "Simplified + Engineered Features"
)


# ============================================================
# COMBINE RESULTS
# ============================================================

all_results = (
    results_full
    + results_simple
)

results_df = pd.DataFrame(
    all_results
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 75)
print("FINAL FEATURE EXPERIMENT RESULTS")
print("=" * 75)

print(results_df.to_string(index=False))


# ============================================================
# SAVE RESULTS
# ============================================================

results_path = (
    OUTPUT_PATH
    / "feature_experiment_results.csv"
)

results_df.to_csv(
    results_path,
    index=False
)


print("\nResults saved successfully!")

print(
    "Location:",
    results_path
)


# ============================================================
# PROJECT RECOMMENDATION
# ============================================================

print("\n" + "=" * 75)
print("EXPERIMENT COMPLETED")
print("=" * 75)

print("""
Next Decision:

Compare the performance of:

1. Full Realistic Feature Model
2. Simplified + Engineered Feature Model

If simplified model performance is reasonably close,
we will use it for the final frontend because it provides
a better user experience.

Otherwise, we will select a balanced set of features
between accuracy and usability.
""")