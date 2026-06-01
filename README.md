# FinanceLens

https://finance-lens-kappa.vercel.app

# FinanceLens

FinanceLens is an AI-powered personal finance dashboard that helps users understand spending habits, identify unusual transactions, and generate personalized financial insights from transaction data. Users can upload bank transaction CSV files and instantly receive analytics, visualizations, and AI-generated recommendations.

## Features

* Upload and process transaction CSV files
* Automatic transaction categorization
* Spending and income analysis
* Anomaly detection for unusual transactions
* Interactive dashboards and visualizations
* AI-powered financial insights using Mistral AI
* Download previously uploaded transaction files
* One-click data reset functionality

## Tech Stack

### Frontend

* Next.js
* React
* TypeScript
* Recharts
* CSS Modules

### Backend

* FastAPI
* Python
* SQLAlchemy
* PostgreSQL
* Pandas

### AI & Analytics

* Mistral AI
* Rule-based transaction categorization
* Statistical anomaly detection

## Architecture

1. User uploads a CSV file containing transaction data.
2. FastAPI processes and validates the data.
3. Transactions are stored in PostgreSQL.
4. Transactions are automatically categorized.
5. Analytics and anomaly detection are performed.
6. Mistral AI generates personalized financial insights.
7. Results are displayed through interactive dashboards and charts.

## Key Metrics

* Processes 100,000+ transaction records efficiently
* Real-time financial dashboard updates
* Automated expense categorization
* AI-generated spending recommendations
* Scalable backend architecture with PostgreSQL



## To-Do

* Multi-user authentication
* Budget planning and goal tracking
* Investment portfolio analysis
* Real-time bank integrations
* Advanced ML-based spending predictions

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```