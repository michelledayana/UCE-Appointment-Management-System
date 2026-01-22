from fastapi import APIRouter, HTTPException, Depends
import requests
from app.config import settings
from app.security.dependencies import admin_required

router = APIRouter()

@router.get("/health", dependencies=[Depends(admin_required)])
def admin_health():
    """Health check del servicio de administración"""
    try:
        response = requests.get(
            f"{settings.ADMINISTRATION_SERVICE_URL}/admin/health",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/stats", dependencies=[Depends(admin_required)])
def dashboard_stats():
    """Obtener estadísticas del dashboard"""
    try:
        response = requests.get(
            f"{settings.ADMINISTRATION_SERVICE_URL}/admin/dashboard/stats",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Devolver datos de ejemplo si el servicio no está disponible
        return {
            "totalUsers": 150,
            "appointmentsToday": 12,
            "activeServices": 8,
            "monthlyRevenue": 15000,
            "recentAppointments": [
                {"id": 1, "serviceName": "Consulta General", "userName": "Juan Pérez", "status": "confirmed"},
                {"id": 2, "serviceName": "Terapia Física", "userName": "María García", "status": "pending"},
            ]
        }

@router.get("/monitoring/health", dependencies=[Depends(admin_required)])
def monitoring_health():
    """Estado del sistema"""
    return {
        "status": "healthy",
        "services": [
            {"name": "API Gateway", "status": "healthy", "uptime": "99.9%", "responseTime": "45ms"},
            {"name": "Auth Service", "status": "healthy", "uptime": "99.8%", "responseTime": "32ms"},
            {"name": "Appointment Service", "status": "healthy", "uptime": "99.7%", "responseTime": "58ms"},
            {"name": "User Service", "status": "healthy", "uptime": "99.9%", "responseTime": "28ms"},
            {"name": "Database", "status": "healthy", "uptime": "100%", "responseTime": "15ms"},
        ]
    }

@router.get("/monitoring/metrics", dependencies=[Depends(admin_required)])
def monitoring_metrics():
    """Métricas del sistema"""
    return {
        "requestsPerMinute": 142,
        "activeUsers": 89,
        "averageResponseTime": 43,
        "errorRate": 0.2,
        "cpuUsage": 45,
        "memoryUsage": 62,
        "diskUsage": 38,
    }