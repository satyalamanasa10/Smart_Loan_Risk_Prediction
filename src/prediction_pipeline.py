# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# UNIFIED PREDICTION PIPELINE
# ============================================================


import os
import sys
import joblib
import pandas as pd


# ============================================================
# PROJECT PATH CONFIGURATION
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    CURRENT_DIR
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "loan_approval_model.pkl"
)


# ============================================================
# IMPORT CUSTOM ENGINES
# ============================================================

from src.risk_engine import calculate_risk_score
from src.recommendation_engine import generate_recommendations

# ============================================================
# LOAD LOAN APPROVAL MODEL
# ============================================================

print("\nLoading Loan Approval Model...")

loan_model = joblib.load(MODEL_PATH)

print("Loan Approval Model Loaded Successfully!")


# ============================================================
# FEATURE ENGINEERING FUNCTION
# ============================================================

def create_engineered_features(data):
    """
    Create the same engineered features used
    during model training.
    """

    data = data.copy()


    # --------------------------------------------------------
    # MONTHLY INCOME
    # --------------------------------------------------------

    data["MonthlyIncome_Calculated"] = (
        data["AnnualIncome"] / 12
    )


    # --------------------------------------------------------
    # DEBT TO INCOME RATIO
    # --------------------------------------------------------

    data["DebtToIncome_Calculated"] = (
        data["MonthlyDebtPayments"] * 12
    ) / data["AnnualIncome"].replace(0, 1)


    # --------------------------------------------------------
    # LOAN TO INCOME RATIO
    # --------------------------------------------------------

    data["LoanToIncomeRatio"] = (
        data["LoanAmount"]
        / data["AnnualIncome"].replace(0, 1)
    )


    # --------------------------------------------------------
    # SAVINGS TO LOAN RATIO
    # --------------------------------------------------------

    data["SavingsToLoanRatio"] = (
        data["SavingsAccountBalance"]
        / data["LoanAmount"].replace(0, 1)
    )


    # --------------------------------------------------------
    # EXPERIENCE TO AGE RATIO
    # --------------------------------------------------------

    data["ExperienceToAgeRatio"] = (
        data["Experience"]
        / data["Age"].replace(0, 1)
    )


    return data


# ============================================================
# MAIN PREDICTION FUNCTION
# ============================================================

def predict_loan(user_input):
    """
    Complete Smart Loan Prediction Pipeline.

    Input:
        Dictionary containing applicant information.

    Output:
        Complete financial analysis including:
        - Loan Prediction
        - Approval Probability
        - Risk Analysis
        - Personalized Recommendations
    """


    # ========================================================
    # CONVERT INPUT INTO DATAFRAME
    # ========================================================

    input_df = pd.DataFrame([user_input])


    # ========================================================
    # CREATE ENGINEERED FEATURES
    # ========================================================

    processed_input = create_engineered_features(
        input_df
    )


    # ========================================================
    # LOAN APPROVAL PREDICTION
    # ========================================================

    prediction = loan_model.predict(
        processed_input
    )[0]


    probabilities = loan_model.predict_proba(
        processed_input
    )[0]


    # ========================================================
    # EXTRACT APPROVAL PROBABILITY
    # ========================================================

    approval_probability = round(
        probabilities[1] * 100,
        2
    )

    rejection_probability = round(
        probabilities[0] * 100,
        2
    )


    # ========================================================
    # DECISION LABEL
    # ========================================================

    if prediction == 1:

        loan_decision = "Approved"

    else:

        loan_decision = "Not Approved"


    # ========================================================
    # SMART RISK ANALYSIS
    # ========================================================

    risk_analysis = calculate_risk_score(

        age=user_input["Age"],

        employment_status=user_input[
            "EmploymentStatus"
        ],

        experience=user_input["Experience"],

        annual_income=user_input[
            "AnnualIncome"
        ],

        credit_score=user_input[
            "CreditScore"
        ],

        monthly_debt=user_input[
            "MonthlyDebtPayments"
        ],

        savings_balance=user_input[
            "SavingsAccountBalance"
        ],

        loan_amount=user_input[
            "LoanAmount"
        ],

        loan_duration=user_input[
            "LoanDuration"
        ]

    )


    # ========================================================
    # GENERATE RECOMMENDATIONS
    # ========================================================

    recommendations = generate_recommendations(
        risk_analysis
    )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    result = {

        "loan_prediction": {

            "decision": loan_decision,

            "approval_probability":
                approval_probability,

            "rejection_probability":
                rejection_probability

        },


        "risk_analysis":
            risk_analysis,


        "recommendations":
            recommendations

    }


    return result


# ============================================================
# TEST MESSAGE
# ============================================================

if __name__ == "__main__":

    print("\nPrediction Pipeline Ready!")