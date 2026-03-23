# ChurnGuard

ChurnGuard is an end-to-end customer churn prediction and retention analytics platform designed to identify at-risk customers, explain churn drivers, and support proactive retention decisions. The system combines machine learning, FastAPI, Streamlit, and SQLite to deliver real-time predictions, batch analysis, dashboard insights, customer-level explainability, and model monitoring.

---

## Project Overview

Customer churn has a direct impact on recurring revenue, customer lifetime value, and long-term business growth, especially in subscription-based industries such as telecom, SaaS, and OTT platforms. ChurnGuard helps address this challenge by predicting which customers are likely to leave, identifying the factors contributing to that risk, and recommending retention actions that can reduce customer loss.

This project was built as a full-stack analytics platform rather than just a machine learning notebook. It includes:

- a backend prediction API
- an interactive frontend
- persistent storage for prediction history
- a business dashboard
- explainable AI components
- model performance monitoring
- automated API tests

---

## Problem Statement

Many organizations struggle to detect churn risk early enough to take meaningful action. Traditional reporting is often reactive and provides only historical summaries, not customer-level predictive intelligence.

ChurnGuard solves this by:

- predicting churn probability for individual customers
- identifying customer risk levels
- surfacing churn drivers and business-friendly explanations
- recommending retention strategies
- supporting batch prediction workflows
- storing and analyzing prediction history for monitoring and review

---

## Key Features

### 1. Single Customer Prediction
Users can enter customer attributes through a Streamlit form and receive:

- churn probability
- churn prediction
- risk category
- churn drivers
- key risk factors
- recommended retention action

### 2. Batch Prediction
Users can upload a CSV file and generate churn predictions for multiple customers at once. This supports analyst workflows and bulk customer risk assessment.

### 3. Explainable Predictions
Each customer prediction includes:

- why the customer may churn
- key risk factors
- business-oriented retention suggestions

### 4. Interactive Dashboard
The dashboard provides:

- total customers
- churn rate
- high-risk customers
- predicted revenue at risk
- risk distribution
- churn by contract type
- churn by payment method
- recent predictions

### 5. Customer Insights Module
Users can inspect:

- the latest predicted customer
- stored customer predictions by index
- top churn drivers
- key risk factors
- retention recommendations

### 6. Model Performance Monitoring
A dedicated page displays:

- accuracy
- precision
- recall
- F1-score
- ROC-AUC
- confusion matrix

### 7. Prediction History with SQLite
Predictions are stored in a SQLite database, enabling:

- persistent storage
- history review
- analytics support
- dashboard reporting

### 8. API Testing
Backend endpoints are validated using pytest and FastAPI TestClient.

---

## Tech Stack

### Backend
- FastAPI
- Python
- Pandas
- Joblib
- SQLite

### Frontend
- Streamlit

### Machine Learning
- Scikit-learn
- XGBoost / Random Forest (depending on active trained model)
- Feature engineering
- Threshold tuning

### Database
- SQLite

### Testing
- Pytest
- FastAPI TestClient

---

## Project Structure

```bash
ChurnGuard/
│
├── app/
│   └── pages/
│       ├── 1_Dashboard.py
│       ├── 2_Single_Prediction.py
│       ├── 3_Batch_Prediction.py
│       ├── 4_Customer_Insights.py
│       ├── 5_Model_Performance.py
│       └── 6_Prediction_History.py
│
├── src/
│   ├── dashboard/
│   │   └── api.py
│   └── models/
│       ├── train_model.py
│       ├── churn_model.pkl
│       ├── model_columns.pkl
│       └── model_metrics.pkl
│
├── data/
│   ├── raw/
│   │   └── IBM Teleco Churn Dataset.csv
│   └── processed/
│       ├── churnguard.db
│       └── prediction_history.csv
│
├── tests/
│   └── test_api.py
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
