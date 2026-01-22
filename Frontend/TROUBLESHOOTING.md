# Solución de Problemas - Frontend

## Errores Comunes y Soluciones

### 1. Error: "Cannot find module '@/...'"

**Problema:** TypeScript no encuentra los módulos con alias `@/`

**Solución:**
```bash
# Asegúrate de que tsconfig.json tenga la configuración correcta
# Verifica que el archivo tsconfig.json tenga:
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}

# Luego reinicia el servidor de desarrollo
npm run dev
```

### 2. Error: "Module not found: Can't resolve 'date-fns/locale'"

**Problema:** La versión de date-fns puede no tener el locale o está mal importado

**Solución:**
```bash
# Reinstala date-fns
npm uninstall date-fns
npm install date-fns@^2.30.0
```

### 3. Error: "use client" directive required

**Problema:** Estás usando hooks de React en un Server Component

**Solución:**
- Asegúrate de que todos los componentes que usan hooks tengan `'use client'` al inicio
- El layout.tsx debe ser Server Component, pero los providers deben ser Client Components

### 4. Error: "Hydration failed"

**Problema:** Hay diferencias entre el renderizado del servidor y del cliente

**Solución:**
- Verifica que no estés usando `window` o `document` directamente en el render inicial
- Usa `useEffect` para código que depende del cliente

### 5. Error: "Cannot read property 'token' of undefined"

**Problema:** El token no se está guardando correctamente en cookies

**Solución:**
```bash
# Verifica que js-cookie esté instalado
npm install js-cookie @types/js-cookie

# Verifica que el API Gateway esté corriendo
# Verifica que CORS esté configurado correctamente
```

### 6. Error de CORS

**Problema:** El navegador bloquea las peticiones por CORS

**Solución:**
- Verifica que el API Gateway tenga configurado CORS para `http://localhost:3000`
- En el API Gateway, asegúrate de tener:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 7. Error: "TypeError: Cannot read property 'map' of undefined"

**Problema:** Estás intentando hacer map sobre un valor undefined

**Solución:**
- Siempre verifica que los datos existan antes de hacer map
- Usa optional chaining: `data?.map(...)`
- Proporciona valores por defecto: `data || []`

### 8. Error al instalar dependencias

**Problema:** Conflictos de versiones o problemas con npm/yarn

**Solución:**
```bash
# Limpia la caché y reinstala
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# O si usas yarn
rm -rf node_modules yarn.lock
yarn cache clean
yarn install
```

### 9. Error: "Port 3000 is already in use"

**Problema:** Ya hay otro proceso usando el puerto 3000

**Solución:**
```bash
# En Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# En Linux/Mac
lsof -ti:3000 | xargs kill -9

# O usa otro puerto
npm run dev -- -p 3001
```

### 10. Error: TailwindCSS no funciona

**Problema:** Los estilos de Tailwind no se aplican

**Solución:**
```bash
# Verifica que tailwind.config.js esté configurado correctamente
# Verifica que globals.css tenga los imports de Tailwind
# Reinicia el servidor de desarrollo
```

## Pasos para Debugging

1. **Verifica que todas las dependencias estén instaladas:**
```bash
npm install
```

2. **Limpia la caché de Next.js:**
```bash
rm -rf .next
npm run dev
```

3. **Verifica los logs del servidor:**
- Revisa la consola del terminal donde ejecutas `npm run dev`
- Revisa la consola del navegador (F12)

4. **Verifica la configuración:**
- `.env.local` existe y tiene `NEXT_PUBLIC_API_URL`
- `tsconfig.json` tiene los paths correctos
- `tailwind.config.js` está configurado

5. **Revisa la versión de Node.js:**
```bash
node --version
# Debe ser 18 o superior
```

## Comandos Útiles

```bash
# Desarrollo
npm run dev

# Build de producción
npm run build

# Iniciar producción
npm start

# Linter
npm run lint

# Verificar tipos TypeScript
npx tsc --noEmit
```

## Si Nada Funciona

1. Elimina `node_modules` y `package-lock.json`
2. Elimina `.next` (carpeta de build)
3. Reinstala todo: `npm install`
4. Reinicia el servidor: `npm run dev`

Si el problema persiste, comparte el mensaje de error completo para poder ayudarte mejor.
