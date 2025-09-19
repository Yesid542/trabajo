const { app, BrowserWindow,Menu } = require('electron')
const path = require('path')

let mainWindow

function createWindow() {

  const iconPath = path.join(__dirname, '../frontend/public/App.ico')
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },

    icon: iconPath
  })



  // Cargar el frontend de Vite en desarrollo
  mainWindow.loadURL('http://localhost:5173')

}


app.whenReady().then(createWindow)