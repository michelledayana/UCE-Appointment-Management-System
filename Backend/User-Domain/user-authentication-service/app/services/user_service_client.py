import os
import requests
from fastapi import HTTPException

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")

def get_user_by_email(email: str):
    try:
        response = requests.get(
            f"{USER_SERVICE_URL}/users/by-email/{email}"
        )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="User service not available"
        )

    if response.status_code != 200:
        return None

    return response.json()
