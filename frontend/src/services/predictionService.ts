import { api } from "../lib/api";
import type { CustomerPayload, PredictionResponse } from "../types/churn";

export async function predictCustomer(
  payload: CustomerPayload
): Promise<PredictionResponse> {
  const response = await api.post<PredictionResponse>("/predict", payload);
  return response.data;
}