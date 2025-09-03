# helpers/desarrollo_helpers.py
from .database_helpers import ejecutar_consulta
from .modulo_helpers import obtener_modulo_por_id
from .usuarios_helpers import obtener_usuario_por_id

def validar_desarrollo_data(data, es_actualizacion=False):
    """
    Valida los datos del desarrollo
    """
    campos_requeridos = ['idModulo', 'idUsuarios', 'avance','fechaHora']
    
    if not es_actualizacion:
        for campo in campos_requeridos:
            if campo not in data or data[campo] is None:
                raise ValueError(f"El campo '{campo}' es requerido")
    
    # Validaciones específicas
    if 'idModulo' in data and data['idModulo'] is not None:
        try:
            data['idModulo'] = int(data['idModulo'])
            # Verificar que el módulo exista
            if not obtener_modulo_por_id(data['idModulo']):
                raise ValueError("El módulo referenciado no existe")
        except (ValueError, TypeError):
            raise ValueError("El ID de módulo debe ser un número entero válido")
    
    if 'idUsuarios' in data and data['idUsuarios'] is not None:
        try:
            data['idUsuarios'] = int(data['idUsuarios'])
            # Verificar que el usuario exista
            if not obtener_usuario_por_id(data['idUsuarios']):
                raise ValueError("El usuario referenciado no existe")
        except (ValueError, TypeError):
            raise ValueError("El ID de usuario debe ser un número entero válido")
    
    if 'avance' in data and data['avance'] is not None:
        try:
            avance = float(data['avance'])
            if avance < 0 or avance > 100:
                raise ValueError("El avance debe estar entre 0 y 100")
            data['avance'] = avance
        except (ValueError, TypeError):
            raise ValueError("El avance debe ser un número válido")
    
    
    return data

def crear_desarrollo(data):
    """
    Crea un nuevo registro de desarrollo en la base de datos
    """
    try:
        # Si no se proporciona idDesarrollo, generar uno automáticamente
        
        query = """
            INSERT INTO desarrollo 
            (idModulo, idUsuarios, avance,fechaHora) 
            VALUES ( ?, ?, ?,?)
        """
        
        ejecutar_consulta(
            query,
            (
                data['idModulo'],
                data['idUsuarios'],
                data['avance'],
                data['fechaHora']
            )
        )
        
        return data['idModulo']
        
    except Exception as e:
        raise Exception(f"Error al crear desarrollo: {str(e)}")

def obtener_todos_desarrollos():
    """
    Obtiene todos los desarrollos con información de las relaciones
    """
    try:
        return ejecutar_consulta("""
            SELECT 
                d.*,
                m.nombre as modulo_nombre,
                m.descripcion as modulo_descripcion,
                u.nombre as usuario_nombre,
                u.apellido as usuario_apellido,
                u.correo as usuario_correo
            FROM desarrollo d
            INNER JOIN modulo m ON d.idModulo = m.idModulo
            INNER JOIN usuarios u ON d.idUsuarios = u.idUsuarios
            ORDER BY d.idDesarrollo DESC
        """)
    except Exception as e:
        raise Exception(f"Error al obtener desarrollos: {str(e)}")

def obtener_desarrollo_por_id(desarrollo_id):
    """
    Obtiene un desarrollo específico por su ID con información completa
    """
    try:
        resultados = ejecutar_consulta("""
            SELECT 
                d.*,
                m.nombre as modulo_nombre,
                m.descripcion as modulo_descripcion,
                m.logroFirebasePath,
                u.nombre as usuario_nombre,
                u.apellido as usuario_apellido,
                u.correo as usuario_correo,
                u.tipoDocumento,
                u.numeroDocumento
            FROM desarrollo d
            INNER JOIN modulo m ON d.idModulo = m.idModulo
            INNER JOIN usuarios u ON d.idUsuarios = u.idUsuarios
            WHERE d.idDesarrollo = ?
        """, (desarrollo_id,))
        
        return resultados[0] if resultados else None
    except Exception as e:
        raise Exception(f"Error al obtener desarrollo por ID: {str(e)}")

def obtener_desarrollos_por_usuario(usuario_id):
    """
    Obtiene todos los desarrollos de un usuario específico
    """
    try:
        return ejecutar_consulta("""
            SELECT 
                d.*,
                m.nombre as modulo_nombre,
                m.descripcion as modulo_descripcion,
                m.logroFirebasePath
            FROM desarrollo d
            INNER JOIN modulo m ON d.idModulo = m.idModulo
            WHERE d.idUsuarios = ?
            ORDER BY d.idDesarrollo DESC
        """, (usuario_id,))
    except Exception as e:
        raise Exception(f"Error al obtener desarrollos por usuario: {str(e)}")

def obtener_desarrollos_por_modulo(modulo_id):
    """
    Obtiene todos los desarrollos de un módulo específico
    """
    try:
        return ejecutar_consulta("""
            SELECT 
                d.*,
                u.nombre as usuario_nombre,
                u.apellido as usuario_apellido,
                u.correo as usuario_correo
            FROM desarrollo d
            INNER JOIN usuarios u ON d.idUsuarios = u.idUsuarios
            WHERE d.idModulo = ?
            ORDER BY d.avance DESC
        """, (modulo_id,))
    except Exception as e:
        raise Exception(f"Error al obtener desarrollos por módulo: {str(e)}")

def obtener_desarrollo_usuario_modulo(usuario_id, modulo_id):
    """
    Obtiene el desarrollo específico de un usuario en un módulo
    """
    try:
        resultados = ejecutar_consulta("""
            SELECT 
                d.*,
                m.nombre as modulo_nombre,
                u.nombre as usuario_nombre,
                u.apellido as usuario_apellido
            FROM desarrollo d
            INNER JOIN modulo m ON d.idModulo = m.idModulo
            INNER JOIN usuarios u ON d.idUsuarios = u.idUsuarios
            WHERE d.idUsuarios = ? AND d.idModulo = ?
        """, (usuario_id, modulo_id))
        
        return resultados[0] if resultados else None
    except Exception as e:
        raise Exception(f"Error al obtener desarrollo usuario-módulo: {str(e)}")

def actualizar_desarrollo(desarrollo_id, data):
    """
    Actualiza un desarrollo existente
    """
    try:
        data = validar_desarrollo_data(data, es_actualizacion=True)
        
        # Construir query dinámicamente
        campos = []
        valores = []
        
        campos_posibles = ['idModulo', 'idUsuarios', 'avance']
        
        for campo in campos_posibles:
            if campo in data and data[campo] is not None:
                campos.append(f"{campo} = ?")
                valores.append(data[campo])
        
        if not campos:
            raise ValueError("No hay campos válidos para actualizar")
        
        valores.append(desarrollo_id)
        query = f"UPDATE desarrollo SET {', '.join(campos)} WHERE idDesarrollo = ?"
        
        ejecutar_consulta(query, valores)
        return True
        
    except Exception as e:
        raise Exception(f"Error al actualizar desarrollo: {str(e)}")

def actualizar_avance_desarrollo(desarrollo_id, nuevo_avance):
    """
    Actualiza solo el avance de un desarrollo
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
            "UPDATE desarrollo SET avance = ? WHERE idDesarrollo = ?",
            (avance, desarrollo_id)
        )
        return True
        
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar avance: {str(e)}")

def actualizar_avance_usuario_modulo(usuario_id, modulo_id, nuevo_avance):
    """
    Actualiza el avance de un usuario específico en un módulo específico
    """
    try:
        # Validar avance
        try:
            avance = float(nuevo_avance)
            if avance < 0 or avance > 100:
                raise ValueError("El avance debe estar entre 0 y 100")
        except (ValueError, TypeError):
            raise ValueError("El avance debe ser un número válido")
        
        # Verificar si ya existe el desarrollo
        desarrollo_existente = obtener_desarrollo_usuario_modulo(usuario_id, modulo_id)
        
        if desarrollo_existente:
            # Actualizar existente
            ejecutar_consulta(
                "UPDATE desarrollo SET avance = ? WHERE idUsuarios = ? AND idModulo = ?",
                (avance, usuario_id, modulo_id)
            )
        else:
            # Crear nuevo
            crear_desarrollo({
                'idUsuarios': usuario_id,
                'idModulo': modulo_id,
                'avance': avance
            })
        
        return True
        
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar avance usuario-módulo: {str(e)}")

def eliminar_desarrollo(desarrollo_id):
    """
    Elimina un desarrollo por su ID
    """
    try:
        ejecutar_consulta(
            "DELETE FROM desarrollo WHERE idDesarrollo = ?", 
            (desarrollo_id,)
        )
        return True
    except Exception as e:
        raise Exception(f"Error al eliminar desarrollo: {str(e)}")

def eliminar_desarrollo_usuario_modulo(usuario_id, modulo_id):
    """
    Elimina el desarrollo de un usuario específico en un módulo específico
    """
    try:
        ejecutar_consulta(
            "DELETE FROM desarrollo WHERE idUsuarios = ? AND idModulo = ?", 
            (usuario_id, modulo_id)
        )
        return True
    except Exception as e:
        raise Exception(f"Error al eliminar desarrollo usuario-módulo: {str(e)}")

def obtener_avance_promedio_usuario(usuario_id):
    """
    Calcula el avance promedio de un usuario en todos sus módulos
    """
    try:
        resultado = ejecutar_consulta(
            "SELECT AVG(avance) as promedio FROM desarrollo WHERE idUsuarios = ?",
            (usuario_id,)
        )
        return resultado[0]['promedio'] or 0
    except Exception as e:
        raise Exception(f"Error al calcular avance promedio: {str(e)}")

def obtener_avance_promedio_modulo(modulo_id):
    """
    Calcula el avance promedio de un módulo entre todos los usuarios
    """
    try:
        resultado = ejecutar_consulta(
            "SELECT AVG(avance) as promedio FROM desarrollo WHERE idModulo = ?",
            (modulo_id,)
        )
        return resultado[0]['promedio'] or 0
    except Exception as e:
        raise Exception(f"Error al calcular avance promedio módulo: {str(e)}")

def obtener_usuarios_top_avance(limite=10):
    """
    Obtiene los usuarios con mayor avance promedio
    """
    try:
        return ejecutar_consulta("""
            SELECT 
                u.idUsuarios,
                u.nombre,
                u.apellido,
                u.correo,
                AVG(d.avance) as avance_promedio,
                COUNT(d.idDesarrollo) as modulos_asignados
            FROM usuarios u
            LEFT JOIN desarrollo d ON u.idUsuarios = d.idUsuarios
            GROUP BY u.idUsuarios
            ORDER BY avance_promedio DESC
            LIMIT ?
        """, (limite,))
    except Exception as e:
        raise Exception(f"Error al obtener usuarios top: {str(e)}")

def obtener_modulos_top_avance(limite=10):
    """
    Obtiene los módulos con mayor avance promedio
    """
    try:
        return ejecutar_consulta("""
            SELECT 
                m.idModulo,
                m.nombre as modulo_nombre,
                m.descripcion,
                AVG(d.avance) as avance_promedio,
                COUNT(d.idDesarrollo) as usuarios_asignados
            FROM modulo m
            LEFT JOIN desarrollo d ON m.idModulo = d.idModulo
            GROUP BY m.idModulo
            ORDER BY avance_promedio DESC
            LIMIT ?
        """, (limite,))
    except Exception as e:
        raise Exception(f"Error al obtener módulos top: {str(e)}")

def verificar_desarrollo_existente(usuario_id, modulo_id):
    """
    Verifica si ya existe un desarrollo para un usuario y módulo específicos
    """
    try:
        resultados = ejecutar_consulta(
            "SELECT * FROM desarrollo WHERE idUsuarios = ? AND idModulo = ?",
            (usuario_id, modulo_id)
        )
        return resultados[0] if resultados else None
    except Exception as e:
        raise Exception(f"Error al verificar desarrollo existente: {str(e)}")