from io import StringIO
import pandas as pd
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from pathlib import Path

from .database import Base, engine, get_db, SessionLocal
from .models import Transaction
from .schemas import TransactionOut, SummaryResponse, InsightResponse
from .ai import categorize_transaction, detect_anomalies, generate_insights
from .seed_data import seed_transactions
latest_uploaded_file = None
app = FastAPI(title="FinanceLens API")

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

latest_uploaded_file = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# with SessionLocal() as db:
#     seed_transactions(db)


@app.get("/")
def read_root():
    return {"message": "FinanceLens API running"}


@app.get("/transactions", response_model=list[TransactionOut])
def get_transactions(db: Session = Depends(get_db)):
    rows = db.query(Transaction).order_by(Transaction.date.desc(), Transaction.id.desc()).all()
    return rows


@app.post("/upload-transactions")
async def upload_transactions(file: UploadFile = File(...), db: Session = Depends(get_db)):
    global latest_uploaded_file

    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    content = await file.read()
    decoded = content.decode("utf-8")

    saved_path = UPLOAD_DIR / file.filename
    with open(saved_path, "wb") as f:
        f.write(content)

    latest_uploaded_file = file.filename

    df = pd.read_csv(StringIO(decoded))

    required_columns = {"date", "description", "amount"}
    lower_cols = {c.lower().strip(): c for c in df.columns}
    if not required_columns.issubset(set(lower_cols.keys())):
        raise HTTPException(status_code=400, detail="CSV must contain date, description, and amount columns.")

    normalized = pd.DataFrame({
        "date": pd.to_datetime(df[lower_cols["date"]]).dt.date,
        "description": df[lower_cols["description"]].astype(str),
        "amount": pd.to_numeric(df[lower_cols["amount"]], errors="coerce").fillna(0),
    })

    normalized["category"] = normalized.apply(
        lambda row: categorize_transaction(row["description"], row["amount"]),
        axis=1,
    )
    normalized = detect_anomalies(normalized)

    inserted = 0
    for _, row in normalized.iterrows():
        tx = Transaction(
            date=row["date"],
            description=row["description"],
            amount=float(row["amount"]),
            category=row["category"],
            is_anomaly=bool(row["is_anomaly"]),
            notes=None,
        )
        db.add(tx)
        inserted += 1

    db.commit()

    return {
        "message": f"Uploaded {inserted} transactions successfully.",
        "filename": file.filename,
        "download_url": f"http://localhost:8000/download/{file.filename}"
    }


@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )


@app.get("/latest-upload")
def latest_upload():
    if latest_uploaded_file is None:
        return {"filename": None, "download_url": None}

    return {
        "filename": latest_uploaded_file,
        "download_url": f"http://localhost:8000/download/{latest_uploaded_file}"
    }


@app.get("/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    txs = db.query(Transaction).all()

    total_spend = sum(t.amount for t in txs if t.amount > 0)
    total_income = sum(-t.amount for t in txs if t.amount < 0)
    net = total_income - total_spend

    category_totals = {}
    for t in txs:
        if t.amount > 0:
            category_totals[t.category] = category_totals.get(t.category, 0) + t.amount

    if category_totals:
        top_category = max(category_totals, key=category_totals.get)
        top_category_amount = category_totals[top_category]
    else:
        top_category = "None"
        top_category_amount = 0.0

    return {
        "total_spend": round(total_spend, 2),
        "total_income": round(total_income, 2),
        "net": round(net, 2),
        "top_category": top_category,
        "top_category_amount": round(top_category_amount, 2),
    }


@app.get("/category-breakdown")
def category_breakdown(db: Session = Depends(get_db)):
    rows = (
        db.query(Transaction.category, func.sum(Transaction.amount))
        .filter(Transaction.amount > 0)
        .group_by(Transaction.category)
        .all()
    )

    return [
        {"category": category, "amount": round(float(amount), 2)}
        for category, amount in rows
    ]


@app.get("/insights", response_model=InsightResponse)
def get_insights(db: Session = Depends(get_db)):
    txs = db.query(Transaction).all()
    df = pd.DataFrame([
        {
            "date": t.date,
            "description": t.description,
            "amount": t.amount,
            "category": t.category,
            "is_anomaly": t.is_anomaly,
        }
        for t in txs
    ])

    insights = generate_insights(df)
    return insights


@app.delete("/clear")
def clear_data(db: Session = Depends(get_db)):
    global latest_uploaded_file

    db.query(Transaction).delete()
    db.commit()

    latest_uploaded_file = None

    for file_path in UPLOAD_DIR.glob("*"):
        if file_path.is_file():
            file_path.unlink()

    return {"message": "Database and uploaded files cleared"}