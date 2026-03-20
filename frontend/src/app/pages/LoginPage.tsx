import { useState } from 'react';
import { useNavigate } from 'react-router';
import { BarChart3, Shield, TrendingUp, Users } from 'lucide-react';

export function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Simple navigation to dashboard
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex">
      {/* Left Panel - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-600 to-indigo-700 p-12 flex-col justify-between text-white">
        <div>
          <h1 className="text-4xl font-bold mb-4">ChurnGuard</h1>
          <p className="text-xl text-blue-100">Intelligent Customer Churn Analytics Platform</p>
        </div>

        <div className="space-y-8">
          <div className="flex items-start gap-4">
            <div className="bg-white/20 p-3 rounded-lg">
              <BarChart3 size={24} />
            </div>
            <div>
              <h3 className="font-semibold mb-1">Advanced Analytics</h3>
              <p className="text-blue-100 text-sm">Predict customer churn with ML-powered insights</p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <div className="bg-white/20 p-3 rounded-lg">
              <Shield size={24} />
            </div>
            <div>
              <h3 className="font-semibold mb-1">Retention Strategies</h3>
              <p className="text-blue-100 text-sm">Actionable recommendations to reduce churn</p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <div className="bg-white/20 p-3 rounded-lg">
              <TrendingUp size={24} />
            </div>
            <div>
              <h3 className="font-semibold mb-1">Revenue Protection</h3>
              <p className="text-blue-100 text-sm">Protect revenue by identifying at-risk customers</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-8 text-sm text-blue-100">
          <div className="flex items-center gap-2">
            <Users size={16} />
            <span>500K+ Customers Analyzed</span>
          </div>
        </div>
      </div>

      {/* Right Panel - Login Form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="bg-white rounded-2xl shadow-2xl p-10 w-full max-w-md">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h2>
            <p className="text-gray-600">Sign in to your ChurnGuard account</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="you@company.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your password"
                required
              />
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input type="checkbox" className="mr-2 rounded" />
                <span className="text-sm text-gray-600">Remember me</span>
              </label>
              <a href="#" className="text-sm text-blue-600 hover:text-blue-700">
                Forgot password?
              </a>
            </div>

            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Sign In
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-600">
            Don't have an account?{' '}
            <a href="#" className="text-blue-600 hover:text-blue-700 font-medium">
              Contact Sales
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
