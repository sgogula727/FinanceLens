"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { CategoryBreakdown } from "../types";

export default function CategoryChart({ data }: { data: CategoryBreakdown[] }) {
  if (!data || data.length === 0) {
    return (
      <div className="panel">
        <h2>Spending by Category</h2>
        <p>No category data available.</p>
      </div>
    );
  }

  return (
    <div className="panel">
      <h2>Spending by Category</h2>
      <BarChart width={700} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="category" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="amount" fill="#38bdf8" />
      </BarChart>
    </div>
  );
}