# helpers/contenido_helpers.py
from .database_helpers import ejecutar_consulta

def validar_contenido_data(data, es_actualizacion=False):
    """
    Valida los datos del contenido
    """
    campos_requeridos = ['idModulo','nombre','avance']
    
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
    
    
    if 'avance' in data and data['avance'] is not None:
        try:
            avance = float(data['avance'])
            if avance < 0 or avance > 100:
                raise ValueError("El avance debe estar entre 0 y 100")
            data['avance'] = avance
        except (ValueError, TypeError):
            raise ValueError("El avance debe ser un número válido")
    
    if 'idModulo' in data and data['idModulo'] is not None:
        try:
            data['idModulo'] = int(data['idModulo'])
        except (ValueError, TypeError):
            raise ValueError("El ID de contenido debe ser un número entero")
    
    return data

def crear_contenido(data):
    """
    Crea un nuevo contenido en la base de datos
    """
    try:
        data = validar_contenido_data(data)
        
        query = """
            INSERT INTO contenido 
            (idModulo,nombre, avance) 
            VALUES (?, ?, ?)
        """
        
        ejecutar_consulta(
            query,
            (
                data['idModulo'],
                data['nombre'],
                data['avance']
            )
        )
        
        return data['idModulo']
        
    except Exception as e:
        raise Exception(f"Error al crear contenido: {str(e)}")

def obtener_todos_contenidos():
    """
    Obtiene todos los contenidos de la base de datos
    """
    try:
        return ejecutar_consulta("""
            SELECT * FROM contenido 
            ORDER BY idContenido DESC
        """)
    except Exception as e:
        raise Exception(f"Error al obtener contenidos: {str(e)}")

def obtener_contenido_por_id(contenido_id):
    """
    Obtiene un contenido específico por su ID
    """
    try:
        resultados = ejecutar_consulta(
            "SELECT * FROM contenido WHERE idContenido = ?", 
            (contenido_id,)
        )
        return resultados[0] if resultados else None
    except Exception as e:
        raise Exception(f"Error al obtener contenido por ID: {str(e)}")

def obtener_contenidos_por_avance(min_avance=None, max_avance=None):
    """
    Obtiene contenidos filtrados por rango de avance
    """
    try:
        query = "SELECT * FROM contenido WHERE 1=1"
        params = []
        
        if min_avance is not None:
            query += " AND avance >= ?"
            params.append(float(min_avance))
        
        if max_avance is not None:
            query += " AND avance <= ?"
            params.append(float(max_avance))
        
        query += " ORDER BY avance DESC"
        
        return ejecutar_consulta(query, params)
    except Exception as e:
        raise Exception(f"Error al obtener contenidos por avance: {str(e)}")

def actualizar_contenido(contenido_id, data):
    """
    Actualiza un contenido existente
    """
    try:
        data = validar_contenido_data(data, es_actualizacion=True)
        
        # Construir query dinámicamente
        campos = []
        valores = []
        
        campos_posibles = ['nombre', 'avance']
        
        for campo in campos_posibles:
            if campo in data and data[campo] is not None:
                campos.append(f"{campo} = ?")
                valores.append(data[campo])
        
        if not campos:
            raise ValueError("No hay campos válidos para actualizar")
        
        valores.append(contenido_id)
        query = f"UPDATE contenido SET {', '.join(campos)} WHERE idContenido = ?"
        
        ejecutar_consulta(query, valores)
        return True
        
    except Exception as e:
        raise Exception(f"Error al actualizar contenido: {str(e)}")

def actualizar_avance_contenido(contenido_id, nuevo_avance):
    """
    Actualiza solo el avance de un contenido
    """
    try:
        # Validar avance
        try:
            avance = float(nuevo_avance)
            if avance < 0 or avance > 100:
                raise ValueError("El avance debe estar entre 0 y 100")
        except (ValueError, TypeError):
            raise ValueError("El avance debe ser un número válido")
        
        ejecutar_consulta(
            "UPDATE contenido SET avance = ? WHERE idContenido = ?",
            (avance, contenido_id)
        )
        return True
        
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar avance: {str(e)}")

def eliminar_contenido(contenido_id):
    """
    Elimina un contenido por su ID
    """
    try:
        ejecutar_consulta(
            "DELETE FROM contenido WHERE idContenido = ?", 
            (contenido_id,)
        )
        return True
    except Exception as e:
        raise Exception(f"Error al eliminar contenido: {str(e)}")

def buscar_contenidos_por_nombre(nombre_busqueda):
    """
    Busca contenidos por nombre
    """
    try:
        return ejecutar_consulta(
            "SELECT * FROM contenido WHERE nombre LIKE ? ORDER BY idContenido DESC",
            (f'%{nombre_busqueda}%',)
        )
    except Exception as e:
        raise Exception(f"Error al buscar contenidos: {str(e)}")

def obtener_contenidos_completados():
    """
    Obtiene contenidos con avance del 100%
    """
    try:
        return ejecutar_consulta(
            "SELECT * FROM contenido WHERE avance = 100 ORDER BY idContenido DESC"
        )
    except Exception as e:
        raise Exception(f"Error al obtener contenidos completados: {str(e)}")

def obtener_contenidos_pendientes():
    """
    Obtiene contenidos con avance menor al 100%
    """
    try:
        return ejecutar_consulta(
            "SELECT * FROM contenido WHERE avance < 100 ORDER BY avance DESC"
        )
    except Exception as e:
        raise Exception(f"Error al obtener contenidos pendientes: {str(e)}")

def obtener_promedio_avance():
    """
    Calcula el promedio de avance de todos los contenidos
    """
    try:
        resultado = ejecutar_consulta("SELECT AVG(avance) as promedio FROM contenido")
        return resultado[0]['promedio'] or 0
    except Exception as e:
        raise Exception(f"Error al calcular promedio de avance: {str(e)}")
