# helpers/modifica_helpers.py
from datetime import datetime
from .database_helpers import ejecutar_consulta

from datetime import datetime

def validar_modificacion_data(data):
    """
    Valida los datos de modificación
    """
    campos_requeridos = ['idUsuarios', 'idBiblioteca']
    
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None:
            raise ValueError(f"El campo '{campo}' es requerido")
    
    # Validaciones específicas
    if 'idUsuarios' in data:
        try:
            data['idUsuarios'] = int(data['idUsuarios'])
        except (ValueError, TypeError):
            raise ValueError("El ID de usuario debe ser un número entero")
    
    if 'idBiblioteca' in data:
        try:
            data['idBiblioteca'] = int(data['idBiblioteca'])
        except (ValueError, TypeError):
            raise ValueError("El ID de biblioteca debe ser un número entero")
    
    return data

def crear_modificacion(data):
    """
    Crea un nuevo registro de modificación
    """
    try:
        # Validar datos
        data = validar_modificacion_data(data)
        
        # Obtener fecha y hora actual
        fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insertar el registro de modificación
        query = '''
            INSERT INTO modifica (idUsuarios, idBiblioteca, fechaHora)
            VALUES (?, ?, ?)
        '''
        
        params = (
            data['idUsuarios'],
            data['idBiblioteca'],
            fecha_hora_actual
        )
        
        # ejecutar_consulta devuelve el lastrowid directamente (entero)
        ultimo_id = ejecutar_consulta(query, params)
        return ultimo_id
        
    except Exception as e:
        if "FOREIGN KEY constraint failed" in str(e):
            raise ValueError("Error de integridad: Verifique que el usuario y el recurso de biblioteca existan")
        raise Exception(f"Error al crear modificación: {str(e)}")

def obtener_modificaciones():
    """
    Obtiene todos los registros de modificación con información relacionada
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT m.idModifica, m.idUsuarios, m.idBiblioteca, m.fechaHora,
                   u.nombre as usuario_nombre,
                   b.titulo as biblioteca_titulo
            FROM modifica m
            LEFT JOIN usuarios u ON m.idUsuarios = u.idUsuarios
            LEFT JOIN biblioteca b ON m.idBiblioteca = b.idBiblioteca
            ORDER BY m.fechaHora DESC
        ''')
        
        return resultados
        
    except Exception as e:
        raise Exception(f"Error al obtener modificaciones: {str(e)}")

def obtener_modificaciones_por_usuario(id_usuario):
    """
    Obtiene todas las modificaciones realizadas por un usuario específico
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT m.idModifica, m.idUsuarios, m.idBiblioteca, m.fechaHora,
                   u.nombre as usuario_nombre,
                   b.titulo as biblioteca_titulo
            FROM modifica m
            LEFT JOIN usuarios u ON m.idUsuarios = u.idUsuarios
            LEFT JOIN biblioteca b ON m.idBiblioteca = b.idBiblioteca
            WHERE m.idUsuarios = ?
            ORDER BY m.fechaHora DESC
        ''', (id_usuario,))
        
        return resultados
        
    except Exception as e:
        raise Exception(f"Error al obtener modificaciones del usuario: {str(e)}")

def obtener_modificacion_por_id(id_modifica):
    """
    Obtiene una modificación específica por su ID
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT m.idModifica, m.idUsuarios, m.idBiblioteca, m.fechaHora,
                   u.nombre as usuario_nombre,
                   b.titulo as biblioteca_titulo
            FROM modifica m
            LEFT JOIN usuarios u ON m.idUsuarios = u.idUsuarios
            LEFT JOIN biblioteca b ON m.idBiblioteca = b.idBiblioteca
            WHERE m.idModifica = ?
        ''', (id_modifica,))
        
        return resultados[0] if resultados else None
        
    except Exception as e:
        raise Exception(f"Error al obtener modificación: {str(e)}")


def obtener_modificaciones_por_biblioteca(id_biblioteca):
    """
    Obtiene todas las modificaciones realizadas a un recurso específico de biblioteca
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT m.idModifica, m.idUsuarios, m.idBiblioteca, m.fechaHora,
                   u.nombre as usuario_nombre,
                   b.titulo as biblioteca_titulo
            FROM modifica m
            LEFT JOIN usuarios u ON m.idUsuarios = u.idUsuarios
            LEFT JOIN biblioteca b ON m.idBiblioteca = b.idBiblioteca
            WHERE m.idBiblioteca = ?
            ORDER BY m.fechaHora DESC
        ''', (id_biblioteca,))
        
        return resultados
        
    except Exception as e:
        raise Exception(f"Error al obtener modificaciones del recurso: {str(e)}")

def obtener_ultima_modificacion_biblioteca(id_biblioteca):
    """
    Obtiene la última modificación realizada a un recurso de biblioteca
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT m.idModifica, m.idUsuarios, m.idBiblioteca, m.fechaHora,
                   u.nombre as usuario_nombre,
                   b.titulo as biblioteca_titulo
            FROM modifica m
            LEFT JOIN usuarios u ON m.idUsuarios = u.idUsuarios
            LEFT JOIN biblioteca b ON m.idBiblioteca = b.idBiblioteca
            WHERE m.idBiblioteca = ?
            ORDER BY m.fechaHora DESC
            LIMIT 1
        ''', (id_biblioteca,))
        
        return resultados[0] if resultados else None
        
    except Exception as e:
        raise Exception(f"Error al obtener última modificación: {str(e)}")

def obtener_historial_modificaciones():
    """
    Obtiene el historial completo de modificaciones con información detallada
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT m.idModifica, m.idUsuarios, m.idBiblioteca, m.fechaHora,
                   u.nombre as usuario_nombre, u.email as usuario_email,
                   b.titulo as biblioteca_titulo, b.descripcion as biblioteca_descripcion
            FROM modifica m
            LEFT JOIN usuarios u ON m.idUsuarios = u.idUsuarios
            LEFT JOIN biblioteca b ON m.idBiblioteca = b.idBiblioteca
            ORDER BY m.fechaHora DESC
        ''')
        
        return resultados
        
    except Exception as e:
        raise Exception(f"Error al obtener historial: {str(e)}")

def eliminar_modificacion(id_modifica):
    """
    Elimina un registro de modificación
    """
    try:
        # ejecutar_consulta devuelve el número de filas afectadas (entero)
        filas_afectadas = ejecutar_consulta(
            'DELETE FROM modifica WHERE idModifica = ?', 
            (id_modifica,)
        )
        
        return filas_afectadas > 0
        
    except Exception as e:
        raise Exception(f"Error al eliminar modificación: {str(e)}")

def contar_modificaciones_por_usuario(id_usuario):
    """
    Cuenta el total de modificaciones realizadas por un usuario
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT COUNT(*) as total
            FROM modifica
            WHERE idUsuarios = ?
        ''', (id_usuario,))
        
        return resultados[0]['total'] if resultados else 0
        
    except Exception as e:
        raise Exception(f"Error al contar modificaciones: {str(e)}")

def obtener_modificaciones_rango_fechas(fecha_inicio, fecha_fin):
    """
    Obtiene modificaciones dentro de un rango de fechas
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT m.idModifica, m.idUsuarios, m.idBiblioteca, m.fechaHora,
                   u.nombre as usuario_nombre,
                   b.titulo as biblioteca_titulo
            FROM modifica m
            LEFT JOIN usuarios u ON m.idUsuarios = u.idUsuarios
            LEFT JOIN biblioteca b ON m.idBiblioteca = b.idBiblioteca
            WHERE m.fechaHora BETWEEN ? AND ?
            ORDER BY m.fechaHora DESC
        ''', (fecha_inicio, fecha_fin))
        
        return resultados
        
    except Exception as e:
        raise Exception(f"Error al obtener modificaciones por rango de fechas: {str(e)}")

def obtener_usuarios_mas_activos(limite=10):
    """
    Obtiene los usuarios más activos (con más modificaciones)
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT u.idUsuarios, u.nombre, u.email,
                   COUNT(m.idModifica) as total_modificaciones
            FROM usuarios u
            LEFT JOIN modifica m ON u.idUsuarios = m.idUsuarios
            GROUP BY u.idUsuarios, u.nombre, u.email
            ORDER BY total_modificaciones DESC
            LIMIT ?
        ''', (limite,))
        
        return resultados
        
    except Exception as e:
        raise Exception(f"Error al obtener usuarios más activos: {str(e)}")

def obtener_recursos_mas_modificados(limite=10):
    """
    Obtiene los recursos más modificados
    """
    try:
        resultados = ejecutar_consulta('''
            SELECT b.idBiblioteca, b.titulo, b.descripcion,
                   COUNT(m.idModifica) as total_modificaciones
            FROM biblioteca b
            LEFT JOIN modifica m ON b.idBiblioteca = m.idBiblioteca
            GROUP BY b.idBiblioteca, b.titulo, b.descripcion
            ORDER BY total_modificaciones DESC
            LIMIT ?
        ''', (limite,))
        
        return resultados
        
    except Exception as e:
        raise Exception(f"Error al obtener recursos más modificados: {str(e)}")

def obtener_estadisticas_modificaciones():
    """
    Obtiene estadísticas generales de modificaciones
    """
    try:
        total_modificaciones = ejecutar_consulta('SELECT COUNT(*) as total FROM modifica')
        usuarios_activos = ejecutar_consulta('SELECT COUNT(DISTINCT idUsuarios) as total FROM modifica')
        recursos_modificados = ejecutar_consulta('SELECT COUNT(DISTINCT idBiblioteca) as total FROM modifica')
        
        return {
            'total_modificaciones': total_modificaciones[0]['total'] if total_modificaciones else 0,
            'usuarios_activos': usuarios_activos[0]['total'] if usuarios_activos else 0,
            'recursos_modificados': recursos_modificados[0]['total'] if recursos_modificados else 0
        }
        
    except Exception as e:
        raise Exception(f"Error al obtener estadísticas: {str(e)}")