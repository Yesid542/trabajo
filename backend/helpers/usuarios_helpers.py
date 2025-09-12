# helpers/usuarios_helpers.py
from .database_helpers import ejecutar_consulta
import re
from werkzeug.security import generate_password_hash, check_password_hash

# Agregar estas funciones si no existen:

def verify_user_credentials(correo, contrasena_plana):
    """
    Verifica las credenciales de un usuario
    """
    try:
        # Buscar usuario por correo
        query = "SELECT * FROM usuarios WHERE correo = ?"
        resultados = ejecutar_consulta(query, [correo])
        
        if resultados and len(resultados) > 0:
            usuario = resultados[0]  # Tomar el primer resultado            

            if check_password_hash(usuario['contrasena'], contrasena_plana):
                return usuario  # Credenciales correctas
        
        return None  # Usuario no existe o contraseña incorrecta
        
    except Exception as e:
        print(f"Error verificando usuario: {e}")
        return None

def get_user_by_email(email):
    """Obtener usuario por email (usa tu database_helpers)"""
    from database_helpers import query_db
    return query_db('SELECT * FROM users WHERE email = ?', [email], one=True)



def validar_correo(correo):
    """Valida que el correo tenga un formato válido"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron, correo):
        raise ValueError("El formato del correo electrónico no es válido")
    return correo.lower()

def validar_usuario_data(data, es_actualizacion=False):
    """
    Valida los datos de un usuario
    """
    campos_requeridos = ['nombre', 'apellido', 'correo', 'contrasena', 
                        'tipoDocumento', 'numeroDocumento']
    
    if not es_actualizacion:
        for campo in campos_requeridos:
            if campo not in data or not data[campo]:
                raise ValueError(f"El campo '{campo}' es requerido")
    
    # Validaciones específicas
    if 'nombre' in data and data['nombre']:
        if len(data['nombre'].strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
    
    if 'apellido' in data and data['apellido']:
        if len(data['apellido'].strip()) < 2:
            raise ValueError("El apellido debe tener al menos 2 caracteres")
    
    if 'correo' in data and data['correo']:
        data['correo'] = validar_correo(data['correo'])
    
    if 'contrasena' in data and data['contrasena']:
        if len(data['contrasena']) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
    
    if 'tipoDocumento' in data and data['tipoDocumento']:
        tipos_validos = ['CC', 'TI', 'CE', 'PASAPORTE']
        if data['tipoDocumento'].upper() not in tipos_validos:
            raise ValueError("Tipo de documento no válido. Use: CC, TI, CE, PASAPORTE")
    
    if 'numeroDocumento' in data and data['numeroDocumento']:
        if not data['numeroDocumento'].strip().isdigit():
            raise ValueError("El número de documento debe contener solo dígitos")
    
    return data

def crear_usuario(data):
    try:
        data = validar_usuario_data(data)
        
        # 🔐 GENERAR HASH DE LA CONTRASEÑA (ANTES de guardar)
        contrasena_hash = generate_password_hash(data['contrasena'])
        
        query = """
            INSERT INTO usuarios 
            (idFicha, nombre, apellido, correo, contrasena, tipoDocumento, numeroDocumento) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        nuevo_id = ejecutar_consulta(
            query,
            (
                data.get('idFicha'),
                data['nombre'].strip(),
                data['apellido'].strip(),
                data['correo'],
                contrasena_hash,  # ✅ Ahora guardamos el HASH, no el texto plano
                data['tipoDocumento'].upper(),
                data['numeroDocumento'].strip()
            )
        )
        
        return nuevo_id
    except Exception as e:
        print(f"Error creando el usuario: {e}")
        return None


def obtener_todos_usuarios():
    """
    Obtiene todos los usuarios de la base de datos
    """
    try:
        return ejecutar_consulta("""
            SELECT u.*, f.ficha as ficha_nombre 
            FROM usuarios u 
            LEFT JOIN ficha f ON u.idFicha = f.idFicha 
            ORDER BY u.idUsuarios DESC
        """)
    except Exception as e:
        raise Exception(f"Error al obtener usuarios: {str(e)}")

def obtener_usuario_por_id(usuario_id):
    """
    Obtiene un usuario específico por su ID
    """
    try:
        resultados = ejecutar_consulta("""
            SELECT u.*, f.ficha as ficha_nombre 
            FROM usuarios u 
            LEFT JOIN ficha f ON u.idFicha = f.idFicha 
            WHERE u.idUsuarios = ?
        """, (usuario_id,))
        
        return resultados[0] if resultados else None
    except Exception as e:
        raise Exception(f"Error al obtener usuario por ID: {str(e)}")

def obtener_usuario_por_documento(tipo_documento, numero_documento):
    """
    Obtiene un usuario por tipo y número de documento
    """
    try:
        resultados = ejecutar_consulta(
            "SELECT * FROM usuarios WHERE tipoDocumento = ? AND numeroDocumento = ?",
            (tipo_documento.upper(), numero_documento.strip())
        )
        return resultados[0] if resultados else None
    except Exception as e:
        raise Exception(f"Error al obtener usuario por documento: {str(e)}")

def actualizar_usuario(usuario_id, data):
    """
    Actualiza un usuario existente
    """
    try:
        data = validar_usuario_data(data, es_actualizacion=True)
        
        # Construir query dinámicamente
        campos = []
        valores = []
        
        for campo in ['idFicha', 'nombre', 'apellido', 'correo', 'contrasena', 
                     'tipoDocumento', 'numeroDocumento']:
            if campo in data and data[campo] is not None:
                campos.append(f"{campo} = ?")
                if campo in ['nombre', 'apellido', 'numeroDocumento']:
                    valores.append(data[campo].strip())
                elif campo == 'tipoDocumento':
                    valores.append(data[campo].upper())
                elif campo == 'correo':
                    valores.append(validar_correo(data[campo]))
                else:
                    valores.append(data[campo])
        
        if not campos:
            raise ValueError("No hay campos válidos para actualizar")
        
        valores.append(usuario_id)
        query = f"UPDATE usuarios SET {', '.join(campos)} WHERE idUsuarios = ?"
        
        ejecutar_consulta(query, valores)
        return True
        
    except Exception as e:
        raise Exception(f"Error al actualizar usuario: {str(e)}")

def eliminar_usuario(usuario_id):
    """
    Elimina un usuario por su ID
    """
    try:
        ejecutar_consulta("DELETE FROM usuarios WHERE idUsuarios = ?", (usuario_id,))
        return True
    except Exception as e:
        raise Exception(f"Error al eliminar usuario: {str(e)}")

def obtener_usuarios_por_ficha(ficha_id):
    """
    Obtiene todos los usuarios asociados a una ficha específica
    """
    try:
        return ejecutar_consulta("""
            SELECT u.*, f.ficha as ficha_nombre 
            FROM usuarios u 
            LEFT JOIN ficha f ON u.idFicha = f.idFicha 
            WHERE u.idFicha = ? 
            ORDER BY u.nombre, u.apellido
        """, (ficha_id,))
    except Exception as e:
        raise Exception(f"Error al obtener usuarios por ficha: {str(e)}")

def buscar_usuarios_por_nombre(nombre):
    """
    Busca usuarios por nombre o apellido
    """
    try:
        return ejecutar_consulta("""
            SELECT u.*, f.ficha as ficha_nombre 
            FROM usuarios u 
            LEFT JOIN ficha f ON u.idFicha = f.idFicha 
            WHERE u.nombre LIKE ? OR u.apellido LIKE ? 
            ORDER BY u.nombre, u.apellido
        """, (f'%{nombre}%', f'%{nombre}%'))
    except Exception as e:
        raise Exception(f"Error al buscar usuarios: {str(e)}")