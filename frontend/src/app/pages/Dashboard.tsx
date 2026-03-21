import { useEffect, useState } from 'react';
import { Sidebar } from '../components/Sidebar';
import { Navbar } from '../components/Navbar';
import { KPICard } from '../components/KPICard';
import { RiskBadge } from '../components/RiskBadge';
import { Users, TrendingDown, AlertTriangle, DollarSign, Filter } from 'lucide-react';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

import {
  getMetrics,
  getRiskDistribution,
  getContractChurn,
  getRecentPredictions,
} from '../../services/dashboardService';

export function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null);
  const [riskData, setRiskData] = useState<any>(null);
  const [contractData, setContractData] = useState<any[]>([]);
  const [recentData, setRecentData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [m, r, c, recent] = await Promise.all([
          getMetrics(),
          getRiskDistribution(),
          getContractChurn(),
          getRecentPredictions(),
        ]);

        setMetrics(m);
        setRiskData(r);
        setContractData(c);
        setRecentData(recent);
      } catch (err) {
        console.error('Dashboard error:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  const riskChartData =
    riskData
      ? riskData.labels.map((label: string, i: number) => ({
          name: label,
          value: riskData.values[i],
          color:
            label === 'High Risk'
              ? '#EF4444'
              : label === 'Medium Risk'
              ? '#F59E0B'
              : '#10B981',
        }))
      : [];

  const contractChartData = contractData.map((item) => ({
    type: item.Contract,
    churnRate: item.churn_rate,
  }));

  if (loading) {
    return <div className="p-8">Loading dashboard...</div>;
  }

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
              value={metrics?.total_customers || 0}
              change="Live data"
              trend="up"
              icon={Users}
              iconBgColor="bg-blue-100"
              iconColor="text-blue-600"
            />
            <KPICard
              title="Churn Rate"
              value={`${metrics?.churn_rate || 0}%`}
              change="Live data"
              trend="down"
              icon={TrendingDown}
              iconBgColor="bg-green-100"
              iconColor="text-green-600"
            />
            <KPICard
              title="High-Risk Customers"
              value={metrics?.high_risk_customers || 0}
              change="Live data"
              trend="up"
              icon={AlertTriangle}
              iconBgColor="bg-red-100"
              iconColor="text-red-600"
            />
            <KPICard
              title="Revenue at Risk"
              value={`$${metrics?.predicted_revenue_at_risk || 0}`}
              change="Live data"
              trend="up"
              icon={DollarSign}
              iconBgColor="bg-yellow-100"
              iconColor="text-yellow-600"
            />
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            {/* Churn Trend (static for now) */}
            <div className="lg:col-span-2 bg-white rounded-xl border p-6">
              <h3 className="text-lg font-semibold mb-4">Churn Trend</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={[
                  { month: 'Jan', churnRate: 15 },
                  { month: 'Feb', churnRate: 18 },
                  { month: 'Mar', churnRate: 14 },
                  { month: 'Apr', churnRate: 16 },
                  { month: 'May', churnRate: 19 },
                  { month: 'Jun', churnRate: 17 },
                ]}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line dataKey="churnRate" stroke="#3B82F6" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Risk Distribution */}
            <div className="bg-white rounded-xl border p-6">
              <h3 className="text-lg font-semibold mb-4">Risk Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie data={riskChartData} dataKey="value" nameKey="name" outerRadius={80}>
                    {riskChartData.map((entry: any, index: number) => (
                      <Cell key={index} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Contract Chart */}
          <div className="bg-white rounded-xl border p-6 mb-8">
            <h3 className="text-lg font-semibold mb-4">Contract vs Churn</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={contractChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="type" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="churnRate" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Recent Predictions */}
          <div className="bg-white rounded-xl border p-6">
            <div className="flex justify-between mb-4">
              <h3 className="text-lg font-semibold">Recent Predictions</h3>
              <button className="flex items-center gap-2 px-3 py-1 border rounded">
                <Filter size={16} />
                Filters
              </button>
            </div>

            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="py-3">Timestamp</th>
                  <th>Contract</th>
                  <th>Charges</th>
                  <th>Probability</th>
                  <th>Risk</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {recentData.map((item, i) => (
                  <tr key={i} className="border-b">
                    <td className="py-3">{item.timestamp}</td>
                    <td>{item.Contract}</td>
                    <td>${item.MonthlyCharges}</td>
                    <td>{Math.round(item.churn_probability * 100)}%</td>
                    <td>
                      <RiskBadge
                        level={
                          item.risk_level === 'High Risk'
                            ? 'High'
                            : item.risk_level === 'Medium Risk'
                            ? 'Medium'
                            : 'Low'
                        }
                      />
                    </td>
                    <td>{item.retention_action}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

        </div>
      </div>
    </div>
  );
}