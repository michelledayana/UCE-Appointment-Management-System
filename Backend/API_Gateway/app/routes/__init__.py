from .auth import router as auth_router
from .users import router as users_router
from .profile import router as profile_router
from .catalog import router as catalog_router
from .scheduling import router as scheduling_router
from .appointment import router as appointment_router
from .admin import router as admin_router

__all__ = [
    "auth_router",
    "users_router",
    "profile_router",
    "catalog_router",
    "scheduling_router",
    "appointment_router",
    "admin_router",
]
