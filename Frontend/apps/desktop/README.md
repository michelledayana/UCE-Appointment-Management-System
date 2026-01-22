# Sistema de Agendamiento de Citas - Aplicación de Escritorio

Aplicación de escritorio desarrollada con Electron que empaqueta la aplicación web Next.js.

## 🚀 Características

- ✅ Interfaz web completa empaquetada
- ✅ Multiplataforma (Windows, macOS, Linux)
- ✅ Auto-actualización (opcional)
- ✅ Menús nativos
- ✅ Accesos directos de teclado

## 📋 Requisitos

- Node.js 18+ 
- npm o yarn
- La aplicación web Next.js debe estar corriendo o construida

## 🛠️ Instalación

1. **Instalar dependencias:**
```bash
npm install
```

2. **Asegurarse de que la app web esté disponible:**
   - En desarrollo: La app web debe estar corriendo en `http://localhost:3000`
   - En producción: Construir la app web primero

## ▶️ Ejecutar

### Modo Desarrollo
```bash
# Terminal 1: Ejecutar la app web
cd ../web
npm run dev

# Terminal 2: Ejecutar Electron
cd ../desktop
npm run dev
```

### Modo Producción
```bash
# Primero construir la app web
cd ../web
npm run build

# Luego construir la app de escritorio
cd ../desktop
npm run build
```

## 📦 Construir Ejecutables

### Windows
```bash
npm run build:win
```

### macOS
```bash
npm run build:mac
```

### Linux
```bash
npm run build:linux
```

Los ejecutables se generarán en la carpeta `dist/`.

## ⚙️ Configuración

### Modo Desarrollo
La aplicación carga `http://localhost:3000` automáticamente.

### Modo Producción
La aplicación carga los archivos estáticos de la build de Next.js.

## 🔧 Personalización

### Cambiar el Icono
Reemplazar los archivos en `assets/`:
- `icon.ico` - Windows
- `icon.icns` - macOS
- `icon.png` - Linux

### Cambiar el Título
Editar `productName` en `package.json` → `build`.

## 📁 Estructura

```
desktop/
├── main.js          # Proceso principal de Electron
├── preload.js       # Script de preload seguro
├── package.json     # Configuración y dependencias
├── assets/          # Iconos de la aplicación
└── dist/            # Ejecutables generados (después de build)
```

## 🐛 Solución de Problemas

### La aplicación no carga
- Verificar que la app web esté corriendo en desarrollo
- Verificar que la build de Next.js exista en producción

### Errores de CORS
- La app web debe permitir el origen de Electron
- Verificar configuración de Next.js

## 📝 Notas

- La aplicación usa la misma base de código que la web
- Todos los cambios en la web se reflejan automáticamente
- El almacenamiento local funciona igual que en el navegador
