const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
const isDev = process.argv.includes('--dev');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      webSecurity: true,
    },
    icon: path.join(__dirname, 'assets', 'icon.png'),
    show: false,
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
  });

  // Cargar la aplicación web
  const startUrl = 'http://localhost:3000';

  // Función para cargar la URL con reintentos
  const loadApp = () => {
    const http = require('http');
    const checkServer = () => {
      const req = http.get(startUrl, (res) => {
        if (res.statusCode === 200) {
          mainWindow.loadURL(startUrl);
        } else {
          setTimeout(checkServer, 1000);
        }
      });
      req.on('error', () => {
        setTimeout(checkServer, 1000);
      });
      req.setTimeout(2000, () => {
        req.destroy();
        setTimeout(checkServer, 1000);
      });
    };
    checkServer();
  };

  loadApp();

  // Mostrar ventana cuando esté lista
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Abrir DevTools en desarrollo
    if (isDev) {
      mainWindow.webContents.openDevTools();
    }
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Manejar errores de carga
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    if (isDev) {
      console.error('Error loading:', errorCode, errorDescription);
    } else {
      mainWindow.loadURL(startUrl);
    }
  });
}

// Crear menú de aplicación
function createMenu() {
  const template = [
    {
      label: 'Archivo',
      submenu: [
        {
          label: 'Salir',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => {
            app.quit();
          },
        },
      ],
    },
    {
      label: 'Ver',
      submenu: [
        {
          label: 'Recargar',
          accelerator: 'CmdOrCtrl+R',
          click: (item, focusedWindow) => {
            if (focusedWindow) focusedWindow.reload();
          },
        },
        {
          label: 'Forzar Recarga',
          accelerator: 'CmdOrCtrl+Shift+R',
          click: (item, focusedWindow) => {
            if (focusedWindow) focusedWindow.webContents.reloadIgnoringCache();
          },
        },
        {
          label: 'Alternar Herramientas de Desarrollador',
          accelerator: process.platform === 'darwin' ? 'Alt+Cmd+I' : 'Ctrl+Shift+I',
          click: (item, focusedWindow) => {
            if (focusedWindow) {
              focusedWindow.webContents.toggleDevTools();
            }
          },
        },
        { type: 'separator' },
        {
          label: 'Pantalla Completa',
          accelerator: process.platform === 'darwin' ? 'Ctrl+Cmd+F' : 'F11',
          click: (item, focusedWindow) => {
            if (focusedWindow) {
              focusedWindow.setFullScreen(!focusedWindow.isFullScreen());
            }
          },
        },
      ],
    },
    {
      label: 'Ayuda',
      submenu: [
        {
          label: 'Acerca de',
          click: () => {
            // Aquí puedes mostrar un diálogo de "Acerca de"
          },
        },
      ],
    },
  ];

  if (process.platform === 'darwin') {
    template.unshift({
      label: app.getName(),
      submenu: [
        { label: 'Acerca de ' + app.getName(), role: 'about' },
        { type: 'separator' },
        { label: 'Servicios', role: 'services', submenu: [] },
        { type: 'separator' },
        { label: 'Ocultar ' + app.getName(), accelerator: 'Command+H', role: 'hide' },
        { label: 'Ocultar Otros', accelerator: 'Command+Shift+H', role: 'hideothers' },
        { label: 'Mostrar Todo', role: 'unhide' },
        { type: 'separator' },
        { label: 'Salir', accelerator: 'Command+Q', click: () => app.quit() },
      ],
    });
  }

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

app.whenReady().then(() => {
  createWindow();
  createMenu();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Manejar enlaces externos
app.on('web-contents-created', (event, contents) => {
  contents.on('new-window', (event, navigationUrl) => {
    event.preventDefault();
    // Abrir enlaces externos en el navegador predeterminado
    require('electron').shell.openExternal(navigationUrl);
  });
});
