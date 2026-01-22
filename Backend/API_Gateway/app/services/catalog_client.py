from app.utils.http_client import forward_request
from app.config import settings

def get_services(headers):
    return forward_request(
        method="GET",
        url=f"{settings.SERVICE_CATALOG_URL}/catalog/services",
        headers=headers
    )
