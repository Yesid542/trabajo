from datetime import datetime
from .database_helpers import ejecutar_consulta

def crear_ruta_archivo(data):
    """
    Crea un registro en la tabla rutas con validación de tabla existente
    """
    try:
        # Validar que la tabla referenciada exista
        if not existe_tabla(data['idTablas']):
            raise ValueError(f"La tabla '{data['idTablas']}' no está registrada")
        
        query = '''
            INSERT INTO rutas (nombre_archivo, ruta_supabase, tipo_archivo, 
                             tamaño, id_referencia, idTablas)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        params = (
            data['nombre_archivo'],
            data['ruta_supabase'],
            data['tipo_archivo'],
            data['tamaño'],
            data['id_referencia'],
            data['idTablas']
        )
        
        # ejecutar_consulta devuelve el ID del último registro insertado
        return ejecutar_consulta(query, params)
        
    except Exception as e:
        raise Exception(f"Error creando ruta: {str(e)}")

def obtener_rutas_por_referencia(id_referencia, idTablas):
    """
    Obtiene todas las rutas asociadas a un recurso
    """
    try:
        # Validar que la tabla exista
        if not existe_tabla(idTablas):
            return []
        
        resultados = ejecutar_consulta(
            '''SELECT r.*, t.nombre as nombre_tabla 
               FROM rutas r 
               LEFT JOIN tablas t ON r.idTablas = t.nombre
               WHERE r.id_referencia = ? AND r.idTablas = ?
               ORDER BY r.creado_en DESC''',
            (id_referencia, idTablas)
        )
        
        # Asegurar que siempre retornamos una lista
        return resultados if isinstance(resultados, list) else []
        
    except Exception as e:
        raise Exception(f"Error obteniendo rutas: {str(e)}")

def obtener_ruta_por_id(id_ruta):
    """
    Obtiene una ruta específica por su ID
    """
    try:
        resultados = ejecutar_consulta(
            '''SELECT r.*, t.nombre as nombre_tabla 
               FROM rutas r 
               LEFT JOIN tablas t ON r.idTablas = t.nombre
               WHERE r.id = ?''',
            (id_ruta,)
        )
        
        # Si es lista, tomar el primer elemento, sino retornar None
        if isinstance(resultados, list) and resultados:
            return resultados[0]
        return None
            
    except Exception as e:
        raise Exception(f"Error obteniendo ruta: {str(e)}")

def eliminar_ruta(id_ruta):
    """
    Elimina un registro de la tabla rutas
    """
    try:
        filas_afectadas = ejecutar_consulta(
            "DELETE FROM rutas WHERE id = ?",
            (id_ruta,)
        )
        
        # ejecutar_consulta retorna rowcount para DELETE
        return filas_afectadas > 0 if isinstance(filas_afectadas, int) else False
        
    except Exception as e:
        raise Exception(f"Error eliminando ruta: {str(e)}")

def obtener_todas_rutas():
    """Obtiene todas las rutas con información de la tabla"""
    try:
        resultados = ejecutar_consulta('''
            SELECT r.*, t.nombre as nombre_tabla 
            FROM rutas r 
            LEFT JOIN tablas t ON r.idTablas = t.nombre
            ORDER BY r.creado_en DESC
        ''')
        
        # Asegurar que siempre retornamos una lista
        return resultados if isinstance(resultados, list) else []
        
    except Exception as e:
        raise Exception(f"Error obteniendo rutas: {str(e)}")

def contar_rutas_por_tabla(idTablas):
    """
    Cuenta cuántas rutas hay para una tabla específica
    """
    try:
        resultados = ejecutar_consulta(
            "SELECT COUNT(*) as total FROM rutas WHERE idTablas = ?",
            (idTablas,)
        )
        
        # Si es lista, tomar el primer elemento
        if isinstance(resultados, list) and resultados:
            return resultados[0].get('total', 0)
        return 0
        
    except Exception as e:
        raise Exception(f"Error contando rutas: {str(e)}")