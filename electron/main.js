const { spawn } = require('child_process');
const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  const iconPath = path.join(__dirname, '../frontend/public/App.ico');
  const backendPath = path.join(__dirname, '../backend/server.py');

  const pythonProcess = spawn('python', [backendPath], {
    detached: true,
    stdio: 'ignore'
  });
  pythonProcess.unref();

  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
    icon: iconPath
  });

  // Cargar frontend (elige solo una opción según el entorno)
  mainWindow.loadFile(path.join(__dirname, './dist/index.html'));
  mainWindow.loadFile(path.join(__dirname, '../frontend/dist/index.html'));

}

app.whenReady().then(createWindow);