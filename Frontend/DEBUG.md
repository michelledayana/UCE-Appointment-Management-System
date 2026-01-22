# Guía de Debugging - Error de Registro

## Pasos para Diagnosticar el Error

### 1. Verificar que el API Gateway esté corriendo

```bash
# Verifica que el API Gateway esté en el puerto correcto
curl http://localhost:8000/health
# Debe devolver: {"status": "healthy"}
```

### 2. Verificar que el servicio de registro esté corriendo

El API Gateway necesita conectarse al servicio de registro. Verifica:
- Que el servicio `user-registration-service` esté corriendo
- Que esté en el puerto configurado (probablemente 8081)
- Que la URL en el `.env` del API Gateway sea correcta

### 3. Verificar la configuración del API Gateway

En el archivo `.env` del API Gateway debe estar:
```env
USER_REGISTRATION_URL=http://localhost:8081
```

### 4. Verificar la configuración del Frontend

En el archivo `.env.local` del Frontend debe estar:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Abrir la Consola del Navegador

1. Presiona F12 en el navegador
2. Ve a la pestaña "Console"
3. Intenta registrar nuevamente
4. Revisa los errores que aparecen

### 6. Verificar la Pestaña Network

1. Presiona F12
2. Ve a la pestaña "Network"
3. Intenta registrar
4. Busca la petición a `/users/register`
5. Revisa:
   - Status Code (200, 400, 500, etc.)
   - Response (qué devuelve el servidor)
   - Request Payload (qué se está enviando)

## Errores Comunes

### Error 503 - Service Unavailable
**Causa:** El servicio de registro no está corriendo o no es accesible
**Solución:** 
- Verifica que el servicio esté corriendo
- Verifica la URL en el `.env` del API Gateway

### Error 400 - Bad Request
**Causa:** Los datos enviados no son válidos
**Solución:**
- Verifica que todos los campos estén completos
- Verifica el formato del email

### Error 500 - Internal Server Error
**Causa:** Error en el servidor
**Solución:**
- Revisa los logs del API Gateway
- Revisa los logs del servicio de registro

### Error de CORS
**Causa:** El API Gateway no permite el origen del frontend
**Solución:**
- Verifica que CORS esté configurado para `http://localhost:3000`

### Error de Conexión
**Causa:** No se puede conectar al API Gateway
**Solución:**
- Verifica que el API Gateway esté corriendo
- Verifica la URL en `.env.local` del frontend

## Comandos Útiles

```bash
# Verificar que el API Gateway esté corriendo
curl http://localhost:8000/health

# Verificar que el servicio de registro esté corriendo
curl http://localhost:8081/health

# Ver logs del API Gateway (si está en Docker)
docker logs api_gateway

# Ver logs del servicio de registro (si está en Docker)
docker logs user_registration_service
```

## Información a Compartir para Debugging

Si el error persiste, comparte:
1. El mensaje de error exacto que aparece
2. El código de estado HTTP (de la pestaña Network)
3. La respuesta del servidor (de la pestaña Network)
4. Los logs del API Gateway
5. Los logs del servicio de registro
