import { Sidebar } from '../components/Sidebar';
import { Navbar } from '../components/Navbar';
import { Download, FileText, TrendingUp, DollarSign } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const churnByPaymentMethod = [
  { method: 'Electronic Check', churnRate: 45, customers: 2340 },
  { method: 'Mailed Check', churnRate: 18, customers: 1580 },
  { method: 'Bank Transfer', churnRate: 16, customers: 1720 },
  { method: 'Credit Card', churnRate: 15, customers: 2290 },
];

const churnByTenure = [
  { tenure: '0-12 months', churnRate: 48, customers: 1850 },
  { tenure: '13-24 months', churnRate: 32, customers: 1420 },
  { tenure: '25-36 months', churnRate: 18, customers: 1290 },
  { tenure: '37-48 months', churnRate: 12, customers: 1180 },
  { tenure: '49+ months', churnRate: 8, customers: 3494 },
];

const churnByService = [
  { name: 'No Internet', value: 1200, color: '#10B981' },
  { name: 'DSL', value: 2100, color: '#F59E0B' },
  { name: 'Fiber Optic', value: 3800, color: '#EF4444' },
];

const revenueImpactData = [
  { month: 'Jan', retained: 420, lost: 180 },
  { month: 'Feb', retained: 435, lost: 165 },
  { month: 'Mar', retained: 450, lost: 150 },
  { month: 'Apr', retained: 468, lost: 132 },
  { month: 'May', retained: 482, lost: 118 },
  { month: 'Jun', retained: 495, lost: 105 },
];

export function Reports() {
  return (
    <div className="flex bg-gray-50 min-h-screen">
      <Sidebar />
      <div className="flex-1">
        <Navbar title="Business Analytics & Reports" />
        
        <div className="p-8 ml-64">
          {/* Executive Summary */}
          <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl p-8 mb-8 text-white">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold mb-2">Executive Summary Report</h2>
                <p className="text-blue-100">Quarter 2, 2026 - Customer Churn Analytics</p>
              </div>
              <div className="flex gap-3">
                <button className="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition-colors">
                  <FileText size={18} />
                  <span>PDF</span>
                </button>
                <button className="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition-colors">
                  <Download size={18} />
                  <span>CSV</span>
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <p className="text-blue-100 text-sm mb-2">Total Revenue</p>
                <p className="text-3xl font-bold">$8.4M</p>
                <p className="text-sm text-green-300 mt-1">↑ 12.5% vs Q1</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <p className="text-blue-100 text-sm mb-2">Churned Revenue</p>
                <p className="text-3xl font-bold">$1.2M</p>
                <p className="text-sm text-red-300 mt-1">↓ 8.3% vs Q1</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <p className="text-blue-100 text-sm mb-2">Retention Rate</p>
                <p className="text-3xl font-bold">82.8%</p>
                <p className="text-sm text-green-300 mt-1">↑ 3.2% vs Q1</p>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <p className="text-blue-100 text-sm mb-2">Interventions</p>
                <p className="text-3xl font-bold">1,247</p>
                <p className="text-sm text-green-300 mt-1">68% success rate</p>
              </div>
            </div>
          </div>

          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Churn by Payment Method */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Churn by Payment Method</h3>
                <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                  Export
                </button>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={churnByPaymentMethod}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis dataKey="method" stroke="#6B7280" tick={{ fontSize: 12 }} />
                  <YAxis stroke="#6B7280" />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="churnRate" fill="#3B82F6" name="Churn Rate (%)" />
                </BarChart>
              </ResponsiveContainer>
              <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                <p className="text-sm text-blue-900">
                  <strong>Key Insight:</strong> Electronic check users show 3x higher churn rate. 
                  Recommend migrating to automatic payment methods.
                </p>
              </div>
            </div>

            {/* Churn by Tenure Group */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Churn by Tenure Group</h3>
                <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                  Export
                </button>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={churnByTenure}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis dataKey="tenure" stroke="#6B7280" tick={{ fontSize: 12 }} />
                  <YAxis stroke="#6B7280" />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="churnRate" fill="#8B5CF6" name="Churn Rate (%)" />
                </BarChart>
              </ResponsiveContainer>
              <div className="mt-4 p-3 bg-purple-50 rounded-lg">
                <p className="text-sm text-purple-900">
                  <strong>Key Insight:</strong> First-year customers are 6x more likely to churn. 
                  Enhanced onboarding programs critical.
                </p>
              </div>
            </div>
          </div>

          {/* Revenue Impact and Service Analysis */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            {/* Revenue Impact Over Time */}
            <div className="lg:col-span-2 bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Revenue Impact Analysis</h3>
                <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                  Export
                </button>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={revenueImpactData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis dataKey="month" stroke="#6B7280" />
                  <YAxis stroke="#6B7280" />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="retained" stroke="#10B981" strokeWidth={2} name="Revenue Retained ($K)" />
                  <Line type="monotone" dataKey="lost" stroke="#EF4444" strokeWidth={2} name="Revenue Lost ($K)" />
                </LineChart>
              </ResponsiveContainer>
              <div className="mt-4 grid grid-cols-2 gap-4">
                <div className="p-3 bg-green-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-1">
                    <TrendingUp size={16} className="text-green-600" />
                    <span className="text-sm font-semibold text-green-900">Retained Revenue</span>
                  </div>
                  <p className="text-2xl font-bold text-green-600">$2.75M</p>
                  <p className="text-xs text-green-700 mt-1">Through retention campaigns</p>
                </div>
                <div className="p-3 bg-red-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-1">
                    <DollarSign size={16} className="text-red-600" />
                    <span className="text-sm font-semibold text-red-900">Lost Revenue</span>
                  </div>
                  <p className="text-2xl font-bold text-red-600">$850K</p>
                  <p className="text-xs text-red-700 mt-1">From churned customers</p>
                </div>
              </div>
            </div>

            {/* Churn by Service Type */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Churn by Service Type</h3>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={churnByService}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}\n${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {churnByService.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div className="mt-4 space-y-2">
                {churnByService.map((service, index) => (
                  <div key={index} className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: service.color }} />
                      <span className="text-gray-700">{service.name}</span>
                    </div>
                    <span className="font-semibold text-gray-900">{service.value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Summary Statistics Table */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900">Key Performance Indicators Summary</h3>
              <div className="flex gap-2">
                <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors">
                  <FileText size={16} />
                  Export PDF
                </button>
                <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors">
                  <Download size={16} />
                  Download CSV
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="border border-gray-200 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-3">Customer Metrics</p>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">Total Customers:</span>
                    <span className="font-semibold text-gray-900">10,234</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">New Customers:</span>
                    <span className="font-semibold text-green-600">+342</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">Churned Customers:</span>
                    <span className="font-semibold text-red-600">-187</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">Net Growth:</span>
                    <span className="font-semibold text-blue-600">+155</span>
                  </div>
                </div>
              </div>

              <div className="border border-gray-200 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-3">Churn Analysis</p>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">Overall Churn Rate:</span>
                    <span className="font-semibold text-gray-900">17.2%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">High Risk Customers:</span>
                    <span className="font-semibold text-red-600">1,234</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">Medium Risk:</span>
                    <span className="font-semibold text-yellow-600">2,800</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">Low Risk:</span>
                    <span className="font-semibold text-green-600">6,200</span>
                  </div>
                </div>
              </div>

              <div className="border border-gray-200 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-3">Financial Impact</p>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">Total Revenue:</span>
                    <span className="font-semibold text-gray-900">$8.4M</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">Revenue at Risk:</span>
                    <span className="font-semibold text-red-600">$892K</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">Retained Revenue:</span>
                    <span className="font-semibold text-green-600">$2.75M</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-700">ROI on Campaigns:</span>
                    <span className="font-semibold text-blue-600">340%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
