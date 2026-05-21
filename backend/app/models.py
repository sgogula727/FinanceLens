from sqlalchemy import Column, Integer, String, Float, Date, Boolean, Text
from .database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False, default="Uncategorized")
    is_anomaly = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)