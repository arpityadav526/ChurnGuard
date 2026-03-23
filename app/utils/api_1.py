import requests
from typing import Dict, Any, Optional

BASE_URL = "http://127.0.0.1:8000"   # change later when deployed


def get_request(endpoint: str, params: Optional[Dict[str, Any]] = None):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def post_request(endpoint: str, json_data: Optional[Dict[str, Any]] = None, files=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        if files:
            response = requests.post(url, files=files, timeout=60)
        else:
            response = requests.post(url, json=json_data, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}