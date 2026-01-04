import requests
from fastapi import HTTPException

USER_SERVICE_URL = "http://localhost:8081"

def get_user_by_email(email: str):
    response = requests.get(
        f"{USER_SERVICE_URL}/users/by-email",
        params={"email": email}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return response.json()
