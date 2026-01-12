import requests
from fastapi import HTTPException

def forward_request(method, url, headers=None, json=None):
    response = requests.request(method, url, headers=headers, json=json)

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()
