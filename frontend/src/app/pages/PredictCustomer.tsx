import { useState } from 'react';
import { Sidebar } from '../components/Sidebar';
import { Navbar } from '../components/Navbar';
import { RiskBadge } from '../components/RiskBadge';
import { Gauge } from 'lucide-react';
import { predictCustomer } from '../../services/predictionService';
import type { CustomerPayload, PredictionResponse } from '../../types/churn';

export function PredictCustomer() {
  const [formData, setFormData] = useState({
    gender: '',
    seniorCitizen: '',
    partner: '',
    dependents: '',
    tenure: '',
    phoneService: '',
    multipleLines: '',
    internetService: '',
    onlineSecurity: '',
    onlineBackup: '',
    deviceProtection: '',
    techSupport: '',
    streamingTV: '',
    streamingMovies: '',
    contract: '',
    paperlessBilling: '',
    paymentMethod: '',
    monthlyCharges: '',
    totalCharges: '',
  });

  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const payload: CustomerPayload = {
        gender: formData.gender,
        SeniorCitizen: formData.seniorCitizen === 'Yes' ? 1 : 0,
        Partner: formData.partner,
        Dependents: formData.dependents,
        tenure: Number(formData.tenure),
        PhoneService: formData.phoneService,
        MultipleLines: formData.multipleLines,
        InternetService: formData.internetService,
        OnlineSecurity: formData.onlineSecurity,
        OnlineBackup: formData.onlineBackup,
        DeviceProtection: formData.deviceProtection,
        TechSupport: formData.techSupport,
        StreamingTV: formData.streamingTV,
        StreamingMovies: formData.streamingMovies,
        Contract: formData.contract,
        PaperlessBilling: formData.paperlessBilling,
        PaymentMethod:
          formData.paymentMethod === 'Bank transfer'
            ? 'Bank transfer (automatic)'
            : formData.paymentMethod === 'Credit card'
            ? 'Credit card (automatic)'
            : formData.paymentMethod,
        MonthlyCharges: Number(formData.monthlyCharges),
        TotalCharges: Number(formData.totalCharges),
      };

      const response = await predictCustomer(payload);
      setPrediction(response);
    } catch (err) {
      console.error(err);
      setError('Prediction failed. Check backend connection and CORS settings.');
    } finally {
      setLoading(false);
    }
  };

  const getRiskBadgeLevel = (risk: string): 'Low' | 'Medium' | 'High' => {
    if (risk === 'High Risk') return 'High';
    if (risk === 'Medium Risk') return 'Medium';
    return 'Low';
  };

  const riskPercentage = prediction
    ? Math.round(prediction.churn_probability * 100)
    : 0;

  const riskColor = prediction
    ? prediction.churn_probability >= 0.7
      ? '#EF4444'
      : prediction.churn_probability >= 0.4
      ? '#F59E0B'
      : '#10B981'
    : '#E5E7EB';

  return (
    <div className="flex bg-gray-50 min-h-screen">
      <Sidebar />
      <div className="flex-1">
        <Navbar title="Predict Customer Churn" />

        <div className="p-8 ml-64">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <div className="bg-white rounded-xl border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">
                  Customer Information
                </h3>

                <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-4">
                      Demographics
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Gender
                        </label>
                        <select
                          name="gender"
                          value={formData.gender}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Male">Male</option>
                          <option value="Female">Female</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Senior Citizen
                        </label>
                        <select
                          name="seniorCitizen"
                          value={formData.seniorCitizen}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Partner
                        </label>
                        <select
                          name="partner"
                          value={formData.partner}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Dependents
                        </label>
                        <select
                          name="dependents"
                          value={formData.dependents}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Tenure (months)
                        </label>
                        <input
                          type="number"
                          name="tenure"
                          value={formData.tenure}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        />
                      </div>
                    </div>
                  </div>

                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-4">
                      Services
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Phone Service
                        </label>
                        <select
                          name="phoneService"
                          value={formData.phoneService}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Multiple Lines
                        </label>
                        <select
                          name="multipleLines"
                          value={formData.multipleLines}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                          <option value="No phone service">No phone service</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Internet Service
                        </label>
                        <select
                          name="internetService"
                          value={formData.internetService}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="DSL">DSL</option>
                          <option value="Fiber optic">Fiber optic</option>
                          <option value="No">No</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Online Security
                        </label>
                        <select
                          name="onlineSecurity"
                          value={formData.onlineSecurity}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                          <option value="No internet service">No internet service</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Online Backup
                        </label>
                        <select
                          name="onlineBackup"
                          value={formData.onlineBackup}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                          <option value="No internet service">No internet service</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Device Protection
                        </label>
                        <select
                          name="deviceProtection"
                          value={formData.deviceProtection}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                          <option value="No internet service">No internet service</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Tech Support
                        </label>
                        <select
                          name="techSupport"
                          value={formData.techSupport}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                          <option value="No internet service">No internet service</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Streaming TV
                        </label>
                        <select
                          name="streamingTV"
                          value={formData.streamingTV}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                          <option value="No internet service">No internet service</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Streaming Movies
                        </label>
                        <select
                          name="streamingMovies"
                          value={formData.streamingMovies}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                          <option value="No internet service">No internet service</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-4">
                      Contract & Billing
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Contract
                        </label>
                        <select
                          name="contract"
                          value={formData.contract}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Month-to-month">Month-to-month</option>
                          <option value="One year">One year</option>
                          <option value="Two year">Two year</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Paperless Billing
                        </label>
                        <select
                          name="paperlessBilling"
                          value={formData.paperlessBilling}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Yes">Yes</option>
                          <option value="No">No</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Payment Method
                        </label>
                        <select
                          name="paymentMethod"
                          value={formData.paymentMethod}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        >
                          <option value="">Select</option>
                          <option value="Electronic check">Electronic check</option>
                          <option value="Mailed check">Mailed check</option>
                          <option value="Bank transfer">Bank transfer</option>
                          <option value="Credit card">Credit card</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Monthly Charges ($)
                        </label>
                        <input
                          type="number"
                          step="0.01"
                          name="monthlyCharges"
                          value={formData.monthlyCharges}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Total Charges ($)
                        </label>
                        <input
                          type="number"
                          step="0.01"
                          name="totalCharges"
                          value={formData.totalCharges}
                          onChange={handleChange}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                          required
                        />
                      </div>
                    </div>
                  </div>

                  {error && (
                    <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                      {error}
                    </div>
                  )}

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:bg-blue-400 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Predicting...' : 'Predict Churn'}
                  </button>
                </form>
              </div>
            </div>

            <div className="lg:col-span-1">
              {prediction ? (
                <div className="bg-white rounded-xl border border-gray-200 p-6 sticky top-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">
                    Prediction Result
                  </h3>

                  <div className="flex flex-col items-center mb-6">
                    <div className="relative w-48 h-48 mb-4">
                      <svg
                        className="transform -rotate-90"
                        viewBox="0 0 200 200"
                      >
                        <circle
                          cx="100"
                          cy="100"
                          r="80"
                          fill="none"
                          stroke="#E5E7EB"
                          strokeWidth="20"
                        />
                        <circle
                          cx="100"
                          cy="100"
                          r="80"
                          fill="none"
                          stroke={riskColor}
                          strokeWidth="20"
                          strokeDasharray={`${prediction.churn_probability * 502.4} 502.4`}
                          strokeLinecap="round"
                        />
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <Gauge className="text-gray-400 mb-2" size={24} />
                        <span className="text-3xl font-bold text-gray-900">
                          {riskPercentage}%
                        </span>
                        <span className="text-sm text-gray-500">Churn Risk</span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div className="border-t border-gray-200 pt-4">
                      <p className="text-sm text-gray-600 mb-2">Prediction</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {prediction.churn_prediction === 1 ? 'Will Churn' : 'Will Stay'}
                      </p>
                    </div>

                    <div className="border-t border-gray-200 pt-4">
                      <p className="text-sm text-gray-600 mb-2">Risk Level</p>
                      <RiskBadge level={getRiskBadgeLevel(prediction.risk_level)} />
                    </div>

                    <div className="border-t border-gray-200 pt-4">
                      <p className="text-sm text-gray-600 mb-2">Recommendation</p>
                      <p className="text-sm text-gray-700 leading-relaxed">
                        {prediction.retention_action}
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-white rounded-xl border border-gray-200 p-6 sticky top-8">
                  <div className="text-center py-12">
                    <Gauge className="mx-auto text-gray-300 mb-4" size={48} />
                    <p className="text-gray-500">
                      Fill out the form and click &quot;Predict Churn&quot; to see results
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}