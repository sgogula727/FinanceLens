from datetime import date
from sqlalchemy.orm import Session
from .models import Transaction
from .ai import categorize_transaction


SAMPLE_TRANSACTIONS = [
    {"date": date(2026, 3, 1), "description": "Kroger Store #202", "amount": 84.23},
    {"date": date(2026, 3, 2), "description": "Starbucks 4832", "amount": 7.12},
    {"date": date(2026, 3, 3), "description": "Spotify USA", "amount": 10.99},
    {"date": date(2026, 3, 3), "description": "Direct Dep Payroll", "amount": -1800.00},
    {"date": date(2026, 3, 4), "description": "Uber Trip", "amount": 22.41},
    {"date": date(2026, 3, 5), "description": "Amazon Purchase", "amount": 119.88},
    {"date": date(2026, 3, 6), "description": "Shell Oil", "amount": 42.67},
    {"date": date(2026, 3, 8), "description": "Apartment Rent", "amount": 1450.00},
    {"date": date(2026, 3, 9), "description": "Chipotle", "amount": 14.52},
    {"date": date(2026, 3, 10), "description": "Best Buy", "amount": 349.99},
]

def seed_transactions(db: Session):
    existing = db.query(Transaction).count()
    if existing > 0:
        return

    for item in SAMPLE_TRANSACTIONS:
        category = categorize_transaction(item["description"], item["amount"])
        row = Transaction(
            date=item["date"],
            description=item["description"],
            amount=item["amount"],
            category=category,
            is_anomaly=False,
            notes=None,
        )
        db.add(row)

    db.commit()