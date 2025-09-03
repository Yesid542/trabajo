# helpers/evaluacion_helpers.py
from .database_helpers import ejecutar_consulta

def validar_evaluacion_data(data, es_actualizacion=False):
    """
    Valida los datos de una evaluación
    """
    campos_requeridos = [
        'idModulo','descripcionPregunta', 'opcionA', 'opcionB', 
        'opcionC', 'opcionD', 'respuesta'
    ]
    
    if not es_actualizacion:
        for campo in campos_requeridos:
            if campo not in data or not data[campo]:
                raise ValueError(f"El campo '{campo}' es requerido")
    
    # Validaciones específicas
    if 'descripcionPregunta' in data and data['descripcionPregunta']:
        if len(data['descripcionPregunta'].strip()) < 5:
            raise ValueError("La descripción de la pregunta debe tener al menos 5 caracteres")
    
    # Validar que la respuesta sea una de las opciones válidas
    if 'respuesta' in data and data['respuesta']:
        respuesta = data['respuesta'].upper()
        opciones_validas = ['A', 'B', 'C', 'D']
        if respuesta not in opciones_validas:
            raise ValueError("La respuesta debe ser A, B, C o D")
        data['respuesta'] = respuesta  # Normalizar a mayúsculas
    
    # Validar calificación si existe
    if 'calificacion' in data and data['calificacion'] is not None:
        try:
            calificacion = float(data['calificacion'])
            if calificacion < 0 or calificacion > 100:
                raise ValueError("La calificación debe estar entre 0 y 100")
            data['calificacion'] = calificacion
        except (ValueError, TypeError):
            raise ValueError("La calificación debe ser un número válido")
    
    return data

def crear_evaluacion(data):
    """
    Crea una nueva evaluación en la base de datos
    """
    try:
        data = validar_evaluacion_data(data)
        
        query = """
            INSERT INTO evaluacion 
            (idModulo,descripcionPregunta, opcionA, opcionB, opcionC, opcionD, 
             respuesta,calificacion) 
            VALUES (?,?, ?, ?, ?, ?, ?, ?)
        """
        
        nuevo_id = ejecutar_consulta(
            query,
            (
                data['idModulo'],
                data['descripcionPregunta'].strip(),
                data['opcionA'].strip(),
                data['opcionB'].strip(),
                data['opcionC'].strip(),
                data['opcionD'].strip(),
                data['respuesta'],
                data.get('calificacion')
            )
        )
        
        return nuevo_id
        
    except Exception as e:
        raise Exception(f"Error al crear evaluación: {str(e)}")

def obtener_todas_evaluaciones():
    """
    Obtiene todas las evaluaciones de la base de datos
    """
    try:
        return ejecutar_consulta("""
            SELECT * FROM evaluacion 
            ORDER BY idEvaluacion DESC
        """)
    except Exception as e:
        raise Exception(f"Error al obtener evaluaciones: {str(e)}")

def obtener_evaluacion_por_id(evaluacion_id):
    """
    Obtiene una evaluación específica por su ID
    """
    try:
        resultados = ejecutar_consulta(
            "SELECT * FROM evaluacion WHERE idEvaluacion = ?", 
            (evaluacion_id,)
        )
        return resultados[0] if resultados else None
    except Exception as e:
        raise Exception(f"Error al obtener evaluación por ID: {str(e)}")

def actualizar_evaluacion(evaluacion_id, data):
    """
    Actualiza una evaluación existente
    """
    try:
        data = validar_evaluacion_data(data, es_actualizacion=True)
        
        # Construir query dinámicamente
        campos = []
        valores = []
        
        campos_posibles = [
            'descripcionPregunta', 'opcionA', 'opcionB', 'opcionC', 'opcionD',
            'respuesta', 'calificacion'
        ]
        
        for campo in campos_posibles:
            if campo in data and data[campo] is not None:
                campos.append(f"{campo} = ?")
                if campo in ['descripcionPregunta', 'opcionA', 'opcionB', 
                           'opcionC', 'opcionD']:
                    valores.append(data[campo].strip())
                else:
                    valores.append(data[campo])
        
        if not campos:
            raise ValueError("No hay campos válidos para actualizar")
        
        valores.append(evaluacion_id)
        query = f"UPDATE evaluacion SET {', '.join(campos)} WHERE idEvaluacion = ?"
        
        ejecutar_consulta(query, valores)
        return True
        
    except Exception as e:
        raise Exception(f"Error al actualizar evaluación: {str(e)}")

def eliminar_evaluacion(evaluacion_id):
    """
    Elimina una evaluación por su ID
    """
    try:
        ejecutar_consulta(
            "DELETE FROM evaluacion WHERE idEvaluacion = ?", 
            (evaluacion_id,)
        )
        return True
    except Exception as e:
        raise Exception(f"Error al eliminar evaluación: {str(e)}")

def obtener_evaluaciones_por_calificacion(min_calificacion=None, max_calificacion=None):
    """
    Obtiene evaluaciones filtradas por rango de calificación
    """
    try:
        query = "SELECT * FROM evaluacion WHERE calificacion IS NOT NULL"
        params = []
        
        if min_calificacion is not None:
            query += " AND calificacion >= ?"
            params.append(float(min_calificacion))
        
        if max_calificacion is not None:
            query += " AND calificacion <= ?"
            params.append(float(max_calificacion))
        
        query += " ORDER BY calificacion DESC"
        
        return ejecutar_consulta(query, params)
    except Exception as e:
        raise Exception(f"Error al obtener evaluaciones por calificación: {str(e)}")

def buscar_evaluaciones_por_pregunta(texto_busqueda):
    """
    Busca evaluaciones por texto en la pregunta
    """
    try:
        return ejecutar_consulta(
            "SELECT * FROM evaluacion WHERE descripcionPregunta LIKE ? ORDER BY idEvaluacion DESC",
            (f'%{texto_busqueda}%',)
        )
    except Exception as e:
        raise Exception(f"Error al buscar evaluaciones: {str(e)}")

def obtener_evaluaciones_sin_calificar():
    """
    Obtiene evaluaciones que no tienen calificación
    """
    try:
        return ejecutar_consulta(
            "SELECT * FROM evaluacion WHERE calificacion IS NULL ORDER BY idEvaluacion DESC"
        )
    except Exception as e:
        raise Exception(f"Error al obtener evaluaciones sin calificar: {str(e)}")

def actualizar_calificacion(evaluacion_id, calificacion):
    """
    Actualiza solo la calificación de una evaluación
    """
    try:
        if calificacion is not None:
            calificacion = float(calificacion)
            if calificacion < 0 or calificacion > 100:
                raise ValueError("La calificación debe estar entre 0 y 100")
        
        ejecutar_consulta(
            "UPDATE evaluacion SET calificacion = ? WHERE idEvaluacion = ?",
            (calificacion, evaluacion_id)
        )
        return True
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar calificación: {str(e)}")

def obtener_evaluaciones_con_imagen():
    """
    Obtiene evaluaciones que tienen imagen
    """
    try:
        return ejecutar_consulta(
            "SELECT * FROM evaluacion WHERE imagenFirebasePath IS NOT NULL AND imagenFirebasePath != '' ORDER BY idEvaluacion DESC"
        )
    except Exception as e:
        raise Exception(f"Error al obtener evaluaciones con imagen: {str(e)}")

def contar_evaluaciones_totales():
    """
    Retorna el número total de evaluaciones
    """
    try:
        resultado = ejecutar_consulta("SELECT COUNT(*) as total FROM evaluacion")
        return resultado[0]['total'] if resultado else 0
    except Exception as e:
        raise Exception(f"Error al contar evaluaciones: {str(e)}")