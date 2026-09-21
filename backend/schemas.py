from pydantic import BaseModel


class LoanApplication(BaseModel):

    age: int

    employment_status: str

    education_level: str

    experience: float

    home_ownership_status: str

    annual_income: float

    credit_score: int

    monthly_debt_payments: float

    savings_account_balance: float

    loan_amount: float

    loan_duration: int

    loan_purpose: str