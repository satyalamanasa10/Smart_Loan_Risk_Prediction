# ============================================================
# FEATURE ENGINEERING MODULE
# SMART LOAN ELIGIBILITY & DEFAULT RISK PREDICTION SYSTEM
# ============================================================

import pandas as pd


# ============================================================
# FINAL USER INPUT FEATURES
# ============================================================

USER_INPUT_FEATURES = [

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


# ============================================================
# ENGINEERED FEATURES
# ============================================================

ENGINEERED_FEATURES = [

    "MonthlyIncome_Calculated",
    "DebtToIncome_Calculated",
    "LoanToIncomeRatio",
    "SavingsToLoanRatio",
    "ExperienceToAgeRatio"
]


# ============================================================
# FEATURE ENGINEERING FUNCTION
# ============================================================

def create_engineered_features(df):
    """
    Creates additional financial features from user input data.

    Parameters:
    -----------
    df : pandas DataFrame
        DataFrame containing the required user input features.

    Returns:
    --------
    pandas DataFrame
        DataFrame containing original and engineered features.
    """

    # Create a copy to avoid modifying original data
    data = df.copy()


    # --------------------------------------------------------
    # 1. MONTHLY INCOME
    # --------------------------------------------------------

    data["MonthlyIncome_Calculated"] = (

        data["AnnualIncome"] / 12

    )


    # --------------------------------------------------------
    # 2. DEBT TO INCOME RATIO
    # --------------------------------------------------------

    data["DebtToIncome_Calculated"] = (

        data["MonthlyDebtPayments"]

        /

        (data["MonthlyIncome_Calculated"] + 1)

    )


    # --------------------------------------------------------
    # 3. LOAN TO INCOME RATIO
    # --------------------------------------------------------

    data["LoanToIncomeRatio"] = (

        data["LoanAmount"]

        /

        (data["AnnualIncome"] + 1)

    )


    # --------------------------------------------------------
    # 4. SAVINGS TO LOAN RATIO
    # --------------------------------------------------------

    data["SavingsToLoanRatio"] = (

        data["SavingsAccountBalance"]

        /

        (data["LoanAmount"] + 1)

    )


    # --------------------------------------------------------
    # 5. EXPERIENCE TO AGE RATIO
    # --------------------------------------------------------

    data["ExperienceToAgeRatio"] = (

        data["Experience"]

        /

        (data["Age"] + 1)

    )


    return data


# ============================================================
# GET FINAL FEATURE LIST
# ============================================================

def get_final_features():
    """
    Returns the complete list of features used by the model.
    """

    final_features = (

        USER_INPUT_FEATURES

        +

        ENGINEERED_FEATURES

    )


    return final_features


# ============================================================
# VALIDATE INPUT FEATURES
# ============================================================

def validate_input_features(df):
    """
    Checks whether all required user input features
    are present in the DataFrame.
    """

    missing_features = [

        feature

        for feature in USER_INPUT_FEATURES

        if feature not in df.columns

    ]


    if missing_features:

        raise ValueError(

            f"Missing required features: {missing_features}"

        )


    return True