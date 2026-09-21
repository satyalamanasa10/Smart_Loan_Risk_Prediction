# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# RECOMMENDATION ENGINE TESTING
# ============================================================

from risk_engine import calculate_risk_score
from recommendation_engine import generate_recommendations


# ============================================================
# FUNCTION TO DISPLAY RESULTS
# ============================================================

def display_result(title, applicant):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    # --------------------------------------------------------
    # STEP 1: RISK ANALYSIS
    # --------------------------------------------------------

    risk_analysis = calculate_risk_score(**applicant)

    # --------------------------------------------------------
    # STEP 2: GENERATE RECOMMENDATIONS
    # --------------------------------------------------------

    recommendation_result = generate_recommendations(
        risk_analysis
    )

    # ========================================================
    # DISPLAY RISK ANALYSIS
    # ========================================================

    print("\nRISK ASSESSMENT")

    print("Risk Score:",
          risk_analysis["risk_score"])

    print("Risk Level:",
          risk_analysis["risk_level"])

    print("\nFinancial Ratios:")

    print(
        "Debt-to-Income Ratio:",
        risk_analysis["debt_to_income_ratio"]
    )

    print(
        "Loan-to-Income Ratio:",
        risk_analysis["loan_to_income_ratio"]
    )

    print(
        "Savings-to-Loan Ratio:",
        risk_analysis["savings_to_loan_ratio"]
    )

    # ========================================================
    # DISPLAY RECOMMENDATIONS
    # ========================================================

    print("\n" + "-" * 70)
    print("PERSONALIZED RECOMMENDATIONS")
    print("-" * 70)

    for recommendation in recommendation_result["recommendations"]:

        print("💡", recommendation)


    # ========================================================
    # DISPLAY PRIORITY ACTIONS
    # ========================================================

    print("\n" + "-" * 70)
    print("PRIORITY ACTIONS")
    print("-" * 70)

    if recommendation_result["priority_actions"]:

        for action in recommendation_result["priority_actions"]:

            print("🎯", action)

    else:

        print("No immediate priority actions required.")


    # ========================================================
    # DISPLAY FINANCIAL STRENGTHS
    # ========================================================

    print("\n" + "-" * 70)
    print("FINANCIAL STRENGTHS")
    print("-" * 70)

    if recommendation_result["financial_strengths"]:

        for strength in recommendation_result["financial_strengths"]:

            print("✓", strength)

    else:

        print("No major financial strengths identified.")


# ============================================================
# PROJECT HEADER
# ============================================================

print("\n" + "=" * 70)
print("SMART LOAN SYSTEM - RECOMMENDATION ENGINE TESTING")
print("=" * 70)


# ============================================================
# TEST CASE 1 — LOW RISK APPLICANT
# ============================================================

low_risk_applicant = {

    "age": 35,
    "employment_status": "Employed",
    "experience": 12,
    "annual_income": 120000,
    "credit_score": 780,
    "monthly_debt": 800,
    "savings_balance": 70000,
    "loan_amount": 20000,
    "loan_duration": 36

}

display_result(
    "TEST CASE 1: LOW RISK APPLICANT",
    low_risk_applicant
)


# ============================================================
# TEST CASE 2 — MEDIUM RISK APPLICANT
# ============================================================

medium_risk_applicant = {

    "age": 30,
    "employment_status": "Self-Employed",
    "experience": 6,
    "annual_income": 60000,
    "credit_score": 670,
    "monthly_debt": 1800,
    "savings_balance": 10000,
    "loan_amount": 30000,
    "loan_duration": 60

}

display_result(
    "TEST CASE 2: MEDIUM RISK APPLICANT",
    medium_risk_applicant
)


# ============================================================
# TEST CASE 3 — VERY HIGH RISK APPLICANT
# ============================================================

high_risk_applicant = {

    "age": 24,
    "employment_status": "Unemployed",
    "experience": 1,
    "annual_income": 25000,
    "credit_score": 550,
    "monthly_debt": 1800,
    "savings_balance": 1000,
    "loan_amount": 40000,
    "loan_duration": 96

}

display_result(
    "TEST CASE 3: VERY HIGH RISK APPLICANT",
    high_risk_applicant
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("RECOMMENDATION ENGINE TESTING COMPLETED SUCCESSFULLY")
print("=" * 70)