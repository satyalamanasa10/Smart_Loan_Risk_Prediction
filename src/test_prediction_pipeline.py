# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# COMPLETE PREDICTION PIPELINE TESTING
# ============================================================

from prediction_pipeline import predict_loan


# ============================================================
# DISPLAY RESULT FUNCTION
# ============================================================

def display_prediction_result(title, user_input):

    print("\n" + "=" * 75)
    print(title)
    print("=" * 75)

    # --------------------------------------------------------
    # RUN COMPLETE PREDICTION PIPELINE
    # --------------------------------------------------------

    result = predict_loan(user_input)


    # ========================================================
    # LOAN PREDICTION
    # ========================================================

    print("\nLOAN ELIGIBILITY PREDICTION")
    print("-" * 75)

    loan_prediction = result["loan_prediction"]

    print(
        "Decision:",
        loan_prediction["decision"]
    )

    print(
        "Approval Probability:",
        f'{loan_prediction["approval_probability"]}%'
    )

    print(
        "Rejection Probability:",
        f'{loan_prediction["rejection_probability"]}%'
    )


    # ========================================================
    # RISK ANALYSIS
    # ========================================================

    print("\nFINANCIAL RISK ANALYSIS")
    print("-" * 75)

    risk = result["risk_analysis"]

    print(
        "Risk Score:",
        risk["risk_score"],
        "/ 100"
    )

    print(
        "Risk Level:",
        risk["risk_level"]
    )

    print(
        "Debt-to-Income Ratio:",
        risk["debt_to_income_ratio"]
    )

    print(
        "Loan-to-Income Ratio:",
        risk["loan_to_income_ratio"]
    )

    print(
        "Savings-to-Loan Ratio:",
        risk["savings_to_loan_ratio"]
    )


    # ========================================================
    # RISK FACTORS
    # ========================================================

    print("\nRISK FACTORS")
    print("-" * 75)

    if risk["risk_factors"]:

        for factor in risk["risk_factors"]:
            print("⚠", factor)

    else:

        print("No major risk factors identified.")


    # ========================================================
    # FINANCIAL STRENGTHS
    # ========================================================

    print("\nFINANCIAL STRENGTHS")
    print("-" * 75)

    recommendation_data = result["recommendations"]

    if recommendation_data["financial_strengths"]:

        for strength in recommendation_data["financial_strengths"]:
            print("✓", strength)

    else:

        print("No major strengths identified.")


    # ========================================================
    # PERSONALIZED RECOMMENDATIONS
    # ========================================================

    print("\nPERSONALIZED RECOMMENDATIONS")
    print("-" * 75)

    for recommendation in recommendation_data["recommendations"]:
        print("💡", recommendation)


    # ========================================================
    # PRIORITY ACTIONS
    # ========================================================

    print("\nPRIORITY ACTIONS")
    print("-" * 75)

    if recommendation_data["priority_actions"]:

        for action in recommendation_data["priority_actions"]:
            print("🎯", action)

    else:

        print("No immediate priority actions required.")


# ============================================================
# PROJECT HEADER
# ============================================================

print("\n" + "=" * 75)
print("SMART LOAN SYSTEM - COMPLETE PREDICTION PIPELINE TEST")
print("=" * 75)


# ============================================================
# TEST CASE 1 — STRONG APPLICANT
# ============================================================

strong_applicant = {

    "Age": 35,
    "EmploymentStatus": "Employed",
    "EducationLevel": "Master",
    "Experience": 12,
    "HomeOwnershipStatus": "Own",

    "AnnualIncome": 120000,
    "CreditScore": 780,
    "MonthlyDebtPayments": 800,
    "SavingsAccountBalance": 70000,

    "LoanAmount": 20000,
    "LoanDuration": 36,
    "LoanPurpose": "Home"

}

display_prediction_result(
    "TEST CASE 1: STRONG FINANCIAL PROFILE",
    strong_applicant
)


# ============================================================
# TEST CASE 2 — MODERATE APPLICANT
# ============================================================

moderate_applicant = {

    "Age": 30,
    "EmploymentStatus": "Self-Employed",
    "EducationLevel": "Bachelor",
    "Experience": 6,
    "HomeOwnershipStatus": "Rent",

    "AnnualIncome": 60000,
    "CreditScore": 670,
    "MonthlyDebtPayments": 1800,
    "SavingsAccountBalance": 10000,

    "LoanAmount": 30000,
    "LoanDuration": 60,
    "LoanPurpose": "Auto"

}

display_prediction_result(
    "TEST CASE 2: MODERATE FINANCIAL PROFILE",
    moderate_applicant
)


# ============================================================
# TEST CASE 3 — HIGH RISK APPLICANT
# ============================================================

high_risk_applicant = {

    "Age": 24,
    "EmploymentStatus": "Unemployed",
    "EducationLevel": "High School",
    "Experience": 1,
    "HomeOwnershipStatus": "Rent",

    "AnnualIncome": 25000,
    "CreditScore": 550,
    "MonthlyDebtPayments": 1800,
    "SavingsAccountBalance": 1000,

    "LoanAmount": 40000,
    "LoanDuration": 96,
    "LoanPurpose": "Debt Consolidation"

}

display_prediction_result(
    "TEST CASE 3: HIGH RISK FINANCIAL PROFILE",
    high_risk_applicant
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 75)
print("COMPLETE PREDICTION PIPELINE TEST COMPLETED")
print("=" * 75)