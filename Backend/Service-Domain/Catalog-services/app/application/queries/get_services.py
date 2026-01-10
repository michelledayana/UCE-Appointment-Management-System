from app.infrastructure.db.mongo import services_collection
from app.infrastructure.redis.cache import (
    get_services_cache,
    set_services_cache
)


def get_services_query():
    # 1️⃣ Try cache first
    cached_services = get_services_cache()
    if cached_services:
        return cached_services

    # 2️⃣ Query MongoDB
    services = list(services_collection.find({}, {"_id": 0}))

    # 3️⃣ Store in cache
    set_services_cache(services)

    return services
