import { Insights } from "@/types";

export default function InsightsPanel({ insights }: { insights: Insights }) {
  return (
    <div className="panel">
      <h2>AI Insights</h2>
      <p>{insights.summary}</p>

      <h3>Unusual Transactions</h3>
      {insights.anomalies.length === 0 ? (
        <p>No unusual transactions detected.</p>
      ) : (
        <ul>
          {insights.anomalies.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      )}

      <h3>Recommendations</h3>
      <ul>
        {insights.recommendations.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}