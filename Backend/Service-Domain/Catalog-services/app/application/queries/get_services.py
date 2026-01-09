from app.infrastructure.db.mongo import services_collection

def get_services_query():
    services = list(services_collection.find({"is_active": True}))
    return services
