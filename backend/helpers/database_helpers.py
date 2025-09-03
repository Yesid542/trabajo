# helpers/database_helpers.py
from database import get_db
import sqlite3

def ejecutar_consulta(query, params=()):
    """
    Función genérica para ejecutar consultas SQL de manera segura
    """
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query, params)
        
        # Si es una consulta SELECT, retornar resultados
        if query.strip().upper().startswith('SELECT'):
            resultados = cursor.fetchall()
            return [dict(row) for row in resultados]  # Convertir a diccionarios
        
        # Si es INSERT, UPDATE, DELETE
        else:
            db.commit()
            return cursor.lastrowid  # Retornar el ID del último registro insertado
            
    except sqlite3.Error as e:
        # Revertir cambios en caso de error
        db.rollback()
        raise Exception(f"Error en la base de datos: {str(e)}")
    
    finally:
        # Siempre cerrar el cursor
        cursor.close()