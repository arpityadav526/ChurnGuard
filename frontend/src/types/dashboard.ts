export type MetricsResponse = {
  total_customers: number;
  churn_rate: number;
  high_risk_customers: number;
  predicted_revenue_at_risk: number;
  total_predictions_made: number;
};

export type RiskDistributionResponse = {
  labels: string[];
  values: number[];
};

export type ContractChurnItem = {
  Contract: string;
  churn_rate: number;
};

export type PaymentMethodChurnItem = {
  PaymentMethod: string;
  churn_rate: number;
};

export type RecentPredictionItem = {
  timestamp: string;
  Contract: string;
  MonthlyCharges: number;
  churn_probability: number;
  churn_prediction: number;
  risk_level: string;
  retention_action: string;
};