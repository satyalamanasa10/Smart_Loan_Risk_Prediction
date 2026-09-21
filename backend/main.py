from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import LoanApplication
from src.prediction_pipeline import predict_loan


app = FastAPI(
    title="Smart Loan Eligibility and Default Risk Prediction API",
    description="AI-powered Loan Eligibility and Financial Risk Prediction System",
    version="1.0"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Smart Loan Risk Prediction API is running successfully!"
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Backend is running successfully"
    }


# ---------------------------------------------------------
# LOAN PREDICTION
# ---------------------------------------------------------

@app.post("/predict")
def predict(application: LoanApplication):

    try:

        # Convert Pydantic object into dictionary
        user_data = application.model_dump()

        # Convert frontend field names into
        # the exact names expected by the ML pipeline

        formatted_data = {

            "Age": user_data["age"],

            "EmploymentStatus":
                user_data["employment_status"],

            "EducationLevel":
                user_data["education_level"],

            "Experience":
                user_data["experience"],

            "HomeOwnershipStatus":
                user_data["home_ownership_status"],

            "AnnualIncome":
                user_data["annual_income"],

            "CreditScore":
                user_data["credit_score"],

            "MonthlyDebtPayments":
                user_data["monthly_debt_payments"],

            "SavingsAccountBalance":
                user_data["savings_account_balance"],

            "LoanAmount":
                user_data["loan_amount"],

            "LoanDuration":
                user_data["loan_duration"],

            "LoanPurpose":
                user_data["loan_purpose"]
        }


        # Run complete prediction pipeline
        result = predict_loan(formatted_data)


        # -------------------------------------------------
        # Convert backend result into frontend-friendly
        # response format
        # -------------------------------------------------

        loan_prediction = result.get("loan_prediction", {})
        risk_analysis = result.get("risk_analysis", {})
        recommendations = result.get("recommendations", {})


        return {

            # Loan decision
            "loan_decision":
                loan_prediction.get("decision", "Unknown"),

            "approval_probability":
                loan_prediction.get("approval_probability", 0),

            "rejection_probability":
                loan_prediction.get("rejection_probability", 0),


            # Risk information
            "risk_score":
                risk_analysis.get("risk_score", 0),

            "risk_level":
                risk_analysis.get("risk_level", "Unknown"),


            # Financial ratios
            "financial_ratios": {

                "debt_to_income_ratio":
                    risk_analysis.get(
                        "debt_to_income_ratio", 0
                    ),

                "loan_to_income_ratio":
                    risk_analysis.get(
                        "loan_to_income_ratio", 0
                    ),

                "savings_to_loan_ratio":
                    risk_analysis.get(
                        "savings_to_loan_ratio", 0
                    )
            },


            # Risk factors
            "risk_factors":
                risk_analysis.get(
                    "risk_factors", []
                ),


            # Positive financial factors
            "financial_strengths":
                risk_analysis.get(
                    "positive_factors", []
                ),


            # Recommendations
            "recommendations":
                recommendations.get(
                    "recommendations", []
                ),


            # Priority actions
            "priority_actions":
                recommendations.get(
                    "priority_actions", []
                )
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )