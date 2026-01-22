from fastapi import APIRouter, HTTPException
import requests
from app.config import settings

router = APIRouter()

@router.post("/register")
def register(data: dict):
    try:
        # Validar que los datos requeridos estén presentes
        if not data.get('full_name') or not data.get('email') or not data.get('password'):
            raise HTTPException(
                status_code=400,
                detail="Faltan campos requeridos: full_name, email, password"
            )
        
        response = requests.post(
            f"{settings.USER_REGISTRATION_URL}/users/register",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            try:
                error_detail = e.response.json().get('detail', 'Error al registrar usuario')
            except:
                error_detail = e.response.text or 'Error al registrar usuario'
            raise HTTPException(
                status_code=e.response.status_code,
                detail=error_detail
            )
        raise HTTPException(status_code=500, detail="Error al conectar con el servicio de registro")
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail=f"No se pudo conectar con el servicio de registro en {settings.USER_REGISTRATION_URL}. Verifica que el servicio esté corriendo."
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="El servicio de registro tardó demasiado en responder. Intenta nuevamente."
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error de conexión: {str(e)}"
        )
