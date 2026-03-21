import { api } from '../lib/api';
import type {
  MetricsResponse,
  RiskDistributionResponse,
  ContractChurnItem,
  PaymentMethodChurnItem,
  RecentPredictionItem,
} from '../types/dashboard';

export async function getMetrics(): Promise<MetricsResponse> {
  const response = await api.get<MetricsResponse>('/metrics');
  return response.data;
}

export async function getRiskDistribution(): Promise<RiskDistributionResponse> {
  const response = await api.get<RiskDistributionResponse>('/risk-distribution');
  return response.data;
}

export async function getContractChurn(): Promise<ContractChurnItem[]> {
  const response = await api.get<ContractChurnItem[]>('/contract-churn');
  return response.data;
}

export async function getPaymentMethodChurn(): Promise<PaymentMethodChurnItem[]> {
  const response = await api.get<PaymentMethodChurnItem[]>('/payment-method-churn');
  return response.data;
}

export async function getRecentPredictions(): Promise<RecentPredictionItem[]> {
  const response = await api.get<RecentPredictionItem[]>('/recent-predictions');
  return response.data;
}