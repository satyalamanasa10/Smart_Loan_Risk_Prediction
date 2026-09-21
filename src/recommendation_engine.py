# ============================================================
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# PERSONALIZED RECOMMENDATION ENGINE
# ============================================================


def generate_recommendations(risk_analysis):
    """
    Generate personalized financial recommendations
    based on the Smart Risk Engine analysis.
    """

    # ========================================================
    # EXTRACT RISK ANALYSIS DATA
    # ========================================================

    risk_score = risk_analysis["risk_score"]
    risk_level = risk_analysis["risk_level"]

    debt_to_income = risk_analysis["debt_to_income_ratio"]
    loan_to_income = risk_analysis["loan_to_income_ratio"]
    savings_to_loan = risk_analysis["savings_to_loan_ratio"]

    risk_factors = risk_analysis["risk_factors"]
    positive_factors = risk_analysis["positive_factors"]


    # ========================================================
    # INITIALIZE RECOMMENDATION LISTS
    # ========================================================

    recommendations = []
    strengths = []
    priority_actions = []


    # ========================================================
    # OVERALL RISK LEVEL RECOMMENDATION
    # ========================================================

    if risk_level == "Low":

        recommendations.append(
            "Your financial profile appears healthy. "
            "You are in a relatively strong position for loan consideration."
        )

        strengths.append(
            "Overall financial risk is low."
        )


    elif risk_level == "Medium":

        recommendations.append(
            "Your financial profile is moderately stable, "
            "but improving a few financial areas could reduce your risk further."
        )

        priority_actions.append(
            "Review your existing debt and loan requirements before applying."
        )


    elif risk_level == "High":

        recommendations.append(
            "Your financial profile has noticeable risk factors. "
            "Improving key financial indicators before applying is recommended."
        )

        priority_actions.append(
            "Focus on reducing financial risk before taking additional credit."
        )


    else:

        recommendations.append(
            "Your current financial profile indicates a high level of risk. "
            "Consider improving your financial position before applying for a large loan."
        )

        priority_actions.append(
            "Avoid taking additional large financial commitments immediately."
        )


    # ========================================================
    # CREDIT SCORE RECOMMENDATIONS
    # ========================================================

    if "Low credit score" in risk_factors:

        recommendations.append(
            "Work on improving your credit score by making payments on time "
            "and maintaining responsible credit usage."
        )

        priority_actions.append(
            "Improve your credit score before applying for a major loan."
        )


    elif "Below-average credit score" in risk_factors:

        recommendations.append(
            "Improving your credit score could increase your chances "
            "of receiving better loan terms."
        )


    elif "Excellent credit score" in positive_factors:

        strengths.append(
            "Excellent credit score strengthens your borrowing profile."
        )


    elif "Good credit score" in positive_factors:

        strengths.append(
            "Your good credit score supports a healthy borrowing profile."
        )


    # ========================================================
    # DEBT-TO-INCOME ANALYSIS
    # ========================================================

    if debt_to_income >= 0.50:

        recommendations.append(
            "Your debt-to-income ratio is high. Consider reducing existing "
            "monthly debt obligations before applying for another loan."
        )

        priority_actions.append(
            "Reduce monthly debt obligations."
        )


    elif debt_to_income >= 0.35:

        recommendations.append(
            "Your debt-to-income ratio is moderately high. "
            "Reducing existing debt could improve your financial profile."
        )


    elif debt_to_income < 0.20:

        strengths.append(
            "Low debt burden improves your financial stability."
        )


    # ========================================================
    # LOAN-TO-INCOME ANALYSIS
    # ========================================================

    if loan_to_income >= 0.80:

        recommendations.append(
            "The requested loan amount is high compared to your annual income. "
            "Consider applying for a smaller loan amount."
        )

        priority_actions.append(
            "Consider reducing the requested loan amount."
        )


    elif loan_to_income >= 0.50:

        recommendations.append(
            "The requested loan amount is moderately high compared to your income. "
            "A slightly smaller loan may improve affordability."
        )


    elif loan_to_income < 0.20:

        strengths.append(
            "The requested loan amount appears manageable relative to income."
        )


    # ========================================================
    # SAVINGS ANALYSIS
    # ========================================================

    if savings_to_loan < 0.10:

        recommendations.append(
            "Your savings buffer is low compared to the requested loan amount. "
            "Building emergency savings could improve financial resilience."
        )

        priority_actions.append(
            "Increase your emergency savings buffer."
        )


    elif savings_to_loan < 0.20:

        recommendations.append(
            "Consider increasing savings before taking on a larger loan."
        )


    elif savings_to_loan >= 0.50:

        strengths.append(
            "Strong savings provide a useful financial safety buffer."
        )


    # ========================================================
    # CONVERT POSITIVE FACTORS INTO STRENGTHS
    # ========================================================

    for factor in positive_factors:

        if factor not in strengths:

            strengths.append(factor)


    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    recommendations = list(dict.fromkeys(recommendations))
    strengths = list(dict.fromkeys(strengths))
    priority_actions = list(dict.fromkeys(priority_actions))


    # ========================================================
    # FINAL RESULT
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