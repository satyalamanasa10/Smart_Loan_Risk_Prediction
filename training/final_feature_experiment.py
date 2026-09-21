# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# STEP 2B: FINAL HYBRID FEATURE EXPERIMENT
# ============================================================

import pandas as pd
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
# PROJECT HEADER
# ============================================================

print("\n" + "=" * 75)
print("SMART LOAN RISK PREDICTION SYSTEM")
print("FINAL HYBRID FEATURE EXPERIMENT")
print("=" * 75)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully!")
print("Dataset Shape:", df.shape)


# ============================================================
# TARGET
# ============================================================

TARGET = "LoanApproved"

y = df[TARGET].copy()


# ============================================================
# FINAL USER INPUT FEATURES
# ============================================================

final_user_features = [

    # Personal Information
    "Age",
    "EmploymentStatus",
    "EducationLevel",
    "Experience",
    "HomeOwnershipStatus",

    # Financial Information
    "AnnualIncome",
    "CreditScore",
    "MonthlyDebtPayments",
    "SavingsAccountBalance",

    # Loan Information
    "LoanAmount",
    "LoanDuration",
    "LoanPurpose"
]


# Check feature availability

missing_features = [

    feature
    for feature in final_user_features
    if feature not in df.columns

]

if missing_features:

    print("\nWARNING!")
    print("Missing Features:")
    print(missing_features)

else:

    print("\nAll selected features found successfully!")


print("\n" + "-" * 75)
print("FINAL USER INPUT FEATURES")
print("-" * 75)

for index, feature in enumerate(
    final_user_features,
    start=1
):

    print(f"{index}. {feature}")


# ============================================================
# CREATE FEATURE DATASET
# ============================================================

X = df[
    final_user_features
].copy()


# ============================================================
# FEATURE ENGINEERING
# ============================================================

print("\n" + "-" * 75)
print("FEATURE ENGINEERING")
print("-" * 75)


# ------------------------------------------------------------
# 1. MONTHLY INCOME
# ------------------------------------------------------------

X["MonthlyIncome_Calculated"] = (

    X["AnnualIncome"] / 12

)


# ------------------------------------------------------------
# 2. DEBT TO INCOME RATIO
# ------------------------------------------------------------

X["DebtToIncome_Calculated"] = (

    X["MonthlyDebtPayments"]
    /
    (X["MonthlyIncome_Calculated"] + 1)

)


# ------------------------------------------------------------
# 3. LOAN TO INCOME RATIO
# ------------------------------------------------------------

X["LoanToIncomeRatio"] = (

    X["LoanAmount"]
    /
    (X["AnnualIncome"] + 1)

)


# ------------------------------------------------------------
# 4. SAVINGS TO LOAN RATIO
# ------------------------------------------------------------

X["SavingsToLoanRatio"] = (

    X["SavingsAccountBalance"]
    /
    (X["LoanAmount"] + 1)

)


# ------------------------------------------------------------
# 5. EXPERIENCE TO AGE RATIO
# ------------------------------------------------------------

X["ExperienceToAgeRatio"] = (

    X["Experience"]
    /
    (X["Age"] + 1)

)


engineered_features = [

    "MonthlyIncome_Calculated",
    "DebtToIncome_Calculated",
    "LoanToIncomeRatio",
    "SavingsToLoanRatio",
    "ExperienceToAgeRatio"

]


print("\nEngineered Features Created:")

for feature in engineered_features:

    print("-", feature)


# ============================================================
# FINAL FEATURE INFORMATION
# ============================================================

print("\n" + "-" * 75)
print("FINAL DATASET INFORMATION")
print("-" * 75)

print(
    "Original User Features:",
    len(final_user_features)
)

print(
    "Engineered Features:",
    len(engineered_features)
)

print(
    "Total Features:",
    X.shape[1]
)

print("\nFeature Names:")

for index, feature in enumerate(
    X.columns,
    start=1
):

    print(f"{index}. {feature}")


# ============================================================
# IDENTIFY FEATURE TYPES
# ============================================================

numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()


categorical_features = X.select_dtypes(
    include=["object", "category"]
).columns.tolist()


print("\nNumerical Features:")

print(numerical_features)


print("\nCategorical Features:")

print(categorical_features)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("\n" + "=" * 75)
print("TRAIN / TEST SPLIT")
print("=" * 75)


X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)


print("Training Samples:", X_train.shape[0])

print("Testing Samples:", X_test.shape[0])


# ============================================================
# PREPROCESSING PIPELINE
# ============================================================

numerical_transformer = Pipeline(

    steps=[

        (
            "imputer",
            SimpleImputer(strategy="median")
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
# MODELS
# ============================================================

models = {

    "Logistic Regression":

        LogisticRegression(

            max_iter=3000,

            class_weight="balanced",

            random_state=42

        ),


    "Random Forest":

        RandomForestClassifier(

            n_estimators=300,

            max_depth=18,

            min_samples_split=5,

            min_samples_leaf=2,

            class_weight="balanced",

            random_state=42,

            n_jobs=-1

        )

}


# ============================================================
# TRAIN AND EVALUATE MODELS
# ============================================================

print("\n" + "=" * 75)
print("MODEL TRAINING AND EVALUATION")
print("=" * 75)


results = []


for model_name, model in models.items():

    print("\n" + "-" * 75)

    print(
        f"Training {model_name}"
    )

    print("-" * 75)


    # Create pipeline

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


    # Predictions

    predictions = pipeline.predict(

        X_test

    )


    probabilities = pipeline.predict_proba(

        X_test

    )[:, 1]


    # Metrics

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


    # Store results

    results.append({

        "Model": model_name,

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


    # Display metrics

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


# ============================================================
# FINAL RESULTS
# ============================================================

results_df = pd.DataFrame(

    results

)


print("\n" + "=" * 75)

print(
    "FINAL HYBRID FEATURE EXPERIMENT RESULTS"
)

print("=" * 75)


print(

    results_df.to_string(
        index=False
    )

)


# ============================================================
# SAVE RESULTS
# ============================================================

results_file = (

    OUTPUT_PATH

    / "final_feature_experiment_results.csv"

)


results_df.to_csv(

    results_file,

    index=False

)


print("\nResults saved successfully!")

print(
    "Location:",
    results_file
)


# ============================================================
# BEST MODEL
# ============================================================

best_model = results_df.loc[

    results_df["F1 Score"].idxmax()

]


print("\n" + "=" * 75)

print("BEST MODEL BASED ON F1 SCORE")

print("=" * 75)


print(

    "Model:",

    best_model["Model"]

)


print(

    "F1 Score:",

    best_model["F1 Score"],

    "%"

)


print(

    "ROC-AUC:",

    best_model["ROC-AUC"],

    "%"

)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 75)

print(
    "FINAL FEATURE EXPERIMENT COMPLETED SUCCESSFULLY"
)

print("=" * 75)


print("""

Next Step:

We will analyze these results and permanently decide:

1. Final frontend inputs
2. Final engineered features
3. Best preprocessing strategy
4. Best model architecture

After that, we will begin building the
FINAL LOAN APPROVAL MODEL.

""")