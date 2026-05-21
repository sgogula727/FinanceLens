"use client";

import { useEffect, useState } from "react";
import UploadForm from "../components/UploadForm";
import SummaryCards from "../components/SummaryCards";
import CategoryChart from "../components/CategoryChart";
import TransactionTable from "../components/TransactionTable";
import InsightsPanel from "../components/InsightsPanel";
import {
  getTransactions,
  getSummary,
  getCategoryBreakdown,
  getInsights,
} from "../lib/api";
import {
  Transaction,
  Summary,
  CategoryBreakdown,
  Insights,
} from "../types";

export default function HomePage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [categories, setCategories] = useState<CategoryBreakdown[]>([]);
  const [insights, setInsights] = useState<Insights | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [uploadFormKey, setUploadFormKey] = useState(0);

  const loadData = async () => {
    setLoading(true);
    setError("");

    try {
      const [txData, summaryData, categoryData, insightData] = await Promise.all([
        getTransactions(),
        getSummary(),
        getCategoryBreakdown(),
        getInsights(),
      ]);

      setTransactions(txData || []);
      setSummary(summaryData || null);
      setCategories(categoryData || []);
      setInsights(insightData || null);
    } catch (err) {
      console.error("Dashboard load failed:", err);
      setError("Failed to load dashboard data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleReset = async () => {
    await fetch("http://localhost:8000/clear", { method: "DELETE" });
    setUploadFormKey((prev) => prev + 1);
    await loadData();
  };

  return (
    <main className="container">
      <h1>Finance Lens</h1>
      <p>AI-powered personal finance dashboard with transaction categorization and anomaly detection.</p>

      <UploadForm key={uploadFormKey} onUpload={loadData} />

      <div style={{ marginTop: 16 }}>
        <button onClick={handleReset}>Reset Data</button>
      </div>

      {loading && <p>Loading dashboard...</p>}
      {error && <p>{error}</p>}

      {!loading && !error && summary && (
        <>
          <div style={{ marginTop: 20 }}>
            <SummaryCards summary={summary} />
          </div>

          <div className="two-col" style={{ marginTop: 20 }}>
            <CategoryChart data={categories} />
            {insights ? (
              <InsightsPanel insights={insights} />
            ) : (
              <div className="panel">
                <h2>AI Insights</h2>
                <p>No insights available yet.</p>
              </div>
            )}
          </div>

          <div style={{ marginTop: 20 }}>
            <TransactionTable transactions={transactions} />
          </div>
        </>
      )}
    </main>
  );
}