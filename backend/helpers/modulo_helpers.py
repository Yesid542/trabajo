# helpers/modulo_helpers.py
from .database_helpers import ejecutar_consulta

def validar_modulo_data(data, es_actualizacion=False):
    """
    Valida los datos del módulo (versión simplificada)
    """
    campos_requeridos = ['nombre', 'descripcion', 'dificultad']
    
    if not es_actualizacion:
        for campo in campos_requeridos:
            if campo not in data or data[campo] is None:
                raise ValueError(f"El campo '{campo}' es requerido")
    
    # Validaciones específicas
    if 'nombre' in data and data['nombre']:
        nombre = data['nombre'].strip()
        if len(nombre) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        data['nombre'] = nombre
    
    if 'descripcion' in data and data['descripcion']:
        descripcion = data['descripcion'].strip()
        if len(descripcion) < 10:
            raise ValueError("La descripción debe tener al menos 10 caracteres")
        data['descripcion'] = descripcion
    return data

def crear_modulo(data):
    """
    Crea un nuevo módulo en la base de datos (versión simplificada)
    """
    try:
        data = validar_modulo_data(data)
        
        query = """
            INSERT INTO modulo 
            (nombre, descripcion, dificultad) 
            VALUES (?, ?, ?)
        """
        
        nuevo_id = ejecutar_consulta(
            query,
            (
                data['nombre'],
                data['descripcion'],
                data['dificultad']
            )
        )
        
        return nuevo_id
        
    except Exception as e:
        raise Exception(f"Error al crear módulo: {str(e)}")

def obtener_todos_modulos():
    """
    Obtiene todos los módulos de la base de datos
    """
    try:
        return ejecutar_consulta("""
            SELECT * FROM modulo 
            ORDER BY idModulo DESC
        """)
    except Exception as e:
        raise Exception(f"Error al obtener módulos: {str(e)}")


def obtener_modulo_por_id(modulo_id):
    """
    Obtiene un módulo específico por su ID
    """
    try:
        resultados = ejecutar_consulta(
            "SELECT * FROM modulo WHERE idModulo = ?", 
            (modulo_id,)
        )
        return resultados[0] if resultados else None
    except Exception as e:
        raise Exception(f"Error al obtener módulo por ID: {str(e)}")

def actualizar_modulo(modulo_id, data):
    """
    Actualiza un módulo existente
    """
    try:
        data = validar_modulo_data(data, es_actualizacion=True)
        
        # Construir query dinámicamente
        campos = []
        valores = []
        
        campos_posibles = ['nombre', 'descripcion', 'dificultad']
        
        for campo in campos_posibles:
            if campo in data and data[campo] is not None:
                campos.append(f"{campo} = ?")
                valores.append(data[campo])
        
        if not campos:
            raise ValueError("No hay campos válidos para actualizar")
        
        valores.append(modulo_id)
        query = f"UPDATE modulo SET {', '.join(campos)} WHERE idModulo = ?"
        
        ejecutar_consulta(query, valores)
        return True
        
    except Exception as e:
        raise Exception(f"Error al actualizar módulo: {str(e)}")

def eliminar_modulo(modulo_id):
    """
    Elimina un módulo por su ID
    """
    try:
        ejecutar_consulta(
            "DELETE FROM modulo WHERE idModulo = ?", 
            (modulo_id,)
        )
        return True
    except Exception as e:
        raise Exception(f"Error al eliminar módulo: {str(e)}")

def buscar_modulos_por_nombre(nombre_busqueda):
    """
    Busca módulos por nombre
    """
    try:
        return ejecutar_consulta(
            "SELECT * FROM modulo WHERE nombre LIKE ? ORDER BY idModulo DESC",
            (f'%{nombre_busqueda}%',)
        )
    except Exception as e:
        raise Exception(f"Error al buscar módulos: {str(e)}")

def buscar_modulos_por_descripcion(descripcion_busqueda):
    """
    Busca módulos por descripción
    """
    try:
        return ejecutar_consulta(
            "SELECT * FROM modulo WHERE descripcion LIKE ? ORDER BY idModulo DESC",
            (f'%{descripcion_busqueda}%',)
        )
    except Exception as e:
        raise Exception(f"Error al buscar módulos por descripción: {str(e)}")

def contar_modulos_totales():
    """
    Retorna el número total de módulos
    """
    try:
        resultado = ejecutar_consulta("SELECT COUNT(*) as total FROM modulo")
        return resultado[0]['total'] if resultado else 0
    except Exception as e:
        raise Exception(f"Error al contar módulos: {str(e)}")

def obtener_modulos_paginados(pagina=1, por_pagina=10):
    """
    Obtiene módulos con paginación
    """
    try:
        offset = (pagina - 1) * por_pagina
        
        resultados = ejecutar_consulta(
            "SELECT * FROM modulo ORDER BY idModulo DESC LIMIT ? OFFSET ?",
            (por_pagina, offset)
        )
        
        # Obtener el total de módulos
        total_result = ejecutar_consulta("SELECT COUNT(*) as total FROM modulo")
        total = total_result[0]['total'] if total_result else 0
        
        return {
            'datos': resultados,
            'pagina_actual': pagina,
            'por_pagina': por_pagina,
            'total_registros': total,
            'total_paginas': (total + por_pagina - 1) // por_pagina
        }
    except Exception as e:
        raise Exception(f"Error al obtener módulos paginados: {str(e)}")



def obtener_ultimos_modulos(limite=5):
    """
    Obtiene los últimos módulos agregados
    """
    try:
        return ejecutar_consulta(
            "SELECT * FROM modulo ORDER BY idModulo DESC LIMIT ?",
            (limite,)
        )
    except Exception as e:
        raise Exception(f"Error al obtener últimos módulos: {str(e)}")

def obtener_estadisticas_modulos():
    """
    Obtiene estadísticas de los módulos
    """
    try:
        total = contar_modulos_totales()
        ultimos_modulos = obtener_ultimos_modulos(5)
        
        # Estadísticas por longitud de nombre
        por_longitud_nombre = ejecutar_consulta("""
            SELECT 
                CASE 
                    WHEN LENGTH(nombre) < 10 THEN 'Corto (<10)'
                    WHEN LENGTH(nombre) BETWEEN 10 AND 20 THEN 'Medio (10-20)'
                    ELSE 'Largo (>20)'
                END as longitud_nombre,
                COUNT(*) as cantidad
            FROM modulo 
            GROUP BY longitud_nombre
            ORDER BY cantidad DESC
        """)
        
        return {
            'total_modulos': total,
            'ultimos_modulos': ultimos_modulos,
            'por_longitud_nombre': por_longitud_nombre
        }
        
    except Exception as e:
        raise Exception(f"Error al obtener estadísticas: {str(e)}")