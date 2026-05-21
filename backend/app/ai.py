from __future__ import annotations
import math
import pandas as pd
from collections import defaultdict
import os
import json
from mistralai.client import Mistral

CATEGORY_KEYWORDS = {
    "Groceries": ["kroger", "walmart", "aldi", "trader joe", "whole foods", "costco", "target grocery"],
    "Dining": ["starbucks", "mcdonald", "chipotle", "doordash", "uber eats", "restaurant", "cafe", "dunkin"],
    "Transport": ["uber", "lyft", "shell", "exxon", "bp", "gas", "parking", "metro"],
    "Rent": ["rent", "apartment", "lease", "property management"],
    "Utilities": ["electric", "water", "internet", "comcast", "verizon", "at&t", "utility"],
    "Subscriptions": ["spotify", "netflix", "hulu", "amazon prime", "apple.com/bill", "youtube", "adobe"],
    "Shopping": ["amazon", "etsy", "best buy", "nike", "zara", "apple store"],
    "Healthcare": ["cvs", "walgreens", "hospital", "clinic", "pharmacy", "dental"],
    "Travel": ["airbnb", "delta", "united", "marriott", "hilton", "hotel", "flight"],
    "Income": ["payroll", "salary", "deposit", "direct dep", "refund"],
}


def clean_description(text: str) -> str:
    return " ".join(text.lower().strip().split())

def categorize_transaction(description: str, amount: float) -> str:
    desc = clean_description(description)

    if amount < 0:
        # negative amount as income in some exports
        return "Income"

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in desc:
                return category

    if amount > 2000:
        return "Rent"
    if 50 <= amount <= 250 and any(word in desc for word in ["market", "foods", "store"]):
        return "Groceries"

    return "Other"

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        df["is_anomaly"] = False
        return df

    df = df.copy()
    df["is_anomaly"] = False

    category_stats = defaultdict(dict)
    for category, group in df.groupby("category"):
        amounts = group["amount"].abs()
        mean = amounts.mean()
        std = amounts.std()
        if math.isnan(std):
            std = 0
        category_stats[category] = {"mean": mean, "std": std}

    anomaly_flags = []
    seen_merchants = set()
    for _, row in df.iterrows():
        amount = abs(row["amount"])
        category = row["category"]
        desc = clean_description(row["description"])
        stats = category_stats[category]
        mean = stats["mean"]
        std = stats["std"]

        is_large_spike = std > 0 and amount > mean + 2 * std
        is_new_merchant_high = desc not in seen_merchants and amount > max(100, mean * 1.5)

        anomaly = bool(is_large_spike or is_new_merchant_high)
        anomaly_flags.append(anomaly)
        seen_merchants.add(desc)

    df["is_anomaly"] = anomaly_flags
    return df

def generate_insights(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "summary": "No transactions available yet.",
            "anomalies": [],
            "recommendations": [],
        }

    spend_df = df[df["amount"] > 0].copy()
    income_df = df[df["amount"] < 0].copy()

    total_spend = float(spend_df["amount"].sum()) if not spend_df.empty else 0.0
    total_income = float((-income_df["amount"]).sum()) if not income_df.empty else 0.0

    by_category = spend_df.groupby("category")["amount"].sum().sort_values(ascending=False)
    top_category = by_category.index[0] if not by_category.empty else "None"
    top_amount = float(by_category.iloc[0]) if not by_category.empty else 0.0

    anomaly_rows = spend_df[spend_df["is_anomaly"]].sort_values("amount", ascending=False)
    anomaly_messages = [
        f"{row['description']} for ${row['amount']:.2f} on {row['date']}"
        for _, row in anomaly_rows.head(5).iterrows()
    ]

    recommendations = []
    if "Dining" in by_category and by_category["Dining"] > 200:
        recommendations.append("Dining spending is high. Consider setting a weekly eating-out cap.")
    if "Subscriptions" in by_category and by_category["Subscriptions"] > 50:
        recommendations.append("Review recurring subscriptions and cancel any low-value services.")
    if top_category == "Shopping":
        recommendations.append("Shopping is your top spending category. Consider delaying non-essential purchases.")
    if total_spend > total_income and total_income > 0:
        recommendations.append("You spent more than your income in this period. Reduce variable spending categories first.")
    if not recommendations:
        recommendations.append("Your spending looks fairly balanced. Keep monitoring your largest category each month.")

    summary = (
        f"You spent ${total_spend:.2f} and recorded ${total_income:.2f} in income. "
        f"Your largest spending category was {top_category} at ${top_amount:.2f}."
    )

    return {
        "summary": summary,
        "anomalies": anomaly_messages,
        "recommendations": recommendations,
    }

def generate_mistral_insights(df: pd.DataFrame) -> dict:
    if df.empty:
        return generate_insights(df)

    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        return generate_insights(df)

    client = Mistral(api_key=api_key)

    sample_transactions = df.head(50).to_dict(orient="records")

    prompt = f"""
You are an AI financial assistant.

Analyze these transactions and return ONLY valid JSON with this exact structure:

{{
  "summary": "one concise financial overview",
  "anomalies": ["unusual transaction observations"],
  "recommendations": ["practical financial recommendations"]
}}

Transactions:
{sample_transactions}
"""

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print("Mistral insight generation failed:", e)
        return generate_insights(df)