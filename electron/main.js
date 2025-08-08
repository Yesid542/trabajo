const { app, BrowserWindow } = require('electron')
const path = require('path')

let mainWindow

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    }
  })

  // Cargar el frontend de Vite en desarrollo
  mainWindow.loadURL('http://localhost:5173')
  mainWindow.webContents.openDevTools() // Opcional: abre DevTools
}

app.whenReady().then(createWindow)