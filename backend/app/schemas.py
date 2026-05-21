from datetime import date
from pydantic import BaseModel


class TransactionBase(BaseModel):
    date: date
    description: str
    amount: float
    category: str
    is_anomaly: bool = False
    notes: str | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionOut(TransactionBase):
    id: int

    class Config:
        from_attributes = True


class SummaryResponse(BaseModel):
    total_spend: float
    total_income: float
    net: float
    top_category: str
    top_category_amount: float


class InsightResponse(BaseModel):
    summary: str
    anomalies: list[str]
    recommendations: list[str]