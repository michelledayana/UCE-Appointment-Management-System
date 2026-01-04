import requests
from app.config import USER_SERVICE_URL

def register_user(payload: dict):
    try:
        response = requests.post(
            f"{USER_SERVICE_URL}/users/register",
            json=payload,
            timeout=5
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"User service unavailable: {str(e)}")
