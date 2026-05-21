import { Summary } from "@/types";

export default function SummaryCards({ summary }: { summary: Summary }) {
  return (
    <div className="grid cards">
      <div className="panel">
        <h3>Total Spend</h3>
        <p>${summary.total_spend.toFixed(2)}</p>
      </div>
      <div className="panel">
        <h3>Total Income</h3>
        <p>${summary.total_income.toFixed(2)}</p>
      </div>
      <div className="panel">
        <h3>Net</h3>
        <p>${summary.net.toFixed(2)}</p>
      </div>
      <div className="panel">
        <h3>Top Category</h3>
        <p>{summary.top_category}</p>
        <small>${summary.top_category_amount.toFixed(2)}</small>
      </div>
    </div>
  );
}