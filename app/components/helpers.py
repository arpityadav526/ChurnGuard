import os
import requests
import pandas as pd
import streamlit as st


def get_base_url():
    try:
        return st.secrets["BASE_URL"].rstrip("/")
    except Exception:
        return os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")


BASE_URL = get_base_url()


def get_data(endpoint: str):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=20)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        st.error("Request timed out. Backend is taking too long.")
        return None

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Check whether the backend URL is correct and the FastAPI server is running.")
        return None

    except requests.exceptions.HTTPError as e:
        try:
            error_detail = response.json()
            st.error(f"API error: {error_detail}")
        except Exception:
            st.error(f"HTTP error: {e}")
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None


def post_json(endpoint: str, payload: dict):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        st.error("Prediction request timed out.")
        return None

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Check whether the backend URL is correct and the FastAPI server is running.")
        return None

    except requests.exceptions.HTTPError as e:
        try:
            error_detail = response.json()
            st.error(f"API error: {error_detail}")
        except Exception:
            st.error(f"HTTP error: {e}")
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None


def post_file(endpoint: str, uploaded_file):
    if uploaded_file is None:
        st.warning("Please upload a CSV file first.")
        return None

    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        response = requests.post(f"{BASE_URL}{endpoint}", files=files, timeout=120)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        st.error("Batch prediction request timed out.")
        return None

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Check whether the backend URL is correct and the FastAPI server is running.")
        return None

    except requests.exceptions.HTTPError as e:
        try:
            error_detail = response.json()
            st.error(f"API error: {error_detail}")
        except Exception:
            st.error(f"HTTP error: {e}")
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None


def show_metric_card(label, value):
    st.metric(label, value)


def safe_dataframe(data):
    if data is None:
        return pd.DataFrame()
    return pd.DataFrame(data)