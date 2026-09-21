# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# STEP 1B: EXPLORATORY DATA ANALYSIS
# ============================================================

# -------------------------
# IMPORT LIBRARIES
# -------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# ============================================================
# PROJECT PATH CONFIGURATION
# ============================================================

# Current file location: eda/eda_analysis.py
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "Loan.csv"
OUTPUT_PATH = BASE_DIR / "eda" / "outputs"

# Create outputs folder if it doesn't exist
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


# ============================================================
# DISPLAY SETTINGS
# ============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 150)

sns.set_theme(style="whitegrid")


# ============================================================
# LOAD DATASET
# ============================================================

print("\n" + "=" * 70)
print("SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM")
print("EXPLORATORY DATA ANALYSIS")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully!")
print("Dataset Path:", DATA_PATH)

print("\nDataset Shape:", df.shape)
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ============================================================
# 1. BASIC DATASET OVERVIEW
# ============================================================

print("\n" + "=" * 70)
print("1. BASIC DATASET OVERVIEW")
print("=" * 70)

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumn Names:")
for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")

print("\nData Types:")
print(df.dtypes)


# ============================================================
# 2. MISSING VALUES
# ============================================================

print("\n" + "=" * 70)
print("2. MISSING VALUES ANALYSIS")
print("=" * 70)

missing_values = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values,
    "Missing Percentage": (
        df.isnull().sum().values / len(df)
    ) * 100
})

print(missing_values)

print("\nTotal Missing Values:", df.isnull().sum().sum())


# ============================================================
# 3. DUPLICATE VALUES
# ============================================================

print("\n" + "=" * 70)
print("3. DUPLICATE ANALYSIS")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print("Duplicate Rows:", duplicate_count)


# ============================================================
# 4. DATASET STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("4. NUMERICAL STATISTICS")
print("=" * 70)

print(df.describe().T)


# ============================================================
# 5. IDENTIFY FEATURE TYPES
# ============================================================

print("\n" + "=" * 70)
print("5. FEATURE TYPES")
print("=" * 70)

numerical_columns = df.select_dtypes(
    include=np.number
).columns.tolist()

categorical_columns = df.select_dtypes(
    include=["object", "category"]
).columns.tolist()

print("\nNumerical Columns:")
print(numerical_columns)

print("\nCategorical Columns:")
print(categorical_columns)


# ============================================================
# 6. CATEGORICAL FEATURE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("6. CATEGORICAL FEATURE ANALYSIS")
print("=" * 70)

for column in categorical_columns:

    print(f"\n--- {column} ---")
    print(df[column].value_counts())

    # Avoid plotting ApplicationDate
    if column != "ApplicationDate":

        plt.figure(figsize=(10, 5))

        df[column].value_counts().plot(
            kind="bar"
        )

        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Count")

        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(
            OUTPUT_PATH / f"{column}_distribution.png",
            dpi=300
        )

        plt.close()


# ============================================================
# 7. LOAN APPROVAL DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("7. LOAN APPROVAL DISTRIBUTION")
print("=" * 70)

loan_counts = df["LoanApproved"].value_counts()

loan_percentage = (
    df["LoanApproved"]
    .value_counts(normalize=True) * 100
)

print("\nLoan Approval Counts:")
print(loan_counts)

print("\nLoan Approval Percentage:")
print(loan_percentage)


plt.figure(figsize=(7, 5))

sns.countplot(
    data=df,
    x="LoanApproved"
)

plt.title("Loan Approval Distribution")
plt.xlabel("Loan Approved")
plt.ylabel("Number of Applicants")

plt.tight_layout()

plt.savefig(
    OUTPUT_PATH / "loan_approval_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 8. RISKSCORE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("8. RISKSCORE ANALYSIS")
print("=" * 70)

print("Minimum:", df["RiskScore"].min())
print("Maximum:", df["RiskScore"].max())
print("Mean:", df["RiskScore"].mean())
print("Median:", df["RiskScore"].median())
print("Standard Deviation:", df["RiskScore"].std())


# RiskScore Histogram

plt.figure(figsize=(8, 5))

sns.histplot(
    df["RiskScore"],
    kde=True,
    bins=30
)

plt.title("RiskScore Distribution")
plt.xlabel("RiskScore")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    OUTPUT_PATH / "risk_score_distribution.png",
    dpi=300
)

plt.close()


# RiskScore Boxplot

plt.figure(figsize=(8, 4))

sns.boxplot(
    x=df["RiskScore"]
)

plt.title("RiskScore Boxplot")

plt.tight_layout()

plt.savefig(
    OUTPUT_PATH / "risk_score_boxplot.png",
    dpi=300
)

plt.close()


# ============================================================
# 9. NUMERICAL FEATURE DISTRIBUTIONS
# ============================================================

print("\n" + "=" * 70)
print("9. NUMERICAL FEATURE DISTRIBUTIONS")
print("=" * 70)

for column in numerical_columns:

    if column in ["LoanApproved", "RiskScore"]:
        continue

    plt.figure(figsize=(8, 5))

    sns.histplot(
        df[column],
        kde=True,
        bins=30
    )

    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_PATH / f"{column}_histogram.png",
        dpi=200
    )

    plt.close()


print("Numerical feature charts saved successfully.")


# ============================================================
# 10. IMPORTANT FEATURES VS LOAN APPROVAL
# ============================================================

print("\n" + "=" * 70)
print("10. IMPORTANT FEATURES VS LOAN APPROVAL")
print("=" * 70)

important_features = [
    "CreditScore",
    "AnnualIncome",
    "LoanAmount",
    "MonthlyDebtPayments",
    "DebtToIncomeRatio"
]

for feature in important_features:

    if feature in df.columns:

        plt.figure(figsize=(8, 5))

        sns.boxplot(
            data=df,
            x="LoanApproved",
            y=feature
        )

        plt.title(
            f"{feature} vs Loan Approval"
        )

        plt.tight_layout()

        plt.savefig(
            OUTPUT_PATH / f"{feature}_vs_loan_approval.png",
            dpi=300
        )

        plt.close()


# ============================================================
# 11. EMPLOYMENT STATUS VS LOAN APPROVAL
# ============================================================

if (
    "EmploymentStatus" in df.columns
    and "LoanApproved" in df.columns
):

    plt.figure(figsize=(10, 5))

    sns.countplot(
        data=df,
        x="EmploymentStatus",
        hue="LoanApproved"
    )

    plt.title(
        "Employment Status vs Loan Approval"
    )

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_PATH /
        "employment_vs_loan_approval.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 12. FEATURE RELATIONSHIP WITH RISKSCORE
# ============================================================

print("\n" + "=" * 70)
print("12. IMPORTANT FEATURES VS RISKSCORE")
print("=" * 70)

risk_features = [
    "CreditScore",
    "AnnualIncome",
    "LoanAmount",
    "MonthlyDebtPayments",
    "DebtToIncomeRatio"
]

for feature in risk_features:

    if feature in df.columns:

        plt.figure(figsize=(8, 5))

        sns.scatterplot(
            data=df,
            x=feature,
            y="RiskScore",
            alpha=0.5
        )

        plt.title(
            f"{feature} vs RiskScore"
        )

        plt.tight_layout()

        plt.savefig(
            OUTPUT_PATH /
            f"{feature}_vs_risk_score.png",
            dpi=300
        )

        plt.close()


# ============================================================
# 13. CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("13. CORRELATION ANALYSIS")
print("=" * 70)

correlation_matrix = (
    df[numerical_columns]
    .corr()
)


print("\nCorrelation with LoanApproved:")
print(
    correlation_matrix["LoanApproved"]
    .sort_values(ascending=False)
)


print("\nCorrelation with RiskScore:")
print(
    correlation_matrix["RiskScore"]
    .sort_values(ascending=False)
)


# Correlation Heatmap

plt.figure(figsize=(18, 14))

sns.heatmap(
    correlation_matrix,
    cmap="coolwarm",
    center=0,
    linewidths=0.5
)

plt.title(
    "Numerical Feature Correlation Heatmap"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_PATH /
    "correlation_heatmap.png",
    dpi=300
)

plt.close()


# ============================================================
# 14. TOP CORRELATED FEATURES
# ============================================================

print("\n" + "=" * 70)
print("14. TOP FEATURES FOR LOAN APPROVAL")
print("=" * 70)

loan_correlations = (
    correlation_matrix["LoanApproved"]
    .drop("LoanApproved")
    .abs()
    .sort_values(ascending=False)
)

print(loan_correlations)


print("\n" + "=" * 70)
print("15. TOP FEATURES FOR RISKSCORE")
print("=" * 70)

risk_correlations = (
    correlation_matrix["RiskScore"]
    .drop("RiskScore")
    .abs()
    .sort_values(ascending=False)
)

print(risk_correlations)


# ============================================================
# 16. LOAN APPROVAL BY CATEGORICAL FEATURES
# ============================================================

print("\n" + "=" * 70)
print("16. CATEGORICAL FEATURES VS LOAN APPROVAL")
print("=" * 70)

for column in categorical_columns:

    if column == "ApplicationDate":
        continue

    print(f"\nLoan Approval Rate by {column}")

    approval_rate = pd.crosstab(
        df[column],
        df["LoanApproved"],
        normalize="index"
    ) * 100

    print(approval_rate)


# ============================================================
# 17. OUTLIER ANALYSIS USING IQR
# ============================================================

print("\n" + "=" * 70)
print("17. OUTLIER ANALYSIS")
print("=" * 70)

outlier_results = []

for column in numerical_columns:

    if column in [
        "LoanApproved",
        "RiskScore"
    ]:
        continue

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    outlier_results.append({
        "Feature": column,
        "Outlier Count": len(outliers),
        "Outlier Percentage":
            round(
                (len(outliers) / len(df)) * 100,
                2
            )
    })


outlier_df = pd.DataFrame(
    outlier_results
)

outlier_df = outlier_df.sort_values(
    by="Outlier Count",
    ascending=False
)

print(outlier_df)


# Save outlier report

outlier_df.to_csv(
    OUTPUT_PATH / "outlier_analysis.csv",
    index=False
)


# ============================================================
# 18. POSSIBLE DATA LEAKAGE CHECK
# ============================================================

print("\n" + "=" * 70)
print("18. POSSIBLE DATA LEAKAGE CHECK")
print("=" * 70)

possible_leakage_features = [
    "ApplicationDate",
    "RiskScore",
    "LoanApproved",
    "InterestRate",
    "MonthlyLoanPayment"
]

for feature in possible_leakage_features:

    if feature in df.columns:
        print(
            f"WARNING: Review feature -> {feature}"
        )


# ============================================================
# 19. SAVE DATASET SUMMARY
# ============================================================

summary = {
    "Total Rows": [df.shape[0]],
    "Total Columns": [df.shape[1]],
    "Total Missing Values": [
        df.isnull().sum().sum()
    ],
    "Duplicate Rows": [
        df.duplicated().sum()
    ],
    "Approval Rate (%)": [
        round(
            df["LoanApproved"].mean() * 100,
            2
        )
    ],
    "Average RiskScore": [
        round(
            df["RiskScore"].mean(),
            2
        )
    ]
}

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    OUTPUT_PATH / "dataset_summary.csv",
    index=False
)


# ============================================================
# EDA COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nCheck the following folder for charts and reports:")

print(OUTPUT_PATH)

print("\nGenerated files include:")
print("- Dataset summary")
print("- Loan approval distribution")
print("- RiskScore distribution")
print("- Numerical feature distributions")
print("- Feature vs Loan Approval charts")
print("- Feature vs RiskScore charts")
print("- Correlation heatmap")
print("- Outlier analysis")

print("\nNext Step: Feature Selection and Data Preprocessing")