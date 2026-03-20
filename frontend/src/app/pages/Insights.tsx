import { Sidebar } from '../components/Sidebar';
import { Navbar } from '../components/Navbar';
import { TrendingUp, TrendingDown, AlertCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const featureImportanceData = [
  { feature: 'Contract Type', importance: 92 },
  { feature: 'Monthly Charges', importance: 78 },
  { feature: 'Tenure', importance: 65 },
  { feature: 'Internet Service', importance: 54 },
  { feature: 'Tech Support', importance: 42 },
  { feature: 'Payment Method', importance: 38 },
  { feature: 'Online Security', importance: 31 },
  { feature: 'Total Charges', importance: 28 },
];

const churnDrivers = [
  {
    factor: 'Month-to-Month Contract',
    impact: 'High',
    direction: 'increase' as const,
    description: 'Month-to-month contracts show 42% churn rate vs 11% for yearly contracts',
  },
  {
    factor: 'High Monthly Charges',
    impact: 'High',
    direction: 'increase' as const,
    description: 'Customers paying >$80/month are 3.2x more likely to churn',
  },
  {
    factor: 'Low Tenure',
    impact: 'Medium',
    direction: 'increase' as const,
    description: 'Customers with <12 months tenure have 65% higher churn risk',
  },
  {
    factor: 'No Tech Support',
    impact: 'Medium',
    direction: 'increase' as const,
    description: 'Lack of tech support increases churn probability by 28%',
  },
  {
    factor: 'Electronic Check Payment',
    impact: 'Low',
    direction: 'increase' as const,
    description: 'Electronic check users churn 15% more than credit card users',
  },
];

export function Insights() {
  return (
    <div className="flex bg-gray-50 min-h-screen">
      <Sidebar />
      <div className="flex-1">
        <Navbar title="Customer Insights & Explainability" />
        
        <div className="p-8 ml-64">
          {/* Customer Profile Summary */}
          <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Sample Customer Profile Analysis</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div>
                <p className="text-sm text-gray-600 mb-1">Customer ID</p>
                <p className="text-lg font-semibold text-gray-900">C-10234</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Contract Type</p>
                <p className="text-lg font-semibold text-gray-900">Month-to-Month</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Monthly Charges</p>
                <p className="text-lg font-semibold text-gray-900">$89.99</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Tenure</p>
                <p className="text-lg font-semibold text-gray-900">8 months</p>
              </div>
            </div>

            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
              <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
              <div>
                <p className="font-semibold text-red-900 mb-1">High Churn Risk Detected (87%)</p>
                <p className="text-sm text-red-700">This customer exhibits multiple high-risk factors. Immediate retention intervention recommended.</p>
              </div>
            </div>
          </div>

          {/* Top Churn Drivers */}
          <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Top Churn Drivers for This Customer</h3>
            
            <div className="space-y-4">
              {churnDrivers.map((driver, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-3">
                      {driver.direction === 'increase' ? (
                        <TrendingUp className="text-red-500" size={20} />
                      ) : (
                        <TrendingDown className="text-green-500" size={20} />
                      )}
                      <h4 className="font-semibold text-gray-900">{driver.factor}</h4>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      driver.impact === 'High' ? 'bg-red-100 text-red-700' :
                      driver.impact === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-blue-100 text-blue-700'
                    }`}>
                      {driver.impact} Impact
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 ml-8">{driver.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Feature Importance Chart */}
          <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Feature Importance Analysis</h3>
            <p className="text-sm text-gray-600 mb-6">
              Relative importance of features in predicting customer churn
            </p>
            
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={featureImportanceData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis type="number" stroke="#6B7280" />
                <YAxis dataKey="feature" type="category" stroke="#6B7280" width={150} />
                <Tooltip />
                <Legend />
                <Bar dataKey="importance" fill="#3B82F6" name="Importance Score" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* SHAP-Style Explanation */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Model Explanation (SHAP Values)</h3>
            <p className="text-sm text-gray-600 mb-6">
              How each feature contributes to the churn prediction for this specific customer
            </p>

            <div className="space-y-3">
              <div className="flex items-center gap-4">
                <div className="w-48 text-sm text-gray-700">Month-to-Month Contract</div>
                <div className="flex-1 flex items-center gap-2">
                  <div className="flex-1 bg-gray-100 rounded-full h-8">
                    <div className="bg-red-500 h-8 rounded-full flex items-center justify-end px-3" style={{ width: '85%' }}>
                      <span className="text-xs font-semibold text-white">+0.42</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-48 text-sm text-gray-700">High Monthly Charges</div>
                <div className="flex-1 flex items-center gap-2">
                  <div className="flex-1 bg-gray-100 rounded-full h-8">
                    <div className="bg-red-400 h-8 rounded-full flex items-center justify-end px-3" style={{ width: '65%' }}>
                      <span className="text-xs font-semibold text-white">+0.28</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-48 text-sm text-gray-700">Low Tenure (8 months)</div>
                <div className="flex-1 flex items-center gap-2">
                  <div className="flex-1 bg-gray-100 rounded-full h-8">
                    <div className="bg-orange-500 h-8 rounded-full flex items-center justify-end px-3" style={{ width: '55%' }}>
                      <span className="text-xs font-semibold text-white">+0.21</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-48 text-sm text-gray-700">No Tech Support</div>
                <div className="flex-1 flex items-center gap-2">
                  <div className="flex-1 bg-gray-100 rounded-full h-8">
                    <div className="bg-orange-400 h-8 rounded-full flex items-center justify-end px-3" style={{ width: '40%' }}>
                      <span className="text-xs font-semibold text-white">+0.14</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-48 text-sm text-gray-700">Fiber Optic Internet</div>
                <div className="flex-1 flex items-center gap-2">
                  <div className="flex-1 bg-gray-100 rounded-full h-8">
                    <div className="bg-yellow-500 h-8 rounded-full flex items-center justify-end px-3" style={{ width: '30%' }}>
                      <span className="text-xs font-semibold text-white">+0.09</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="w-48 text-sm text-gray-700">Has Phone Service</div>
                <div className="flex-1 flex items-center gap-2">
                  <div className="flex-1 bg-gray-100 rounded-full h-8 flex items-center">
                    <div className="bg-green-500 h-8 rounded-full flex items-center px-3" style={{ width: '15%' }}>
                      <span className="text-xs font-semibold text-white">-0.05</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-900">
                <strong>Interpretation:</strong> Red bars indicate features pushing toward churn, green bars indicate features reducing churn risk. 
                The model's final prediction of 87% churn probability is the sum of these individual contributions plus the base rate.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
