Design a modern, professional ReactJS frontend UI for an industry-level project called “ChurnGuard – Intelligent Customer Churn Analytics Platform”.

The product is a customer churn prediction and retention strategy dashboard for business teams, analysts, and managers. The frontend should look like a real SaaS analytics product used inside a company like Thomson Reuters, not like a student project.

Design goals:
- Clean, premium, enterprise-style interface
- Modern dashboard aesthetic
- Minimal but high-information layout
- Strong visual hierarchy
- Responsive desktop-first design
- Easy to convert into React components later
- Use card-based layouts, charts, tables, filters, KPI widgets, and side navigation
- Use a professional color palette: white / off-white background, dark text, blue primary accents, subtle green/yellow/red for risk levels
- Avoid overly flashy gradients or gaming-style visuals

Create the following screens:

1. Login Page
- Product name: ChurnGuard
- Subtitle: Intelligent Customer Churn Analytics Platform
- Clean login form with email and password
- “Sign In” button
- Optional illustration or analytics-themed side panel
- Enterprise SaaS style

2. Main Dashboard
- Left sidebar navigation
- Top navbar with page title, search bar, notifications, and user profile
- KPI cards:
  - Total Customers
  - Churn Rate
  - High-Risk Customers
  - Predicted Revenue at Risk
- Main charts section:
  - Churn trend line chart
  - Risk distribution donut/pie chart
  - Contract type vs churn bar chart
- Segment summary cards:
  - Low Risk
  - Medium Risk
  - High Risk
- Table of recent customer predictions with columns:
  - Customer ID
  - Contract
  - Monthly Charges
  - Churn Probability
  - Risk Level
  - Suggested Action
- Filters panel for:
  - Contract type
  - Internet service
  - Payment method
  - Risk level

3. Customer Prediction Page
- Form to input single customer data
- Fields:
  - Gender
  - Senior Citizen
  - Partner
  - Dependents
  - Tenure
  - Phone Service
  - Multiple Lines
  - Internet Service
  - Online Security
  - Online Backup
  - Device Protection
  - Tech Support
  - Streaming TV
  - Streaming Movies
  - Contract
  - Paperless Billing
  - Payment Method
  - Monthly Charges
  - Total Charges
- “Predict Churn” button
- Output result card showing:
  - Churn Probability
  - Prediction (Will Churn / Will Stay)
  - Risk Level
  - Retention Recommendation
- Add a visual gauge or progress bar for churn probability

4. Customer Insights / Explainability Page
- Show why the model predicted churn
- Layout with:
  - Top churn drivers cards
  - Feature importance bar chart
  - SHAP-inspired explanation panel
  - Customer profile summary
- Include explanation text like:
  - Month-to-month contract increased churn risk
  - High monthly charges increased churn risk
  - Low tenure increased churn risk
- Make this page look analytical and executive-friendly

5. Retention Strategy Page
- Table or card layout for customers needing intervention
- Priority tagging: High / Medium / Low
- Suggested retention action cards such as:
  - Offer long-term contract discount
  - Provide bundle offer
  - Offer free tech support trial
  - Launch onboarding engagement campaign
- Add campaign summary widgets:
  - Customers targeted
  - Expected saves
  - Potential revenue retained

6. Reports / Business Analytics Page
- Executive overview dashboard for business stakeholders
- More polished summary view with:
  - Churn by payment method
  - Churn by tenure group
  - Churn by service type
  - Revenue impact panel
- Add export buttons for PDF/CSV
- Make it suitable for managers and analysts

Navigation items in sidebar:
- Dashboard
- Predict Customer
- Insights
- Retention Strategy
- Reports
- Settings

Design system requirements:
- Use consistent spacing and grid layout
- Rounded cards
- Soft shadows
- Clean tables
- Modern input fields
- Clearly differentiated status badges
- Risk colors:
  - Low Risk = green
  - Medium Risk = amber/yellow
  - High Risk = red
- Use icons where relevant
- Typography should feel modern, readable, and enterprise-grade
- Keep layouts realistic for implementation in React with reusable components

Technical handoff intention:
This design will later be implemented in ReactJS, so structure it with reusable UI sections and components in mind:
- Sidebar
- Navbar
- KPI cards
- Chart cards
- Filter panel
- Data table
- Form components
- Result cards
- Status badges
- Recommendation cards

Please generate a complete multi-screen product UI with consistent visual language, suitable for a portfolio-quality full-stack analytics platform.