import { Sidebar } from '../components/Sidebar';
import { Navbar } from '../components/Navbar';
import { KPICard } from '../components/KPICard';
import { RiskBadge } from '../components/RiskBadge';
import { Users, TrendingDown, AlertTriangle, DollarSign, Filter } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const churnTrendData = [
  { month: 'Jan', churnRate: 15 },
  { month: 'Feb', churnRate: 18 },
  { month: 'Mar', churnRate: 14 },
  { month: 'Apr', churnRate: 16 },
  { month: 'May', churnRate: 19 },
  { month: 'Jun', churnRate: 17 },
];

const riskDistributionData = [
  { name: 'Low Risk', value: 6200, color: '#10B981' },
  { name: 'Medium Risk', value: 2800, color: '#F59E0B' },
  { name: 'High Risk', value: 1200, color: '#EF4444' },
];

const contractTypeData = [
  { type: 'Month-to-Month', churnRate: 42 },
  { type: 'One Year', churnRate: 11 },
  { type: 'Two Year', churnRate: 3 },
];

const recentPredictions = [
  { id: 'C-10234', contract: 'Month-to-Month', charges: 89.99, probability: 87, risk: 'High' as const, action: 'Offer long-term contract discount' },
  { id: 'C-10235', contract: 'One Year', charges: 65.50, probability: 64, risk: 'Medium' as const, action: 'Provide bundle offer' },
  { id: 'C-10236', contract: 'Month-to-Month', charges: 95.00, probability: 91, risk: 'High' as const, action: 'Free tech support trial' },
  { id: 'C-10237', contract: 'Two Year', charges: 45.00, probability: 23, risk: 'Low' as const, action: 'Continue monitoring' },
  { id: 'C-10238', contract: 'Month-to-Month', charges: 110.50, probability: 78, risk: 'High' as const, action: 'Launch engagement campaign' },
  { id: 'C-10239', contract: 'One Year', charges: 55.25, probability: 48, risk: 'Medium' as const, action: 'Loyalty rewards program' },
];

export function Dashboard() {
  return (
    <div className="flex bg-gray-50 min-h-screen">
      <Sidebar />
      <div className="flex-1">
        <Navbar title="Dashboard" />
        
        <div className="p-8 ml-64">
          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <KPICard
              title="Total Customers"
              value="10,234"
              change="+2.5% from last month"
              trend="up"
              icon={Users}
              iconBgColor="bg-blue-100"
              iconColor="text-blue-600"
            />
            <KPICard
              title="Churn Rate"
              value="17.2%"
              change="-1.3% from last month"
              trend="down"
              icon={TrendingDown}
              iconBgColor="bg-green-100"
              iconColor="text-green-600"
            />
            <KPICard
              title="High-Risk Customers"
              value="1,234"
              change="+5.2% from last month"
              trend="up"
              icon={AlertTriangle}
              iconBgColor="bg-red-100"
              iconColor="text-red-600"
            />
            <KPICard
              title="Revenue at Risk"
              value="$892K"
              change="+3.8% from last month"
              trend="up"
              icon={DollarSign}
              iconBgColor="bg-yellow-100"
              iconColor="text-yellow-600"
            />
          </div>

          {/* Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            {/* Churn Trend Chart */}
            <div className="lg:col-span-2 bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Churn Trend</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={churnTrendData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis dataKey="month" stroke="#6B7280" />
                  <YAxis stroke="#6B7280" />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="churnRate" stroke="#3B82F6" strokeWidth={2} name="Churn Rate (%)" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Risk Distribution */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={riskDistributionData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {riskDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Contract Type vs Churn */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <div className="lg:col-span-2 bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Contract Type vs Churn Rate</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={contractTypeData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis dataKey="type" stroke="#6B7280" />
                  <YAxis stroke="#6B7280" />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="churnRate" fill="#3B82F6" name="Churn Rate (%)" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Segment Summary Cards */}
            <div className="space-y-4">
              <div className="bg-white rounded-xl border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Low Risk</span>
                  <RiskBadge level="Low" size="sm" />
                </div>
                <p className="text-2xl font-bold text-gray-900">6,200</p>
                <p className="text-sm text-gray-500 mt-1">60.6% of customers</p>
              </div>

              <div className="bg-white rounded-xl border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Medium Risk</span>
                  <RiskBadge level="Medium" size="sm" />
                </div>
                <p className="text-2xl font-bold text-gray-900">2,800</p>
                <p className="text-sm text-gray-500 mt-1">27.4% of customers</p>
              </div>

              <div className="bg-white rounded-xl border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">High Risk</span>
                  <RiskBadge level="High" size="sm" />
                </div>
                <p className="text-2xl font-bold text-gray-900">1,234</p>
                <p className="text-sm text-gray-500 mt-1">12.1% of customers</p>
              </div>
            </div>
          </div>

          {/* Recent Predictions Table */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900">Recent Customer Predictions</h3>
              <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors">
                <Filter size={16} />
                Filters
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Customer ID</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Contract</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Monthly Charges</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Churn Probability</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Risk Level</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Suggested Action</th>
                  </tr>
                </thead>
                <tbody>
                  {recentPredictions.map((prediction) => (
                    <tr key={prediction.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4 text-sm font-medium text-gray-900">{prediction.id}</td>
                      <td className="py-3 px-4 text-sm text-gray-600">{prediction.contract}</td>
                      <td className="py-3 px-4 text-sm text-gray-900">${prediction.charges}</td>
                      <td className="py-3 px-4 text-sm">
                        <div className="flex items-center gap-2">
                          <div className="flex-1 bg-gray-200 rounded-full h-2 max-w-[80px]">
                            <div
                              className={`h-2 rounded-full ${
                                prediction.probability >= 70 ? 'bg-red-500' : 
                                prediction.probability >= 40 ? 'bg-yellow-500' : 'bg-green-500'
                              }`}
                              style={{ width: `${prediction.probability}%` }}
                            />
                          </div>
                          <span className="font-medium text-gray-900">{prediction.probability}%</span>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <RiskBadge level={prediction.risk} size="sm" />
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">{prediction.action}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
