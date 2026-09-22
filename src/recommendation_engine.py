# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# PERSONALIZED RECOMMENDATION ENGINE
# ============================================================


def generate_recommendations(risk_analysis):
    """
    Generate personalized financial recommendations
    based on the Smart Risk Engine analysis.

    This module does NOT calculate the risk score.
    It only explains the identified strengths/risk factors
    and generates actionable recommendations.
    """

    # ========================================================
    # EXTRACT RISK ANALYSIS DATA
    # ========================================================

    risk_score = risk_analysis["risk_score"]
    risk_level = risk_analysis["risk_level"]

    debt_to_income = risk_analysis["debt_to_income_ratio"]
    loan_to_income = risk_analysis["loan_to_income_ratio"]
    savings_to_loan = risk_analysis["savings_to_loan_ratio"]

    risk_factors = risk_analysis.get(
        "risk_factors",
        []
    )

    positive_factors = risk_analysis.get(
        "positive_factors",
        []
    )


    # ========================================================
    # INITIALIZE RESULT LISTS
    # ========================================================

    recommendations = []
    strengths = []
    priority_actions = []


    # ========================================================
    # 1. OVERALL RISK LEVEL
    # ========================================================

    if risk_level == "Low":

        recommendations.append(
            "Your overall financial risk is low. "
            "Your current financial profile appears relatively stable."
        )

        priority_actions.append(
            "Maintain your current financial habits and repayment discipline."
        )


    elif risk_level == "Medium":

        recommendations.append(
            "Your financial profile shows a moderate level of risk. "
            "Improving the areas identified below could strengthen your "
            "financial position."
        )


    elif risk_level == "High":

        recommendations.append(
            "Your financial profile contains several risk factors. "
            "Addressing the identified areas before taking additional credit "
            "could improve your financial stability."
        )

        priority_actions.append(
            "Address the highest-risk financial factors before taking "
            "additional credit."
        )


    else:

        recommendations.append(
            "Your financial profile indicates very high risk. "
            "Carefully review your existing financial commitments before "
            "taking on additional debt."
        )

        priority_actions.append(
            "Avoid increasing financial commitments until major risk factors "
            "are addressed."
        )


    # ========================================================
    # 2. CREDIT SCORE ANALYSIS
    # ========================================================

    if "Low credit score" in risk_factors:

        recommendations.append(
            "Your credit score is low and may negatively affect your "
            "borrowing profile. Focus on timely repayments and responsible "
            "credit usage."
        )

        priority_actions.append(
            "Improve your credit repayment history and credit usage."
        )


    elif "Below-average credit score" in risk_factors:

        recommendations.append(
            "Your credit score is below average. Maintaining timely "
            "repayments and reducing unnecessary credit usage could help "
            "strengthen your credit profile."
        )

        priority_actions.append(
            "Work on improving your credit score."
        )


    elif "Excellent credit score" in positive_factors:

        strengths.append(
            "Excellent credit score supports a strong borrowing profile."
        )


    elif "Good credit score" in positive_factors:

        strengths.append(
            "Good credit score supports a healthy borrowing profile."
        )


    elif "Fair credit score" in positive_factors:

        strengths.append(
            "Your credit score is fair and provides some support to your "
            "borrowing profile."
        )


    # ========================================================
    # 3. DEBT-TO-INCOME ANALYSIS
    # ========================================================

    if debt_to_income >= 0.50:

        recommendations.append(
            f"Your debt-to-income ratio is {debt_to_income:.0%}, "
            "which indicates a high existing debt burden relative to income. "
            "Reducing monthly debt obligations could improve repayment capacity."
        )

        priority_actions.append(
            "Reduce existing monthly debt obligations."
        )


    elif debt_to_income >= 0.35:

        recommendations.append(
            f"Your debt-to-income ratio is {debt_to_income:.0%}, "
            "indicating a moderately high debt burden. "
            "Reducing existing debt could improve financial flexibility."
        )

        priority_actions.append(
            "Review and reduce existing debt where possible."
        )


    elif debt_to_income >= 0.20:

        recommendations.append(
            f"Your debt-to-income ratio is {debt_to_income:.0%}. "
            "Your existing debt is manageable but should be monitored "
            "before taking on additional credit."
        )


    else:

        strengths.append(
            f"Low debt burden with a debt-to-income ratio of "
            f"{debt_to_income:.0%}."
        )


    # ========================================================
    # 4. LOAN-TO-INCOME ANALYSIS
    # ========================================================

    if loan_to_income >= 0.80:

        recommendations.append(
            f"Your requested loan is approximately "
            f"{loan_to_income:.0%} of your annual income. "
            "This represents a high loan-to-income level."
        )

        priority_actions.append(
            "Consider reducing the requested loan amount."
        )


    elif loan_to_income >= 0.50:

        recommendations.append(
            f"Your requested loan is approximately "
            f"{loan_to_income:.0%} of your annual income. "
            "A smaller loan amount may improve affordability."
        )

        priority_actions.append(
            "Review whether the requested loan amount can be reduced."
        )


    elif loan_to_income >= 0.20:

        recommendations.append(
            f"Your requested loan is approximately "
            f"{loan_to_income:.0%} of your annual income. "
            "Ensure the repayment obligation remains affordable within "
            "your overall budget."
        )


    else:

        strengths.append(
            "The requested loan amount is relatively manageable "
            "compared with annual income."
        )


    # ========================================================
    # 5. SAVINGS-TO-LOAN ANALYSIS
    # ========================================================

    if savings_to_loan < 0.10:

        recommendations.append(
            f"Your savings are approximately "
            f"{savings_to_loan:.0%} of the requested loan amount. "
            "This indicates a limited financial buffer."
        )

        priority_actions.append(
            "Build a stronger emergency savings buffer."
        )


    elif savings_to_loan < 0.20:

        recommendations.append(
            f"Your savings are approximately "
            f"{savings_to_loan:.0%} of the requested loan amount. "
            "Increasing your savings could provide greater financial protection."
        )

        priority_actions.append(
            "Increase savings before taking on larger financial commitments."
        )


    elif savings_to_loan < 0.50:

        recommendations.append(
            "Your savings provide some financial support, but maintaining "
            "additional emergency savings could improve financial resilience."
        )


    else:

        strengths.append(
            "Strong savings buffer provides additional financial support."
        )


    # ========================================================
    # 6. EMPLOYMENT STABILITY
    # ========================================================

    if "Stable employment" in positive_factors:

        strengths.append(
            "Stable employment provides a consistent income source."
        )


    elif "Self-employed with moderate income stability" in positive_factors:

        strengths.append(
            "Self-employment provides an income source, although income "
            "stability may vary."
        )


    elif "Employment instability" in risk_factors:

        recommendations.append(
            "Your current employment status may indicate lower income "
            "stability. Maintaining a reliable income source or providing "
            "additional financial support information could strengthen "
            "your financial profile."
        )

        priority_actions.append(
            "Strengthen income stability before taking on additional debt."
        )


    # ========================================================
    # 7. WORK EXPERIENCE
    # ========================================================

    if "Strong work experience" in positive_factors:

        strengths.append(
            "Strong work experience supports employment stability."
        )


    elif "Limited work experience" in risk_factors:

        recommendations.append(
            "Your work experience is relatively limited. Building a stable "
            "employment history may strengthen your future borrowing profile."
        )


    # ========================================================
    # 8. LONG LOAN DURATION
    # ========================================================

    if "Long loan repayment duration" in risk_factors:

        recommendations.append(
            "The selected repayment duration is relatively long. "
            "A longer repayment period can extend the period of financial "
            "commitment, so review the repayment schedule carefully."
        )

        priority_actions.append(
            "Review whether a shorter repayment period is affordable."
        )


    # ========================================================
    # 9. CONVERT EXISTING POSITIVE FACTORS INTO STRENGTHS
    # ========================================================

    for factor in positive_factors:

        if factor == "Excellent credit score":
            continue

        if factor == "Good credit score":
            continue

        if factor == "Fair credit score":
            continue

        if factor == "Stable employment":
            continue

        if factor == "Self-employed with moderate income stability":
            continue

        if factor == "Strong work experience":
            continue

        if factor == "Low debt burden":
            continue

        if factor == "Loan amount is manageable compared to income":
            continue

        if factor == "Strong savings buffer":
            continue

        if factor not in strengths:
            strengths.append(factor)


    # ========================================================
    # 10. HANDLE NO-SPECIFIC-RISK SITUATION
    # ========================================================

    if not risk_factors and risk_level == "Low":

        recommendations.append(
            "No major financial risk factors were identified by the "
            "current risk analysis."
        )


    # ========================================================
    # 11. GENERAL MAINTENANCE ADVICE FOR LOW RISK
    # ========================================================

    if risk_level == "Low":

        recommendations.append(
            "Continue maintaining timely repayments, responsible credit "
            "usage, and an adequate savings buffer."
        )


    # ========================================================
    # 12. REMOVE DUPLICATES
    # ========================================================

    recommendations = list(
        dict.fromkeys(recommendations)
    )

    strengths = list(
        dict.fromkeys(strengths)
    )

    priority_actions = list(
        dict.fromkeys(priority_actions)
    )


    # ========================================================
    # 13. LIMIT EXCESSIVE REPETITION
    # ========================================================

    # Keep the output useful and readable for the dashboard.
    recommendations = recommendations[:7]
    strengths = strengths[:7]
    priority_actions = priority_actions[:5]


    # ========================================================
    # 14. FINAL RESULT
    # ========================================================

    return {

        "risk_summary": {
            "score": risk_score,
            "level": risk_level
        },

        "recommendations": recommendations,

        "priority_actions": priority_actions,

        "financial_strengths": strengths

    }