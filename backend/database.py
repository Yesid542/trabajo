# database.py
import sqlite3
from flask import g, current_app

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Para acceder por nombre
    return db

def init_db():
    with current_app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Tabla de usuarios (tabla principal)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ficha (
                idFicha INTEGER PRIMARY KEY AUTOINCREMENT,
                ficha TEXT NOT NULL
            )
        ''')
        
        # Tabla de tareas (relación 1:N con usuarios)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                idUsuarios INTEGER PRIMARY KEY AUTOINCREMENT,
                idFicha INTEGER,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                correo TEXT NOT NULL,
                contrasena TEXT NOT NULL,
                tipoDocumento TEXT NOT NULL,
                numeroDocumento TEXT NOT NULL,
                FOREIGN KEY (idFicha) REFERENCES ficha(idFicha) ON DELETE CASCADE
            )
        ''')
        
        # Tabla de comentarios (relación 1:N con tareas)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluacion (
                idEvaluacion INTEGER PRIMARY KEY AUTOINCREMENT,
                idModulo INTEGER NOT NULL,
                descripcionPregunta TEXT NOT NULL,
                opcionA TEXT NOT NULL,
                opcionB TEXT NOT NULL,
                opcionC TEXT NOT NULL,
                opcionD TEXT NOT NULL,
                respuesta TEXT NOT NULL,
                imagenFirebasePath TEXT, 
                calificacion DECIMAL,
                FOREIGN KEY (idModulo) REFERENCES modulo(idModulo) ON DELETE CASCADE
                )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contenido (
                idContenido INTEGER NOT NULL,
                idModulo INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                archivoFirebasePath TEXT NOT NULL,
                avance DECIMAL NOT NULL,
                FOREIGN KEY (idModulo) REFERENCES modulo(idModulo) ON DELETE CASCADE
                
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS modulo(
                idModulo INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                dificultad TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS desarrollo (
                idDesarrollo INTEGER NOT NULL,
                idModulo INTEGER NOT NULL,
                idUsuarios INTEGER NOT NULL,
                avance DECIMAL NOT NULL,
                FOREIGN KEY (idModulo) REFERENCES modulo(idModulo) ON DELETE CASCADE,
                FOREIGN KEY (idUsuarios) REFERENCES usuarios(idUsuarios) ON DELETE CASCADE   
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS biblioteca (
                idBiblioteca INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                imagenFirebasePath TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS modifica (
                idModifica INTEGER NOT NULL,
                idUsuarios INTEGER NOT NULL,
                idBiblioteca INTEGER NOT NULL,
                fechaHora DATETIME NOT NULL,  
                FOREIGN KEY (idUsuarios) REFERENCES usuarios(idUsuarios) ON DELETE CASCADE,
                FOREIGN KEY (idBiblioteca) REFERENCES biblioteca(idBiblioteca) ON DELETE CASCADE   
            )
        ''')
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS rutas (
             id INTEGER PRIMARY KEY AUTOINCREMENT, 
             nombre_archivo TEXT NOT NULL,
             ruta_supabase TEXT NOT NULL,
             tipo_archivo TEXT NOT NULL,
             tamaño INTEGER,
             id_referencia INTEGER NOT NULL,
             idTablas TEXT,
             creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
             FOREIGN KEY (idTablas) REFERENCES tablas(nombre) 
            )
        ''')
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS tablas (
             nombre TEXT PRIMARY KEY 
             )
             
        ''')

        db.commit()

def close_db(error=None):
    db = g.pop('_database', None)
    if db is not None:
        db.close()