# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# RISK ENGINE TESTING
# ============================================================

from risk_engine import calculate_risk_score


# ============================================================
# PROJECT HEADER
# ============================================================

print("\n" + "=" * 70)
print("SMART FINANCIAL RISK ENGINE - TESTING")
print("=" * 70)


# ============================================================
# TEST CASE 1 - LOW RISK APPLICANT
# ============================================================

print("\n" + "-" * 70)
print("TEST CASE 1: LOW RISK APPLICANT")
print("-" * 70)

low_risk_applicant = calculate_risk_score(

    age=35,
    employment_status="Employed",
    experience=12,
    annual_income=120000,
    credit_score=780,
    monthly_debt=800,
    savings_balance=70000,
    loan_amount=20000,
    loan_duration=36

)

print("\nRisk Score:", low_risk_applicant["risk_score"])
print("Risk Level:", low_risk_applicant["risk_level"])

print(
    "Debt-to-Income Ratio:",
    low_risk_applicant["debt_to_income_ratio"]
)

print(
    "Loan-to-Income Ratio:",
    low_risk_applicant["loan_to_income_ratio"]
)

print(
    "Savings-to-Loan Ratio:",
    low_risk_applicant["savings_to_loan_ratio"]
)

print("\nPositive Factors:")

for factor in low_risk_applicant["positive_factors"]:
    print("✓", factor)

print("\nRisk Factors:")

if low_risk_applicant["risk_factors"]:

    for factor in low_risk_applicant["risk_factors"]:
        print("⚠", factor)

else:

    print("None")


# ============================================================
# TEST CASE 2 - MEDIUM RISK APPLICANT
# ============================================================

print("\n" + "-" * 70)
print("TEST CASE 2: MEDIUM RISK APPLICANT")
print("-" * 70)

medium_risk_applicant = calculate_risk_score(

    age=30,
    employment_status="Self-Employed",
    experience=6,
    annual_income=60000,
    credit_score=670,
    monthly_debt=1800,
    savings_balance=10000,
    loan_amount=30000,
    loan_duration=60

)

print("\nRisk Score:", medium_risk_applicant["risk_score"])
print("Risk Level:", medium_risk_applicant["risk_level"])

print(
    "Debt-to-Income Ratio:",
    medium_risk_applicant["debt_to_income_ratio"]
)

print(
    "Loan-to-Income Ratio:",
    medium_risk_applicant["loan_to_income_ratio"]
)

print(
    "Savings-to-Loan Ratio:",
    medium_risk_applicant["savings_to_loan_ratio"]
)

print("\nPositive Factors:")

for factor in medium_risk_applicant["positive_factors"]:
    print("✓", factor)

print("\nRisk Factors:")

if medium_risk_applicant["risk_factors"]:

    for factor in medium_risk_applicant["risk_factors"]:
        print("⚠", factor)


# ============================================================
# TEST CASE 3 - HIGH RISK APPLICANT
# ============================================================

print("\n" + "-" * 70)
print("TEST CASE 3: HIGH RISK APPLICANT")
print("-" * 70)

high_risk_applicant = calculate_risk_score(

    age=24,
    employment_status="Unemployed",
    experience=1,
    annual_income=25000,
    credit_score=550,
    monthly_debt=1800,
    savings_balance=1000,
    loan_amount=40000,
    loan_duration=96

)

print("\nRisk Score:", high_risk_applicant["risk_score"])
print("Risk Level:", high_risk_applicant["risk_level"])

print(
    "Debt-to-Income Ratio:",
    high_risk_applicant["debt_to_income_ratio"]
)

print(
    "Loan-to-Income Ratio:",
    high_risk_applicant["loan_to_income_ratio"]
)

print(
    "Savings-to-Loan Ratio:",
    high_risk_applicant["savings_to_loan_ratio"]
)

print("\nPositive Factors:")

if high_risk_applicant["positive_factors"]:

    for factor in high_risk_applicant["positive_factors"]:
        print("✓", factor)

else:

    print("None")

print("\nRisk Factors:")

for factor in high_risk_applicant["risk_factors"]:
    print("⚠", factor)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("RISK ENGINE TESTING COMPLETED SUCCESSFULLY")
print("=" * 70)