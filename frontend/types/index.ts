export type Transaction = {
    id: number;
    date: string;
    description: string;
    amount: number;
    category: string;
    is_anomaly: boolean;
    notes?: string | null;
  };
  
  export type Summary = {
    total_spend: number;
    total_income: number;
    net: number;
    top_category: string;
    top_category_amount: number;
  };
  
  export type CategoryBreakdown = {
    category: string;
    amount: number;
  };
  
  export type Insights = {
    summary: string;
    anomalies: string[];
    recommendations: string[];
  };