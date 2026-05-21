import { Transaction } from "@/types";

export default function TransactionTable({ transactions }: { transactions: Transaction[] }) {
  return (
    <div className="panel">
      <h2>Transactions</h2>
      <div style={{ overflowX: "auto" }}>
        <table className="table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Description</th>
              <th>Amount</th>
              <th>Category</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((tx) => (
              <tr key={tx.id}>
                <td>{tx.date}</td>
                <td>{tx.description}</td>
                <td>
                    {tx.amount > 0
                        ? `-$${tx.amount.toFixed(2)}`
                        : `+$${Math.abs(tx.amount).toFixed(2)}`}
                    </td>                
                    <td>{tx.category}</td>
                <td>
                  <span className={`badge ${tx.is_anomaly ? "badge-danger" : "badge-normal"}`}>
                    {tx.is_anomaly ? "Anomaly" : "Normal"}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}