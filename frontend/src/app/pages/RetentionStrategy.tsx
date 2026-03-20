import { Sidebar } from '../components/Sidebar';
import { Navbar } from '../components/Navbar';
import { RiskBadge } from '../components/RiskBadge';
import { Target, Users, DollarSign, TrendingUp } from 'lucide-react';

const highRiskCustomers = [
  { id: 'C-10234', name: 'John Smith', contract: 'Month-to-Month', charges: 89.99, probability: 87, priority: 'High' as const, action: 'Offer long-term contract discount' },
  { id: 'C-10236', name: 'Sarah Johnson', contract: 'Month-to-Month', charges: 95.00, probability: 91, priority: 'High' as const, action: 'Free tech support trial' },
  { id: 'C-10238', name: 'Mike Davis', contract: 'Month-to-Month', charges: 110.50, probability: 78, priority: 'High' as const, action: 'Launch engagement campaign' },
  { id: 'C-10235', name: 'Emily Brown', contract: 'One Year', charges: 65.50, probability: 64, priority: 'Medium' as const, action: 'Provide bundle offer' },
  { id: 'C-10239', name: 'David Wilson', contract: 'One Year', charges: 55.25, probability: 48, priority: 'Medium' as const, action: 'Loyalty rewards program' },
  { id: 'C-10240', name: 'Lisa Anderson', contract: 'Month-to-Month', charges: 72.00, probability: 71, priority: 'High' as const, action: 'Premium package upgrade' },
];

const retentionActions = [
  {
    title: 'Long-Term Contract Discount',
    description: 'Offer 20% discount for customers switching from month-to-month to annual contracts',
    targetSegment: 'Month-to-month, high charges',
    expectedImpact: '35% reduction in churn',
    customers: 342,
    potentialSavings: '$287K',
  },
  {
    title: 'Bundle Upgrade Offer',
    description: 'Provide premium service bundle at discounted rate with additional features',
    targetSegment: 'Medium risk, existing customers',
    expectedImpact: '28% reduction in churn',
    customers: 218,
    potentialSavings: '$165K',
  },
  {
    title: 'Free Tech Support Trial',
    description: '3-month complimentary tech support for customers without current support plan',
    targetSegment: 'High charges, no tech support',
    expectedImpact: '22% reduction in churn',
    customers: 156,
    potentialSavings: '$124K',
  },
  {
    title: 'Onboarding Engagement Campaign',
    description: 'Personalized onboarding program for new customers in first 6 months',
    targetSegment: 'Low tenure customers',
    expectedImpact: '31% reduction in churn',
    customers: 289,
    potentialSavings: '$198K',
  },
];

export function RetentionStrategy() {
  return (
    <div className="flex bg-gray-50 min-h-screen">
      <Sidebar />
      <div className="flex-1">
        <Navbar title="Retention Strategy" />
        
        <div className="p-8 ml-64">
          {/* Campaign Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center gap-3 mb-2">
                <div className="bg-blue-100 text-blue-600 p-2 rounded-lg">
                  <Target size={20} />
                </div>
                <p className="text-sm text-gray-600">Active Campaigns</p>
              </div>
              <p className="text-3xl font-bold text-gray-900">4</p>
            </div>

            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center gap-3 mb-2">
                <div className="bg-purple-100 text-purple-600 p-2 rounded-lg">
                  <Users size={20} />
                </div>
                <p className="text-sm text-gray-600">Customers Targeted</p>
              </div>
              <p className="text-3xl font-bold text-gray-900">1,005</p>
            </div>

            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center gap-3 mb-2">
                <div className="bg-green-100 text-green-600 p-2 rounded-lg">
                  <TrendingUp size={20} />
                </div>
                <p className="text-sm text-gray-600">Expected Saves</p>
              </div>
              <p className="text-3xl font-bold text-gray-900">312</p>
            </div>

            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-center gap-3 mb-2">
                <div className="bg-yellow-100 text-yellow-600 p-2 rounded-lg">
                  <DollarSign size={20} />
                </div>
                <p className="text-sm text-gray-600">Revenue Retained</p>
              </div>
              <p className="text-3xl font-bold text-gray-900">$774K</p>
            </div>
          </div>

          {/* Retention Action Cards */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommended Retention Actions</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {retentionActions.map((action, index) => (
                <div key={index} className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between mb-4">
                    <h4 className="text-lg font-semibold text-gray-900">{action.title}</h4>
                    <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-semibold">
                      Active
                    </span>
                  </div>
                  
                  <p className="text-sm text-gray-600 mb-4">{action.description}</p>
                  
                  <div className="space-y-2 mb-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Target Segment:</span>
                      <span className="font-medium text-gray-900">{action.targetSegment}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Expected Impact:</span>
                      <span className="font-semibold text-green-600">{action.expectedImpact}</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Customers</p>
                      <p className="text-xl font-bold text-gray-900">{action.customers}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Potential Savings</p>
                      <p className="text-xl font-bold text-green-600">{action.potentialSavings}</p>
                    </div>
                  </div>

                  <button className="w-full mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors">
                    View Campaign Details
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* High-Priority Customers Table */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">High-Priority Intervention Customers</h3>
                <p className="text-sm text-gray-600 mt-1">Customers requiring immediate retention action</p>
              </div>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors">
                Export List
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Customer ID</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Name</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Contract</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Monthly Charges</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Churn Risk</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Priority</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Suggested Action</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {highRiskCustomers.map((customer) => (
                    <tr key={customer.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4 text-sm font-medium text-gray-900">{customer.id}</td>
                      <td className="py-3 px-4 text-sm text-gray-900">{customer.name}</td>
                      <td className="py-3 px-4 text-sm text-gray-600">{customer.contract}</td>
                      <td className="py-3 px-4 text-sm text-gray-900">${customer.charges}</td>
                      <td className="py-3 px-4 text-sm">
                        <div className="flex items-center gap-2">
                          <div className="flex-1 bg-gray-200 rounded-full h-2 max-w-[60px]">
                            <div
                              className={`h-2 rounded-full ${
                                customer.probability >= 70 ? 'bg-red-500' : 
                                customer.probability >= 40 ? 'bg-yellow-500' : 'bg-green-500'
                              }`}
                              style={{ width: `${customer.probability}%` }}
                            />
                          </div>
                          <span className="font-medium text-gray-900">{customer.probability}%</span>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                          customer.priority === 'High' ? 'bg-red-100 text-red-700' :
                          customer.priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-blue-100 text-blue-700'
                        }`}>
                          {customer.priority}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">{customer.action}</td>
                      <td className="py-3 px-4">
                        <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                          Contact
                        </button>
                      </td>
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
