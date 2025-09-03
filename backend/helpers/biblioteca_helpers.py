# helpers/biblioteca_helpers.py
from .database_helpers import ejecutar_consulta
def crear_recurso_biblioteca(data):
    try:
        # Validar campos obligatorios
        campos_obligatorios = ['titulo', 'descripcion']
        
        for campo in campos_obligatorios:
            if campo not in data or not data[campo]:
                raise ValueError(f"El campo '{campo}' es obligatorio")
        
        # Insertar el recurso
        query = '''
            INSERT INTO biblioteca (titulo, descripcion)
            VALUES (?, ?)
        '''
        
        params = (
            data['titulo'],
            data['descripcion']        
        )
        
        # ejecutar_consulta devuelve el lastrowid directamente (entero)
        ultimo_id = ejecutar_consulta(query, params)
        
        # Devuelve el ID directamente (ya es un entero)
        return ultimo_id
        
    except Exception as e:
        raise ValueError(f"Error al crear recurso: {str(e)}")

def obtener_recursos_biblioteca():
    """
    Obtiene todos los recursos de la biblioteca
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT idBiblioteca, titulo, descripcion
            FROM biblioteca
            ORDER BY idBiblioteca
        ''')
        
        return resultados
        
    except Exception as e:
        raise Exception(f"Error al obtener recursos: {str(e)}")

def obtener_recurso_biblioteca_por_id(id_biblioteca):
    """
    Obtiene un recurso específico por su ID
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT idBiblioteca, titulo, descripcion
            FROM biblioteca 
            WHERE idBiblioteca = ?
        ''', (id_biblioteca,))
        
        return resultados[0] if resultados else None
        
    except Exception as e:
        raise Exception(f"Error al obtener recurso: {str(e)}")

def buscar_recursos_biblioteca(termino_busqueda):
    """
    Busca recursos en la biblioteca por título o descripción
    """
    try:
        termino = f"%{termino_busqueda}%"
        resultados = ejecutar_consulta('''
            SELECT idBiblioteca, titulo, descripcion
            FROM biblioteca 
            WHERE titulo LIKE ? OR descripcion LIKE ?
            ORDER BY titulo
        ''', (termino, termino))
        
        return resultados
        
    except Exception as e:
        raise Exception(f"Error en la búsqueda: {str(e)}")

def actualizar_recurso_biblioteca(id_biblioteca, data):
    """
    Actualiza un recurso existente en la biblioteca
    """
    try:
        # Validar que el recurso exista
        recurso_existente = obtener_recurso_biblioteca_por_id(id_biblioteca)
        if not recurso_existente:
            raise ValueError("El recurso no existe")
        
        # Validar que haya campos para actualizar
        campos_validos = ['titulo', 'descripcion']
        campos_actualizar = [campo for campo in campos_validos if campo in data and data[campo] is not None]
        
        if not campos_actualizar:
            raise ValueError("No se proporcionaron campos válidos para actualizar")
        
        # Construir la consulta dinámicamente
        set_clause = ", ".join([f"{campo} = ?" for campo in campos_actualizar])
        valores = [data[campo] for campo in campos_actualizar]
        valores.append(id_biblioteca)
        
        query = f"UPDATE biblioteca SET {set_clause} WHERE idBiblioteca = ?"
        
        # ejecutar_consulta devuelve el número de filas afectadas (entero)
        filas_afectadas = ejecutar_consulta(query, valores)
        return filas_afectadas > 0
        
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar recurso: {str(e)}")

def eliminar_recurso_biblioteca(id_biblioteca):
    """
    Elimina un recurso de la biblioteca
    """
    try:
        # Verificar que el recurso existe antes de eliminar
        recurso_existente = obtener_recurso_biblioteca_por_id(id_biblioteca)
        if not recurso_existente:
            return False  # O raise ValueError según prefieras
        
        # ejecutar_consulta devuelve el número de filas afectadas (entero)
        filas_afectadas = ejecutar_consulta(
            'DELETE FROM biblioteca WHERE idBiblioteca = ?', 
            (id_biblioteca,)
        )
        
        # Si ya verificamos que existe, debería ser > 0
        return True
        
    except Exception as e:
        raise Exception(f"Error al eliminar recurso: {str(e)}")
        
def contar_recursos_biblioteca():
    """
    Cuenta el total de recursos en la biblioteca
    """
    try:
        resultados = ejecutar_consulta('SELECT COUNT(*) as total FROM biblioteca')
        return resultados[0]['total'] if resultados else 0
        
    except Exception as e:
        raise Exception(f"Error al contar recursos: {str(e)}")

def obtener_recursos_recientes(limite=10):
    """
    Obtiene los recursos más recientes
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT idBiblioteca, titulo, descripcion
            FROM biblioteca 
            ORDER BY idBiblioteca DESC 
            LIMIT ?
        ''', (limite,))
        
        return resultados
        
    except Exception as e:
        raise Exception(f"Error al obtener recursos recientes: {str(e)}")

def validar_recurso_biblioteca(data, es_actualizacion=False):
    """
    Valida los datos del recurso de biblioteca
    """
    if not es_actualizacion:
        campos_requeridos = ['titulo', 'descripcion']
        for campo in campos_requeridos:
            if campo not in data or not data[campo]:
                raise ValueError(f"El campo '{campo}' es requerido")
    
    # Validaciones específicas
    if 'titulo' in data and data['titulo']:
        titulo = data['titulo'].strip()
        if len(titulo) < 2:
            raise ValueError("El título debe tener al menos 2 caracteres")
        data['titulo'] = titulo
    
    if 'descripcion' in data and data['descripcion']:
        descripcion = data['descripcion'].strip()
        if len(descripcion) < 10:
            raise ValueError("La descripción debe tener al menos 10 caracteres")
        data['descripcion'] = descripcion
    
    return data