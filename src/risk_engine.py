# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# SMART FINANCIAL RISK ENGINE
# VERSION 2 - REFINED SCORING SYSTEM
# ============================================================


def calculate_risk_score(
    age,
    employment_status,
    experience,
    annual_income,
    credit_score,
    monthly_debt,
    savings_balance,
    loan_amount,
    loan_duration
):
    """
    Calculate an explainable financial risk score.

    Risk Score Range:
    0   = Very Low Risk
    100 = Very High Risk
    """


    # ========================================================
    # INITIALIZE RISK SCORE
    # ========================================================

    # Small base risk ensures scores do not unrealistically
    # start at exactly zero.
    risk_score = 5

    risk_factors = []
    positive_factors = []


    # ========================================================
    # 1. CREDIT SCORE ANALYSIS
    # Maximum Contribution: 25 Points
    # ========================================================

    if credit_score >= 750:

        credit_risk = 0

        positive_factors.append(
            "Excellent credit score"
        )

    elif credit_score >= 700:

        credit_risk = 4

        positive_factors.append(
            "Good credit score"
        )

    elif credit_score >= 650:

        credit_risk = 8

        positive_factors.append(
            "Fair credit score"
        )

    elif credit_score >= 600:

        credit_risk = 15

        risk_factors.append(
            "Below-average credit score"
        )

    else:

        credit_risk = 25

        risk_factors.append(
            "Low credit score"
        )


    risk_score += credit_risk


    # ========================================================
    # 2. DEBT-TO-INCOME RATIO
    # Maximum Contribution: 20 Points
    # ========================================================

    annual_debt = monthly_debt * 12

    debt_to_income = annual_debt / max(
        annual_income,
        1
    )


    if debt_to_income < 0.20:

        debt_risk = 0

        positive_factors.append(
            "Low debt burden"
        )

    elif debt_to_income < 0.35:

        debt_risk = 5

    elif debt_to_income < 0.50:

        debt_risk = 12

        risk_factors.append(
            "Moderate debt-to-income ratio"
        )

    else:

        debt_risk = 20

        risk_factors.append(
            "High debt-to-income ratio"
        )


    risk_score += debt_risk


    # ========================================================
    # 3. LOAN-TO-INCOME RATIO
    # Maximum Contribution: 18 Points
    # ========================================================

    loan_to_income = loan_amount / max(
        annual_income,
        1
    )


    if loan_to_income < 0.20:

        loan_risk = 0

        positive_factors.append(
            "Loan amount is manageable compared to income"
        )

    elif loan_to_income < 0.50:

        loan_risk = 5

    elif loan_to_income < 0.80:

        loan_risk = 10

        risk_factors.append(
            "Loan amount is relatively high compared to income"
        )

    else:

        loan_risk = 18

        risk_factors.append(
            "Loan amount is very high compared to income"
        )


    risk_score += loan_risk


    # ========================================================
    # 4. SAVINGS BUFFER
    # Maximum Contribution: 12 Points
    # ========================================================

    savings_to_loan = savings_balance / max(
        loan_amount,
        1
    )


    if savings_to_loan >= 0.50:

        savings_risk = 0

        positive_factors.append(
            "Strong savings buffer"
        )

    elif savings_to_loan >= 0.20:

        savings_risk = 3

    elif savings_to_loan >= 0.10:

        savings_risk = 7

    else:

        savings_risk = 12

        risk_factors.append(
            "Low savings compared to loan amount"
        )


    risk_score += savings_risk


    # ========================================================
    # 5. EMPLOYMENT STABILITY
    # Maximum Contribution: 10 Points
    # ========================================================

    employment_status = str(
        employment_status
    ).lower()


    if employment_status == "employed":

        employment_risk = 0

        positive_factors.append(
            "Stable employment"
        )

    elif employment_status == "self-employed":

        employment_risk = 5

        positive_factors.append(
            "Self-employed with moderate income stability"
        )

    else:

        employment_risk = 10

        risk_factors.append(
            "Employment instability"
        )


    risk_score += employment_risk


    # ========================================================
    # 6. WORK EXPERIENCE
    # Maximum Contribution: 5 Points
    # ========================================================

    if experience >= 10:

        experience_risk = 0

        positive_factors.append(
            "Strong work experience"
        )

    elif experience >= 5:

        experience_risk = 2

    else:

        experience_risk = 5

        risk_factors.append(
            "Limited work experience"
        )


    risk_score += experience_risk


    # ========================================================
    # 7. LOAN DURATION
    # Maximum Contribution: 5 Points
    # ========================================================

    if loan_duration <= 36:

        duration_risk = 0

    elif loan_duration <= 60:

        duration_risk = 2

    else:

        duration_risk = 5

        risk_factors.append(
            "Long loan repayment duration"
        )


    risk_score += duration_risk


    # ========================================================
    # FINAL SCORE NORMALIZATION
    # ========================================================

    risk_score = round(
        min(
            max(
                risk_score,
                0
            ),
            100
        ),
        2
    )


    # ========================================================
    # RISK LEVEL CLASSIFICATION
    # ========================================================

    if risk_score <= 20:

        risk_level = "Low"

    elif risk_score <= 50:

        risk_level = "Medium"

    elif risk_score <= 75:

        risk_level = "High"

    else:

        risk_level = "Very High"


    # ========================================================
    # RETURN COMPLETE ANALYSIS
    # ========================================================

    return {

        "risk_score": risk_score,

        "risk_level": risk_level,

        "debt_to_income_ratio": round(
            debt_to_income,
            3
        ),

        "loan_to_income_ratio": round(
            loan_to_income,
            3
        ),

        "savings_to_loan_ratio": round(
            savings_to_loan,
            3
        ),

        "risk_factors": risk_factors,

        "positive_factors": positive_factors

    }