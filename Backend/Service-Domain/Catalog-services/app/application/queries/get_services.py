from app.infrastructure.db.mongo import services_collection

def get_services_query():
    services = []
    for service in services_collection.find():
        service["_id"] = str(service["_id"])
        services.append(service)
    return services
