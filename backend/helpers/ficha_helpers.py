# helpers/ficha_helpers.py
from .database_helpers import ejecutar_consulta

def obtener_todas_fichas():
    """
    Obtiene todas las fichas de la base de datos
    Retorna: Lista de diccionarios con todas las fichas
    """
    try:
        return ejecutar_consulta("SELECT * FROM ficha ORDER BY idFicha DESC")
    except Exception as e:
        raise Exception(f"Error al obtener fichas: {str(e)}")

def crear_ficha(ficha_texto):
    """
    Crea una nueva ficha en la base de datos
    Parámetros: ficha_texto (str) - El texto de la ficha
    Retorna: ID de la nueva ficha creada
    """
    try:
        # Validar que el texto no esté vacío
        if not ficha_texto or not ficha_texto.strip():
            raise ValueError("El texto de la ficha no puede estar vacío")
        
        # Ejecutar la inserción
        nuevo_id = ejecutar_consulta(
            "INSERT INTO ficha (ficha) VALUES (?)", 
            (ficha_texto.strip(),)
        )
        return nuevo_id
        
    except ValueError as e:
        raise e  # Re-lanzar errores de validación
    except Exception as e:
        raise Exception(f"Error al crear ficha: {str(e)}")

def obtener_ficha_por_id(ficha_id):
    """
    Obtiene una ficha específica por su ID
    Parámetros: ficha_id (int) - ID de la ficha a buscar
    Retorna: Diccionario con los datos de la ficha o None si no existe
    """
    try:
        resultados = ejecutar_consulta(
            "SELECT * FROM ficha WHERE idFicha = ?", 
            (ficha_id,)
        )
        return resultados[0] if resultados else None
        
    except Exception as e:
        raise Exception(f"Error al obtener ficha por ID: {str(e)}")

def actualizar_ficha(ficha_id, nuevo_texto):
    """
    Actualiza el texto de una ficha existente
    Parámetros: ficha_id (int), nuevo_texto (str)
    Retorna: True si se actualizó correctamente
    """
    try:
        # Validar el nuevo texto
        if not nuevo_texto or not nuevo_texto.strip():
            raise ValueError("El nuevo texto no puede estar vacío")
        
        ejecutar_consulta(
            "UPDATE ficha SET ficha = ? WHERE idFicha = ?", 
            (nuevo_texto.strip(), ficha_id)
        )
        return True
        
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar ficha: {str(e)}")

def eliminar_ficha(ficha_id):
    """
    Elimina una ficha de la base de datos
    Parámetros: ficha_id (int) - ID de la ficha a eliminar
    Retorna: True si se eliminó correctamente
    """
    try:
        ejecutar_consulta(
            "DELETE FROM ficha WHERE idFicha = ?", 
            (ficha_id,)
        )
        return True
        
    except Exception as e:
        raise Exception(f"Error al eliminar ficha: {str(e)}")

def buscar_fichas_por_texto(texto_busqueda):
    """
    Busca fichas que contengan cierto texto
    Parámetros: texto_busqueda (str) - Texto a buscar
    Retorna: Lista de fichas que coinciden con la búsqueda
    """
    try:
        return ejecutar_consulta(
            "SELECT * FROM ficha WHERE ficha LIKE ? ORDER BY idFicha DESC", 
            (f'%{texto_busqueda}%',)
        )
    except Exception as e:
        raise Exception(f"Error al buscar fichas: {str(e)}")