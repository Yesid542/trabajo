from flask import Flask, session
from flask import Flask, jsonify, request, g
from database import get_db, init_db, close_db
from flask_cors import CORS
from flasgger import Swagger

from helpers import (
    obtener_todas_fichas,
    crear_ficha,
    obtener_ficha_por_id,
    actualizar_ficha,
    eliminar_ficha,
    buscar_fichas_por_texto,
    validar_ficha
)
from helpers import (
    verify_user_credentials,
    get_user_by_email,
    crear_usuario,
    obtener_todos_usuarios,
    obtener_usuario_por_id,
    obtener_usuario_por_documento,
    actualizar_usuario,
    eliminar_usuario,
    obtener_usuarios_por_ficha,
    buscar_usuarios_por_nombre,
    validar_usuario_data,
    validar_correo
)
from helpers import (
    crear_evaluacion,
    obtener_todas_evaluaciones,
    obtener_evaluacion_por_id,
    actualizar_evaluacion,
    eliminar_evaluacion,
    obtener_evaluaciones_por_calificacion,
    buscar_evaluaciones_por_pregunta,
    obtener_evaluaciones_sin_calificar,
    obtener_evaluaciones_con_imagen,
    contar_evaluaciones_totales
)
from helpers import (
    crear_contenido,
    obtener_todos_contenidos,
    obtener_contenido_por_id,
    obtener_contenidos_por_avance,
    actualizar_contenido,
    actualizar_avance_contenido,
    eliminar_contenido,
    buscar_contenidos_por_nombre,
    obtener_contenidos_completados,
    obtener_contenidos_pendientes,
    obtener_promedio_avance,
)
from helpers import (
    crear_modulo,
    obtener_todos_modulos,
    obtener_modulo_por_id,
    actualizar_modulo,
    eliminar_modulo,
    buscar_modulos_por_nombre,
    obtener_estadisticas_modulos
)
from helpers import (
    crear_desarrollo,
    obtener_todos_desarrollos,
    obtener_desarrollo_por_id,
    obtener_desarrollos_por_usuario,
    obtener_desarrollos_por_modulo,
    obtener_desarrollo_usuario_modulo,
    actualizar_desarrollo,
    actualizar_avance_desarrollo,
    actualizar_avance_usuario_modulo,
    eliminar_desarrollo,
    obtener_avance_promedio_usuario,
    obtener_avance_promedio_modulo,
    obtener_usuarios_top_avance,
    obtener_modulos_top_avance,
    verificar_desarrollo_existente
)
from helpers import (
    crear_modulo,
    obtener_todos_modulos,
    obtener_modulo_por_id,
    actualizar_modulo,
    eliminar_modulo,
    buscar_modulos_por_nombre,
    buscar_modulos_por_descripcion,
    obtener_modulos_paginados,
    obtener_ultimos_modulos,
    obtener_estadisticas_modulos
)

from helpers import (
    crear_modificacion,
    obtener_modificaciones,
    obtener_modificaciones_por_usuario,
    obtener_modificacion_por_id,
    obtener_modificaciones_por_biblioteca, 
    obtener_ultima_modificacion_biblioteca,
    obtener_historial_modificaciones, 
    eliminar_modificacion, 
    contar_modificaciones_por_usuario,
    obtener_modificaciones_rango_fechas, 
    obtener_usuarios_mas_activos,
    obtener_recursos_mas_modificados, 
    obtener_estadisticas_modificaciones
)

from helpers import (
    crear_ruta_archivo,
    obtener_rutas_por_referencia,
    obtener_ruta_por_id,
    eliminar_ruta,
    obtener_todas_rutas,
    contar_rutas_por_tabla
)
from helpers import (
    crear_recurso_biblioteca,
    obtener_recursos_biblioteca,
    obtener_recurso_biblioteca_por_id,
    buscar_recursos_biblioteca,
    actualizar_recurso_biblioteca,
    eliminar_recurso_biblioteca,
    contar_recursos_biblioteca,
    obtener_recursos_recientes,
    validar_recurso_biblioteca,
)
from middleware.authMiddleware import login_required, get_current_user


#--------------------------------------------------- Autenticación------------------------------------------------#
app = Flask(__name__)
app.secret_key ='innovemsennovacegafe2025'
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
swagger = Swagger(app)

from flasgger import swag_from

@app.route('/api/auth/login', methods=['POST'])
@swag_from({
    'tags': ['Autenticación'],
    'description': 'Iniciar sesión de usuario',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'correo': {'type': 'string', 'example': 'usuario@ejemplo.com'},
                    'contrasena': {'type': 'string', 'example': 'password123'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login exitoso',
            'examples': {
                'application/json': {'true': True}
            }
        },
        401: {
            'description': 'Credenciales inválidas',
            'examples': {
                'application/json': {'false': False}
            }
        }
    }
})
def login():
    # Tu código existente sin cambios
    from helpers.usuarios_helpers import verify_user_credentials
    
    data = request.get_json()
    user = verify_user_credentials(data['correo'], data['contrasena'])
    
    if user:
        print(user)
        session['user_id'] = user['idUsuarios']
        session['username'] = user['nombre']
        session['email'] = user['correo']
        return jsonify({'true':True})
    else:
        return jsonify({'false': False})

@app.route('/api/auth/logout', methods=['POST'])
@swag_from({
    'tags': ['Autenticación'],
    'description': 'Cerrar sesión del usuario',
    'responses': {
        200: {
            'description': 'Sesión cerrada exitosamente',
            'examples': {
                'application/json': {'message': 'Sesión cerrada'}
            }
        }
    }
})
def logout():
    session.clear()
    return jsonify({'message': 'Sesión cerrada'})

@app.route('/api/auth/check', methods=['GET'])
@swag_from({
    'tags': ['Autenticación'],
    'description': 'Verificar estado de autenticación del usuario',
    'responses': {
        200: {
            'description': 'Estado de autenticación',
            'examples': {
                'application/json': {
                    'authenticated': True,
                    'user': {'id': 1, 'nombre': 'Usuario Ejemplo'}
                }
            }
        }
    }
})
def check_auth():
    user = get_current_user()
    return jsonify({'authenticated': user is not None, 'user': user})

@app.route('/api/perfil', methods=['GET'])
@login_required
@swag_from({
    'tags': ['Usuario'],
    'description': 'Obtener perfil del usuario autenticado',
    'security': [{'session_auth': []}],
    'responses': {
        200: {
            'description': 'Perfil del usuario',
            'examples': {
                'application/json': {
                    'id': 1,
                    'nombre': 'Usuario Ejemplo',
                    'correo': 'usuario@ejemplo.com'
                }
            }
        },
        401: {
            'description': 'No autenticado'
        }
    }
})
def perfil():
    from helpers.usuarios_helpers import get_user_profile
    user_profile = get_user_profile(get_current_user()['id'])
    return jsonify(user_profile)

@app.route("/api/data")
@swag_from({
    'tags': ['General'],
    'description': 'Endpoint de prueba',
    'responses': {
        200: {
            'description': 'Mensaje de prueba',
            'examples': {
                'application/json': {"message": "Hola desde Python!"}
            }
        }
    }
})
def get_data():
    return jsonify({"message": "Hola desde Python!"})

@app.route('/api/fichas/valida/<string:ficha>', methods=['GET'])
@swag_from({
    'tags': ['Fichas'],
    'description': 'Validar si una ficha existe en la base de datos',
    'parameters': [
        {
            'name': 'ficha',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Código de la ficha a validar'
        }
    ],
    'responses': {
        200: {
            'description': 'Ficha válida',
            'examples': {
                'application/json': {'id': 123}
            }
        },
        404: {
            'description': 'Ficha no encontrada',
            'examples': {
                'application/json': False
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def validar_ficha_en_bd(ficha):
    try:
        resultado = validar_ficha(ficha)
        
        if resultado:
            return jsonify({'id':resultado})
        else:
            return jsonify(False)
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/fichas', methods=['GET'])
@swag_from({
    'tags': ['Fichas'],
    'description': 'Obtener todas las fichas',
    'responses': {
        200: {
            'description': 'Lista de fichas',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {'id': 1, 'ficha': 'FICHA001'},
                        {'id': 2, 'ficha': 'FICHA002'}
                    ],
                    'count': 2
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_fichas():
    try:
        fichas = obtener_todas_fichas()
        return jsonify({
            'status': 'success',
            'data': fichas,
            'count': len(fichas)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fichas', methods=['POST'])
@swag_from({
    'tags': ['Fichas'],
    'description': 'Crear una nueva ficha',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'ficha': {
                        'type': 'string',
                        'example': 'NUEVA_FICHA'
                    }
                },
                'required': ['ficha']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Ficha creada exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Ficha creada exitosamente',
                    'id': 123
                }
            }
        },
        400: {
            'description': 'Datos inválidos'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def add_ficha():
    try:
        data = request.get_json()
        
        if not data or 'ficha' not in data:
            return jsonify({'error': 'El campo "ficha" es requerido'}), 400
        
        nuevo_id = crear_ficha(data['ficha'])
        
        return jsonify({
            'status': 'success',
            'message': 'Ficha creada exitosamente',
            'id': nuevo_id
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fichas/buscar', methods=['GET'])
@swag_from({
    'tags': ['Fichas'],
    'description': 'Buscar fichas por texto',
    'parameters': [
        {
            'name': 'q',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Texto de búsqueda'
        }
    ],
    'responses': {
        200: {
            'description': 'Resultados de búsqueda',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {'id': 1, 'ficha': 'FICHA001'},
                        {'id': 2, 'ficha': 'FICHA002'}
                    ],
                    'count': 2
                }
            }
        },
        400: {
            'description': 'Parámetro de búsqueda faltante'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def search_fichas():
    try:
        texto_busqueda = request.args.get('q', '')
        if not texto_busqueda:
            return jsonify({'error': 'Parámetro "q" requerido'}), 400
        
        fichas = buscar_fichas_por_texto(texto_busqueda)
        return jsonify({
            'status': 'success',
            'data': fichas,
            'count': len(fichas)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fichas/<int:ficha_id>', methods=['GET'])
@swag_from({
    'tags': ['Fichas'],
    'description': 'Obtener ficha por ID',
    'parameters': [
        {
            'name': 'ficha_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la ficha'
        }
    ],
    'responses': {
        200: {
            'description': 'Ficha encontrada',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {'id': 1, 'ficha': 'FICHA001'}
                }
            }
        },
        404: {
            'description': 'Ficha no encontrada'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_ficha_por_id(ficha_id):
    try:
        ficha = obtener_ficha_por_id(ficha_id)
        
        if ficha:
            return jsonify({
                'status': 'success',
                'data': ficha
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Ficha con ID {ficha_id} no encontrada'
            }), 404
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/fichas/<int:ficha_id>', methods=['PUT'])
@swag_from({
    'tags': ['Fichas'],
    'description': 'Actualizar ficha existente',
    'parameters': [
        {
            'name': 'ficha_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la ficha a actualizar'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'ficha': {
                        'type': 'string',
                        'example': 'FICHA_ACTUALIZADA'
                    }
                },
                'required': ['ficha']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Ficha actualizada exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Ficha actualizada exitosamente',
                    'data': {'id': 1, 'ficha': 'FICHA_ACTUALIZADA'}
                }
            }
        },
        400: {
            'description': 'Datos inválidos'
        },
        404: {
            'description': 'Ficha no encontrada'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def actualizar_ficha_por_id(ficha_id):
    try:
        data = request.get_json()
        
        if not data or 'ficha' not in data:
            return jsonify({
                'status': 'error',
                'message': 'El campo "ficha" es requerido en el cuerpo de la solicitud'
            }), 400
        
        if not data['ficha'] or not data['ficha'].strip():
            return jsonify({
                'status': 'error',
                'message': 'El campo "ficha" no puede estar vacío'
            }), 400
        
        ficha_existente = obtener_ficha_por_id(ficha_id)
        if not ficha_existente:
            return jsonify({
                'status': 'error',
                'message': f'Ficha con ID {ficha_id} no encontrada'
            }), 404
        
        actualizar_ficha(ficha_id, data['ficha'])
        
        ficha_actualizada = obtener_ficha_por_id(ficha_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Ficha actualizada exitosamente',
            'data': ficha_actualizada
        }), 200
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': 'Datos inválidos',
            'details': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Error interno al actualizar la ficha',
            'details': str(e)
        }), 500





from flasgger import swag_from

@app.route('/api/fichas/<int:ficha_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Fichas'],
    'description': 'Eliminar una ficha por ID',
    'parameters': [
        {
            'name': 'ficha_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la ficha a eliminar'
        }
    ],
    'responses': {
        200: {
            'description': 'Ficha eliminada exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Ficha con ID 1 eliminada exitosamente',
                    'data_eliminada': {'id': 1, 'ficha': 'FICHA001'}
                }
            }
        },
        400: {
            'description': 'ID inválido'
        },
        404: {
            'description': 'Ficha no encontrada'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def eliminar_ficha_por_id(ficha_id):
    try:
        if ficha_id <= 0:
            return jsonify({
                'status': 'error',
                'message': 'El ID debe ser un número positivo'
            }), 400
        
        ficha_existente = obtener_ficha_por_id(ficha_id)
        if not ficha_existente:
            return jsonify({
                'status': 'error',
                'message': f'Ficha con ID {ficha_id} no encontrada'
            }), 404
        
        eliminar_ficha(ficha_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Ficha con ID {ficha_id} eliminada exitosamente',
            'data_eliminada': ficha_existente
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Error interno al eliminar la ficha',
            'details': str(e)
        }), 500

#-------------------------------------Usuarios----------------------------------------------#

@app.route('/api/usuarios', methods=['POST'])
@swag_from({
    'tags': ['Usuarios'],
    'description': 'Crear un nuevo usuario',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string', 'example': 'Juan Pérez'},
                    'correo': {'type': 'string', 'example': 'juan@ejemplo.com'},
                    'contrasena': {'type': 'string', 'example': 'password123'}
                },
                'required': ['nombre', 'correo', 'contrasena']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Usuario creado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Usuario creado exitosamente',
                    'id': 1
                }
            }
        },
        400: {
            'description': 'Datos inválidos o faltantes'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def add_usuario():
    try:
        data = request.get_json()
        nuevo_id = crear_usuario(data)

        if nuevo_id is None:
            raise ValueError("No se pudo crear el usuario. Verifica los datos enviados.")

        return jsonify({
            'status': 'success',
            'message': 'Usuario creado exitosamente',
            'id': nuevo_id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios', methods=['GET'])
@swag_from({
    'tags': ['Usuarios'],
    'description': 'Obtener todos los usuarios',
    'responses': {
        200: {
            'description': 'Lista de usuarios',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {'id': 1, 'nombre': 'Juan Pérez', 'correo': 'juan@ejemplo.com'},
                        {'id': 2, 'nombre': 'María García', 'correo': 'maria@ejemplo.com'}
                    ],
                    'count': 2
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_usuarios():
    try:
        usuarios = obtener_todos_usuarios()
        return jsonify({
            'status': 'success',
            'data': usuarios,
            'count': len(usuarios)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
@swag_from({
    'tags': ['Usuarios'],
    'description': 'Obtener usuario por ID',
    'parameters': [
        {
            'name': 'usuario_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario'
        }
    ],
    'responses': {
        200: {
            'description': 'Usuario encontrado',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {'id': 1, 'nombre': 'Juan Pérez', 'correo': 'juan@ejemplo.com'}
                }
            }
        },
        404: {
            'description': 'Usuario no encontrado'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_usuario_por_id(usuario_id):
    try:
        usuario = obtener_usuario_por_id(usuario_id)
        if usuario:
            return jsonify({'status': 'success', 'data': usuario}), 200
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/correo/<string:correo>', methods=['GET'])
@swag_from({
    'tags': ['Usuarios'],
    'description': 'Obtener usuario por correo electrónico',
    'parameters': [
        {
            'name': 'correo',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Correo electrónico del usuario'
        }
    ],
    'responses': {
        200: {
            'description': 'Usuario encontrado',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {'id': 1, 'nombre': 'Juan Pérez', 'correo': 'juan@ejemplo.com'}
                }
            }
        },
        404: {
            'description': 'Usuario no encontrado'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_usuario_por_correo(correo):
    try:
        usuario = obtener_usuario_por_correo(correo)
        if usuario:
            return jsonify({'status': 'success', 'data': usuario}), 200
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
@swag_from({
    'tags': ['Usuarios'],
    'description': 'Actualizar usuario existente',
    'parameters': [
        {
            'name': 'usuario_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario a actualizar'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string', 'example': 'Juan Pérez Actualizado'},
                    'correo': {'type': 'string', 'example': 'juan.actualizado@ejemplo.com'},
                    'contrasena': {'type': 'string', 'example': 'nuevapassword123'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Usuario actualizado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Usuario actualizado exitosamente',
                    'data': {'id': 1, 'nombre': 'Juan Pérez Actualizado', 'correo': 'juan.actualizado@ejemplo.com'}
                }
            }
        },
        400: {
            'description': 'Datos inválidos'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def update_usuario(usuario_id):
    try:
        data = request.get_json()
        actualizar_usuario(usuario_id, data)
        usuario_actualizado = obtener_usuario_por_id(usuario_id)
        return jsonify({
            'status': 'success',
            'message': 'Usuario actualizado exitosamente',
            'data': usuario_actualizado
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Usuarios'],
    'description': 'Eliminar usuario por ID',
    'parameters': [
        {
            'name': 'usuario_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario a eliminar'
        }
    ],
    'responses': {
        200: {
            'description': 'Usuario eliminado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Usuario eliminado exitosamente'
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def delete_usuario(usuario_id):
    try:
        eliminar_usuario(usuario_id)
        return jsonify({
            'status': 'success',
            'message': 'Usuario eliminado exitosamente'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/ficha/<int:ficha_id>', methods=['GET'])
@swag_from({
    'tags': ['Usuarios'],
    'description': 'Obtener usuarios asociados a una ficha',
    'parameters': [
        {
            'name': 'ficha_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la ficha'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de usuarios de la ficha',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {'id': 1, 'nombre': 'Juan Pérez', 'correo': 'juan@ejemplo.com'},
                        {'id': 2, 'nombre': 'María García', 'correo': 'maria@ejemplo.com'}
                    ],
                    'count': 2
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_usuarios_por_ficha(ficha_id):
    try:
        usuarios = obtener_usuarios_por_ficha(ficha_id)
        return jsonify({
            'status': 'success',
            'data': usuarios,
            'count': len(usuarios)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/buscar', methods=['GET'])
@swag_from({
    'tags': ['Usuarios'],
    'description': 'Buscar usuarios por nombre',
    'parameters': [
        {
            'name': 'nombre',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Texto para buscar en nombres de usuarios'
        }
    ],
    'responses': {
        200: {
            'description': 'Resultados de búsqueda',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {'id': 1, 'nombre': 'Juan Pérez', 'correo': 'juan@ejemplo.com'},
                        {'id': 2, 'nombre': 'Juan Carlos', 'correo': 'juanc@ejemplo.com'}
                    ],
                    'count': 2
                }
            }
        },
        400: {
            'description': 'Parámetro de búsqueda faltante'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def search_usuarios():
    try:
        nombre = request.args.get('nombre', '')
        if not nombre:
            return jsonify({'error': 'Parámetro "nombre" requerido'}), 400
        
        usuarios = buscar_usuarios_por_nombre(nombre)
        return jsonify({
            'status': 'success',
            'data': usuarios,
            'count': len(usuarios)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#------------------------------------------- Evaluaciones ----------------------------#

@app.route('/api/evaluaciones', methods=['POST'])
@swag_from({
    'tags': ['Evaluaciones'],
    'description': 'Crear una nueva evaluación',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'pregunta': {'type': 'string', 'example': '¿Cuál es la capital de Francia?'},
                    'respuesta_correcta': {'type': 'string', 'example': 'París'},
                    'opciones': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ['Londres', 'París', 'Berlín', 'Madrid']
                    },
                    'dificultad': {'type': 'string', 'example': 'media'},
                    'categoria': {'type': 'string', 'example': 'Geografía'}
                },
                'required': ['pregunta', 'respuesta_correcta']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Evaluación creada exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Evaluación creada exitosamente',
                    'id': 1
                }
            }
        },
        400: {
            'description': 'Datos inválidos o faltantes'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def add_evaluacion():
    try:
        data = request.get_json()
        nuevo_id = crear_evaluacion(data)
        return jsonify({
            'status': 'success',
            'message': 'Evaluación creada exitosamente',
            'id': nuevo_id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluaciones', methods=['GET'])
@swag_from({
    'tags': ['Evaluaciones'],
    'description': 'Obtener todas las evaluaciones',
    'responses': {
        200: {
            'description': 'Lista de evaluaciones',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'pregunta': '¿Cuál es la capital de Francia?',
                            'respuesta_correcta': 'París',
                            'dificultad': 'media',
                            'categoria': 'Geografía'
                        }
                    ],
                    'count': 1
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_evaluaciones():
    try:
        evaluaciones = obtener_todas_evaluaciones()
        return jsonify({
            'status': 'success',
            'data': evaluaciones,
            'count': len(evaluaciones)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluaciones/<int:evaluacion_id>', methods=['GET'])
@swag_from({
    'tags': ['Evaluaciones'],
    'description': 'Obtener evaluación por ID',
    'parameters': [
        {
            'name': 'evaluacion_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la evaluación'
        }
    ],
    'responses': {
        200: {
            'description': 'Evaluación encontrada',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {
                        'id': 1,
                        'pregunta': '¿Cuál es la capital de Francia?',
                        'respuesta_correcta': 'París',
                        'dificultad': 'media',
                        'categoria': 'Geografía'
                    }
                }
            }
        },
        404: {
            'description': 'Evaluación no encontrada'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_evaluacion_por_id(evaluacion_id):
    try:
        evaluacion = obtener_evaluacion_por_id(evaluacion_id)
        if evaluacion:
            return jsonify({'status': 'success', 'data': evaluacion}), 200
        else:
            return jsonify({'error': 'Evaluación no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluaciones/<int:evaluacion_id>', methods=['PUT'])
@swag_from({
    'tags': ['Evaluaciones'],
    'description': 'Actualizar evaluación existente',
    'parameters': [
        {
            'name': 'evaluacion_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la evaluación a actualizar'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'pregunta': {'type': 'string', 'example': '¿Cuál es la capital de Italia?'},
                    'respuesta_correcta': {'type': 'string', 'example': 'Roma'},
                    'opciones': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ['Milán', 'Roma', 'Nápoles', 'Turín']
                    },
                    'dificultad': {'type': 'string', 'example': 'baja'},
                    'categoria': {'type': 'string', 'example': 'Geografía Europea'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Evaluación actualizada exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Evaluación actualizada exitosamente',
                    'data': {
                        'id': 1,
                        'pregunta': '¿Cuál es la capital de Italia?',
                        'respuesta_correcta': 'Roma',
                        'dificultad': 'baja',
                        'categoria': 'Geografía Europea'
                    }
                }
            }
        },
        400: {
            'description': 'Datos inválidos'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def update_evaluacion(evaluacion_id):
    try:
        data = request.get_json()
        actualizar_evaluacion(evaluacion_id, data)
        evaluacion_actualizada = obtener_evaluacion_por_id(evaluacion_id)
        return jsonify({
            'status': 'success',
            'message': 'Evaluación actualizada exitosamente',
            'data': evaluacion_actualizada
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluaciones/<int:evaluacion_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Evaluaciones'],
    'description': 'Eliminar evaluación por ID',
    'parameters': [
        {
            'name': 'evaluacion_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la evaluación a eliminar'
        }
    ],
    'responses': {
        200: {
            'description': 'Evaluación eliminada exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Evaluación eliminada exitosamente'
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def delete_evaluacion(evaluacion_id):
    try:
        eliminar_evaluacion(evaluacion_id)
        return jsonify({
            'status': 'success',
            'message': 'Evaluación eliminada exitosamente'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluaciones/buscar', methods=['GET'])
@swag_from({
    'tags': ['Evaluaciones'],
    'description': 'Buscar evaluaciones por texto en la pregunta',
    'parameters': [
        {
            'name': 'q',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Texto para buscar en las preguntas'
        }
    ],
    'responses': {
        200: {
            'description': 'Resultados de búsqueda',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'pregunta': '¿Cuál es la capital de Francia?',
                            'respuesta_correcta': 'París',
                            'dificultad': 'media'
                        }
                    ],
                    'count': 1
                }
            }
        },
        400: {
            'description': 'Parámetro de búsqueda faltante'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def search_evaluaciones():
    try:
        texto = request.args.get('q', '')
        if not texto:
            return jsonify({'error': 'Parámetro "q" requerido'}), 400
        
        evaluaciones = buscar_evaluaciones_por_pregunta(texto)
        return jsonify({
            'status': 'success',
            'data': evaluaciones,
            'count': len(evaluaciones)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500





from flasgger import swag_from

@app.route('/api/evaluaciones/filtro/calificacion', methods=['GET'])
@swag_from({
    'tags': ['Evaluaciones'],
    'description': 'Filtrar evaluaciones por rango de calificación',
    'parameters': [
        {
            'name': 'min',
            'in': 'query',
            'type': 'number',
            'format': 'float',
            'required': False,
            'description': 'Calificación mínima (inclusive)'
        },
        {
            'name': 'max',
            'in': 'query',
            'type': 'number',
            'format': 'float',
            'required': False,
            'description': 'Calificación máxima (inclusive)'
        }
    ],
    'responses': {
        200: {
            'description': 'Evaluaciones filtradas por calificación',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'pregunta': '¿Cuál es la capital de Francia?',
                            'calificacion': 8.5
                        }
                    ],
                    'count': 1
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_evaluaciones_por_calificacion():
    try:
        min_cal = request.args.get('min', type=float)
        max_cal = request.args.get('max', type=float)
        
        evaluaciones = obtener_evaluaciones_por_calificacion(min_cal, max_cal)
        return jsonify({
            'status': 'success',
            'data': evaluaciones,
            'count': len(evaluaciones)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluaciones/estadisticas', methods=['GET'])
@swag_from({
    'tags': ['Evaluaciones'],
    'description': 'Obtener estadísticas generales de evaluaciones',
    'responses': {
        200: {
            'description': 'Estadísticas de evaluaciones',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {
                        'total': 150,
                        'sin_calificar': 25,
                        'con_imagen': 45,
                        'calificadas': 125
                    }
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_estadisticas_evaluaciones():
    try:
        total = contar_evaluaciones_totales()
        sin_calificar = len(obtener_evaluaciones_sin_calificar())
        con_imagen = len(obtener_evaluaciones_con_imagen())
        
        return jsonify({
            'status': 'success',
            'data': {
                'total': total,
                'sin_calificar': sin_calificar,
                'con_imagen': con_imagen,
                'calificadas': total - sin_calificar
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#-------------------------------------------- Contenido ------------------------------#

@app.route('/api/contenidos', methods=['POST'])
@swag_from({
    'tags': ['Contenidos'],
    'description': 'Crear un nuevo contenido',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'titulo': {'type': 'string', 'example': 'Introducción a Python'},
                    'descripcion': {'type': 'string', 'example': 'Conceptos básicos de Python'},
                    'tipo': {'type': 'string', 'example': 'video'},
                    'duracion': {'type': 'integer', 'example': 30},
                    'url': {'type': 'string', 'example': 'https://ejemplo.com/video'},
                    'avance': {'type': 'number', 'format': 'float', 'example': 0.0}
                },
                'required': ['titulo']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Contenido creado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Contenido creado exitosamente',
                    'idContenido': 1
                }
            }
        },
        400: {
            'description': 'Datos inválidos o faltantes'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def add_contenido():
    try:
        data = request.get_json()
        contenido_id = crear_contenido(data)
        return jsonify({
            'status': 'success',
            'message': 'Contenido creado exitosamente',
            'idContenido': contenido_id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contenidos', methods=['GET'])
@swag_from({
    'tags': ['Contenidos'],
    'description': 'Obtener todos los contenidos',
    'responses': {
        200: {
            'description': 'Lista de contenidos',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'titulo': 'Introducción a Python',
                            'tipo': 'video',
                            'avance': 75.5
                        }
                    ],
                    'count': 1
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_contenidos():
    try:
        contenidos = obtener_todos_contenidos()
        return jsonify({
            'status': 'success',
            'data': contenidos,
            'count': len(contenidos)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contenidos/<int:contenido_id>', methods=['GET'])
@swag_from({
    'tags': ['Contenidos'],
    'description': 'Obtener contenido por ID',
    'parameters': [
        {
            'name': 'contenido_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del contenido'
        }
    ],
    'responses': {
        200: {
            'description': 'Contenido encontrado',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {
                        'id': 1,
                        'titulo': 'Introducción a Python',
                        'descripcion': 'Conceptos básicos',
                        'tipo': 'video',
                        'avance': 75.5
                    }
                }
            }
        },
        404: {
            'description': 'Contenido no encontrado'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_contenido_por_id(contenido_id):
    try:
        contenido = obtener_contenido_por_id(contenido_id)
        if contenido:
            return jsonify({'status': 'success', 'data': contenido}), 200
        else:
            return jsonify({'error': 'Contenido no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contenidos/<int:contenido_id>', methods=['PUT'])
@swag_from({
    'tags': ['Contenidos'],
    'description': 'Actualizar contenido existente',
    'parameters': [
        {
            'name': 'contenido_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del contenido a actualizar'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'titulo': {'type': 'string', 'example': 'Python Avanzado'},
                    'descripcion': {'type': 'string', 'example': 'Conceptos avanzados de Python'},
                    'tipo': {'type': 'string', 'example': 'documento'},
                    'duracion': {'type': 'integer', 'example': 45},
                    'url': {'type': 'string', 'example': 'https://ejemplo.com/documento'},
                    'avance': {'type': 'number', 'format': 'float', 'example': 50.0}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Contenido actualizado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Contenido actualizado exitosamente',
                    'data': {
                        'id': 1,
                        'titulo': 'Python Avanzado',
                        'avance': 50.0
                    }
                }
            }
        },
        400: {
            'description': 'Datos inválidos'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def update_contenido(contenido_id):
    try:
        data = request.get_json()
        actualizar_contenido(contenido_id, data)
        contenido_actualizado = obtener_contenido_por_id(contenido_id)
        return jsonify({
            'status': 'success',
            'message': 'Contenido actualizado exitosamente',
            'data': contenido_actualizado
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contenidos/<int:contenido_id>/avance', methods=['PATCH'])
@swag_from({
    'tags': ['Contenidos'],
    'description': 'Actualizar solo el avance de un contenido',
    'parameters': [
        {
            'name': 'contenido_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del contenido'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'avance': {
                        'type': 'number',
                        'format': 'float',
                        'example': 85.5,
                        'description': 'Porcentaje de avance (0-100)'
                    }
                },
                'required': ['avance']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Avance actualizado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Avance actualizado exitosamente',
                    'data': {
                        'id': 1,
                        'titulo': 'Introducción a Python',
                        'avance': 85.5
                    }
                }
            }
        },
        400: {
            'description': 'Datos inválidos o campo avance faltante'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def update_avance_contenido(contenido_id):
    try:
        data = request.get_json()
        if 'avance' not in data:
            return jsonify({'error': 'El campo "avance" es requerido'}), 400
        
        actualizar_avance_contenido(contenido_id, data['avance'])
        contenido_actualizado = obtener_contenido_por_id(contenido_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Avance actualizado exitosamente',
            'data': contenido_actualizado
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contenidos/<int:contenido_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Contenidos'],
    'description': 'Eliminar contenido por ID',
    'parameters': [
        {
            'name': 'contenido_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del contenido a eliminar'
        }
    ],
    'responses': {
        200: {
            'description': 'Contenido eliminado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Contenido eliminado exitosamente'
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def delete_contenido(contenido_id):
    try:
        eliminar_contenido(contenido_id)
        return jsonify({
            'status': 'success',
            'message': 'Contenido eliminado exitosamente'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contenidos/buscar', methods=['GET'])
@swag_from({
    'tags': ['Contenidos'],
    'description': 'Buscar contenidos por nombre',
    'parameters': [
        {
            'name': 'nombre',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Texto para buscar en títulos de contenidos'
        }
    ],
    'responses': {
        200: {
            'description': 'Resultados de búsqueda',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'titulo': 'Introducción a Python',
                            'tipo': 'video'
                        }
                    ],
                    'count': 1
                }
            }
        },
        400: {
            'description': 'Parámetro de búsqueda faltante'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def search_contenidos():
    try:
        nombre = request.args.get('nombre', '')
        if not nombre:
            return jsonify({'error': 'Parámetro "nombre" requerido'}), 400
        
        contenidos = buscar_contenidos_por_nombre(nombre)
        return jsonify({
            'status': 'success',
            'data': contenidos,
            'count': len(contenidos)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contenidos/estadisticas', methods=['GET'])
@swag_from({
    'tags': ['Contenidos'],
    'description': 'Obtener estadísticas de contenidos',
    'responses': {
        200: {
            'description': 'Estadísticas de contenidos',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {
                        'completados': 25,
                        'pendientes': 15,
                        'total': 40,
                        'avance_promedio': 62.5
                    }
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_estadisticas_contenidos():
    try:
        completados = obtener_contenidos_completados()
        pendientes = obtener_contenidos_pendientes()
        promedio = obtener_promedio_avance()
        
        return jsonify({
            'status': 'success',
            'data': {
                'completados': len(completados),
                'pendientes': len(pendientes),
                'total': len(completados) + len(pendientes),
                'avance_promedio': promedio
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contenidos/filtro/avance', methods=['GET'])
@swag_from({
    'tags': ['Contenidos'],
    'description': 'Filtrar contenidos por rango de avance',
    'parameters': [
        {
            'name': 'min',
            'in': 'query',
            'type': 'number',
            'format': 'float',
            'required': False,
            'description': 'Avance mínimo (0-100)'
        },
        {
            'name': 'max',
            'in': 'query',
            'type': 'number',
            'format': 'float',
            'required': False,
            'description': 'Avance máximo (0-100)'
        }
    ],
    'responses': {
        200: {
            'description': 'Contenidos filtrados por avance',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'titulo': 'Introducción a Python',
                            'avance': 75.0
                        }
                    ],
                    'count': 1
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_contenidos_por_avance():
    try:
        min_avance = request.args.get('min', type=float)
        max_avance = request.args.get('max', type=float)
        
        contenidos = obtener_contenidos_por_avance(min_avance, max_avance)
        return jsonify({
            'status': 'success',
            'data': contenidos,
            'count': len(contenidos)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#--------------------------------------------------------------- Módulos --------------------------------#

@app.route('/api/modulos', methods=['POST'])
@swag_from({
    'tags': ['Módulos'],
    'description': 'Crear un nuevo módulo',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string', 'example': 'Fundamentos de Programación'},
                    'descripcion': {'type': 'string', 'example': 'Módulo introductorio a la programación'},
                    'duracion_estimada': {'type': 'integer', 'example': 40},
                    'nivel_dificultad': {'type': 'string', 'example': 'principiante'},
                    'activo': {'type': 'boolean', 'example': True}
                },
                'required': ['nombre']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Módulo creado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Módulo creado exitosamente',
                    'idModulo': 1
                }
            }
        },
        400: {
            'description': 'Datos inválidos o faltantes'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def add_modulo():
    try:
        data = request.get_json()
        modulo_id = crear_modulo(data)
        return jsonify({
            'status': 'success',
            'message': 'Módulo creado exitosamente',
            'idModulo': modulo_id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modulos', methods=['GET'])
@swag_from({
    'tags': ['Módulos'],
    'description': 'Obtener todos los módulos',
    'responses': {
        200: {
            'description': 'Lista de módulos',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'nombre': 'Fundamentos de Programación',
                            'descripcion': 'Módulo introductorio',
                            'nivel_dificultad': 'principiante'
                        }
                    ],
                    'count': 1
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_modulos():
    try:
        modulos = obtener_todos_modulos()
        return jsonify({
            'status': 'success',
            'data': modulos,
            'count': len(modulos)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modulos/paginados', methods=['GET'])
@swag_from({
    'tags': ['Módulos'],
    'description': 'Obtener módulos paginados',
    'parameters': [
        {
            'name': 'pagina',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 1,
            'description': 'Número de página'
        },
        {
            'name': 'por_pagina',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 10,
            'description': 'Cantidad de registros por página'
        }
    ],
    'responses': {
        200: {
            'description': 'Módulos paginados',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'nombre': 'Fundamentos de Programación',
                            'descripcion': 'Módulo introductorio'
                        }
                    ],
                    'paginacion': {
                        'pagina_actual': 1,
                        'por_pagina': 10,
                        'total_registros': 50,
                        'total_paginas': 5
                    }
                }
            }
        },
        400: {
            'description': 'Parámetros de paginación inválidos'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_modulos_paginados():
    try:
        pagina = request.args.get('pagina', 1, type=int)
        por_pagina = request.args.get('por_pagina', 10, type=int)
        
        if pagina < 1 or por_pagina < 1:
            return jsonify({'error': 'La página y por_pagina deben ser mayores a 0'}), 400
        
        resultado = obtener_modulos_paginados(pagina, por_pagina)
        return jsonify({
            'status': 'success',
            'data': resultado['datos'],
            'paginacion': {
                'pagina_actual': resultado['pagina_actual'],
                'por_pagina': resultado['por_pagina'],
                'total_registros': resultado['total_registros'],
                'total_paginas': resultado['total_paginas']
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modulos/<int:modulo_id>', methods=['GET'])
@swag_from({
    'tags': ['Módulos'],
    'description': 'Obtener módulo por ID',
    'parameters': [
        {
            'name': 'modulo_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del módulo'
        }
    ],
    'responses': {
        200: {
            'description': 'Módulo encontrado',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {
                        'id': 1,
                        'nombre': 'Fundamentos de Programación',
                        'descripcion': 'Módulo introductorio a la programación',
                        'nivel_dificultad': 'principiante'
                    }
                }
            }
        },
        404: {
            'description': 'Módulo no encontrado'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_modulo_por_id(modulo_id):
    try:
        modulo = obtener_modulo_por_id(modulo_id)
        if modulo:
            return jsonify({'status': 'success', 'data': modulo}), 200
        else:
            return jsonify({'error': 'Módulo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modulos/<int:modulo_id>', methods=['PUT'])
@swag_from({
    'tags': ['Módulos'],
    'description': 'Actualizar módulo existente',
    'parameters': [
        {
            'name': 'modulo_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del módulo a actualizar'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string', 'example': 'Programación Avanzada'},
                    'descripcion': {'type': 'string', 'example': 'Módulo de conceptos avanzados'},
                    'duracion_estimada': {'type': 'integer', 'example': 60},
                    'nivel_dificultad': {'type': 'string', 'example': 'avanzado'},
                    'activo': {'type': 'boolean', 'example': True}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Módulo actualizado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Módulo actualizado exitosamente',
                    'data': {
                        'id': 1,
                        'nombre': 'Programación Avanzada',
                        'nivel_dificultad': 'avanzado'
                    }
                }
            }
        },
        400: {
            'description': 'Datos inválidos'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def update_modulo(modulo_id):
    try:
        data = request.get_json()
        actualizar_modulo(modulo_id, data)
        modulo_actualizado = obtener_modulo_por_id(modulo_id)
        return jsonify({
            'status': 'success',
            'message': 'Módulo actualizado exitosamente',
            'data': modulo_actualizado
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modulos/<int:modulo_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Módulos'],
    'description': 'Eliminar módulo por ID',
    'parameters': [
        {
            'name': 'modulo_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del módulo a eliminar'
        }
    ],
    'responses': {
        200: {
            'description': 'Módulo eliminado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Módulo eliminado exitosamente'
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def delete_modulo(modulo_id):
    try:
        eliminar_modulo(modulo_id)
        return jsonify({
            'status': 'success',
            'message': 'Módulo eliminado exitosamente'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modulos/buscar/nombre', methods=['GET'])
@swag_from({
    'tags': ['Módulos'],
    'description': 'Buscar módulos por nombre',
    'parameters': [
        {
            'name': 'q',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Texto para buscar en nombres de módulos'
        }
    ],
    'responses': {
        200: {
            'description': 'Resultados de búsqueda por nombre',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'nombre': 'Fundamentos de Programación',
                            'descripcion': 'Módulo introductorio'
                        }
                    ],
                    'count': 1
                }
            }
        },
        400: {
            'description': 'Parámetro de búsqueda faltante'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def search_modulos_nombre():
    try:
        nombre = request.args.get('q', '')
        if not nombre:
            return jsonify({'error': 'Parámetro "q" requerido'}), 400
        
        resultados = buscar_modulos_por_nombre(nombre)
        return jsonify({
            'status': 'success',
            'data': resultados,
            'count': len(resultados)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modulos/buscar/descripcion', methods=['GET'])
@swag_from({
    'tags': ['Módulos'],
    'description': 'Buscar módulos por descripción',
    'parameters': [
        {
            'name': 'q',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Texto para buscar en descripciones de módulos'
        }
    ],
    'responses': {
        200: {
            'description': 'Resultados de búsqueda por descripción',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'nombre': 'Fundamentos de Programación',
                            'descripcion': 'Módulo introductorio a la programación'
                        }
                    ],
                    'count': 1
                }
            }
        },
        400: {
            'description': 'Parámetro de búsqueda faltante'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def search_modulos_descripcion():
    try:
        descripcion = request.args.get('q', '')
        if not descripcion:
            return jsonify({'error': 'Parámetro "q" requerido'}), 400
        
        resultados = buscar_modulos_por_descripcion(descripcion)
        return jsonify({
            'status': 'success',
            'data': resultados,
            'count': len(resultados)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modulos/ultimos', methods=['GET'])
@swag_from({
    'tags': ['Módulos'],
    'description': 'Obtener los últimos módulos creados',
    'parameters': [
        {
            'name': 'limite',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 5,
            'description': 'Límite de módulos a obtener'
        }
    ],
    'responses': {
        200: {
            'description': 'Últimos módulos creados',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 5,
                            'nombre': 'Módulo Reciente',
                            'fecha_creacion': '2024-01-15'
                        }
                    ],
                    'count': 1
                }
            }
        },
        400: {
            'description': 'Límite inválido'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_ultimos_modulos():
    try:
        limite = request.args.get('limite', 5, type=int)
        if limite < 1:
            return jsonify({'error': 'El límite debe ser mayor a 0'}), 400
        
        modulos = obtener_ultimos_modulos(limite)
        return jsonify({
            'status': 'success',
            'data': modulos,
            'count': len(modulos)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modulos/estadisticas', methods=['GET'])
@swag_from({
    'tags': ['Módulos'],
    'description': 'Obtener estadísticas de módulos',
    'responses': {
        200: {
            'description': 'Estadísticas de módulos',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {
                        'total_modulos': 25,
                        'modulos_activos': 20,
                        'modulos_inactivos': 5,
                        'promedio_duracion': 35.5
                    }
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_estadisticas_modulos():
    try:
        estadisticas = obtener_estadisticas_modulos()
        return jsonify({
            'status': 'success',
            'data': estadisticas
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modulos/total', methods=['GET'])
@swag_from({
    'tags': ['Módulos'],
    'description': 'Obtener el total de módulos',
    'responses': {
        200: {
            'description': 'Total de módulos',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'total_modulos': 25
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_total_modulos():
    try:
        total = contar_modulos_totales()
        return jsonify({
            'status': 'success',
            'total_modulos': total
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#------------------------------------- Desarrollo----------------------------------#

from flasgger import swag_from

@app.route('/api/desarrollos', methods=['POST'])
@swag_from({
    'tags': ['Desarrollos'],
    'description': 'Crear un nuevo desarrollo (relación usuario-módulo)',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'idUsuarios': {
                        'type': 'integer',
                        'example': 1,
                        'description': 'ID del usuario'
                    },
                    'idModulo': {
                        'type': 'integer', 
                        'example': 1,
                        'description': 'ID del módulo'
                    },
                    'avance': {
                        'type': 'number',
                        'format': 'float',
                        'example': 0.0,
                        'description': 'Porcentaje de avance inicial'
                    },
                    'estado': {
                        'type': 'string',
                        'example': 'en_progreso',
                        'description': 'Estado del desarrollo'
                    }
                },
                'required': ['idUsuarios', 'idModulo']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Desarrollo creado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Desarrollo creado exitosamente',
                    'idDesarrollo': 1
                }
            }
        },
        400: {
            'description': 'Datos inválidos o faltantes'
        },
        409: {
            'description': 'Ya existe un desarrollo para este usuario y módulo'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def add_desarrollo():
    try:
        data = request.get_json()
        
        desarrollo_existente = verificar_desarrollo_existente(data.get('idUsuarios'), data.get('idModulo'))
        if desarrollo_existente:
            return jsonify({
                'status': 'error',
                'message': 'Ya existe un desarrollo para este usuario y módulo',
                'desarrollo_existente': desarrollo_existente
            }), 409
        
        desarrollo_id = crear_desarrollo(data)
        return jsonify({
            'status': 'success',
            'message': 'Desarrollo creado exitosamente',
            'idDesarrollo': desarrollo_id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/desarrollos', methods=['GET'])
@swag_from({
    'tags': ['Desarrollos'],
    'description': 'Obtener todos los desarrollos',
    'responses': {
        200: {
            'description': 'Lista de todos los desarrollos',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'idUsuarios': 1,
                            'idModulo': 1,
                            'avance': 75.5,
                            'estado': 'en_progreso'
                        }
                    ],
                    'count': 1
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_desarrollos():
    try:
        desarrollos = obtener_todos_desarrollos()
        return jsonify({
            'status': 'success',
            'data': desarrollos,
            'count': len(desarrollos)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/desarrollos/<int:desarrollo_id>', methods=['GET'])
@swag_from({
    'tags': ['Desarrollos'],
    'description': 'Obtener desarrollo por ID',
    'parameters': [
        {
            'name': 'desarrollo_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del desarrollo'
        }
    ],
    'responses': {
        200: {
            'description': 'Desarrollo encontrado',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {
                        'id': 1,
                        'idUsuarios': 1,
                        'idModulo': 1,
                        'avance': 75.5,
                        'estado': 'en_progreso'
                    }
                }
            }
        },
        404: {
            'description': 'Desarrollo no encontrado'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_desarrollo_por_id(desarrollo_id):
    try:
        desarrollo = obtener_desarrollo_por_id(desarrollo_id)
        if desarrollo:
            return jsonify({'status': 'success', 'data': desarrollo}), 200
        else:
            return jsonify({'error': 'Desarrollo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:usuario_id>/desarrollos', methods=['GET'])
@swag_from({
    'tags': ['Desarrollos'],
    'description': 'Obtener desarrollos por usuario',
    'parameters': [
        {
            'name': 'usuario_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario'
        }
    ],
    'responses': {
        200: {
            'description': 'Desarrollos del usuario',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'idModulo': 1,
                            'avance': 75.5,
                            'estado': 'en_progreso'
                        }
                    ],
                    'count': 1,
                    'avance_promedio': 75.5
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_desarrollos_por_usuario(usuario_id):
    try:
        desarrollos = obtener_desarrollos_por_usuario(usuario_id)
        avance_promedio = obtener_avance_promedio_usuario(usuario_id)
        
        return jsonify({
            'status': 'success',
            'data': desarrollos,
            'count': len(desarrollos),
            'avance_promedio': avance_promedio
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modulos/<int:modulo_id>/desarrollos', methods=['GET'])
@swag_from({
    'tags': ['Desarrollos'],
    'description': 'Obtener desarrollos por módulo',
    'parameters': [
        {
            'name': 'modulo_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del módulo'
        }
    ],
    'responses': {
        200: {
            'description': 'Desarrollos del módulo',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': [
                        {
                            'id': 1,
                            'idUsuarios': 1,
                            'avance': 75.5,
                            'estado': 'en_progreso'
                        }
                    ],
                    'count': 1,
                    'avance_promedio': 75.5
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_desarrollos_por_modulo(modulo_id):
    try:
        desarrollos = obtener_desarrollos_por_modulo(modulo_id)
        avance_promedio = obtener_avance_promedio_modulo(modulo_id)
        
        return jsonify({
            'status': 'success',
            'data': desarrollos,
            'count': len(desarrollos),
            'avance_promedio': avance_promedio
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:usuario_id>/modulos/<int:modulo_id>/desarrollo', methods=['GET'])
@swag_from({
    'tags': ['Desarrollos'],
    'description': 'Obtener desarrollo específico de usuario y módulo',
    'parameters': [
        {
            'name': 'usuario_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario'
        },
        {
            'name': 'modulo_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del módulo'
        }
    ],
    'responses': {
        200: {
            'description': 'Desarrollo encontrado',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {
                        'id': 1,
                        'avance': 75.5,
                        'estado': 'en_progreso'
                    }
                }
            }
        },
        404: {
            'description': 'Desarrollo no encontrado'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_desarrollo_usuario_modulo(usuario_id, modulo_id):
    try:
        desarrollo = obtener_desarrollo_usuario_modulo(usuario_id, modulo_id)
        if desarrollo:
            return jsonify({'status': 'success', 'data': desarrollo}), 200
        else:
            return jsonify({
                'status': 'not_found',
                'message': 'No se encontró desarrollo para este usuario y módulo'
            }), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/desarrollos/<int:desarrollo_id>/avance', methods=['PATCH'])
@swag_from({
    'tags': ['Desarrollos'],
    'description': 'Actualizar avance de desarrollo por ID',
    'parameters': [
        {
            'name': 'desarrollo_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del desarrollo'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'avance': {
                        'type': 'number',
                        'format': 'float',
                        'example': 85.0,
                        'description': 'Nuevo porcentaje de avance (0-100)'
                    }
                },
                'required': ['avance']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Avance actualizado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Avance actualizado exitosamente',
                    'data': {
                        'id': 1,
                        'avance': 85.0,
                        'estado': 'en_progreso'
                    }
                }
            }
        },
        400: {
            'description': 'Campo avance faltante o datos inválidos'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def update_avance_desarrollo(desarrollo_id):
    try:
        data = request.get_json()
        if 'avance' not in data:
            return jsonify({'error': 'El campo "avance" es requerido'}), 400
        
        actualizar_avance_desarrollo(desarrollo_id, data['avance'])
        desarrollo_actualizado = obtener_desarrollo_por_id(desarrollo_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Avance actualizado exitosamente',
            'data': desarrollo_actualizado
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:usuario_id>/modulos/<int:modulo_id>/avance', methods=['PATCH'])
@swag_from({
    'tags': ['Desarrollos'],
    'description': 'Actualizar avance por usuario y módulo',
    'parameters': [
        {
            'name': 'usuario_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario'
        },
        {
            'name': 'modulo_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del módulo'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'avance': {
                        'type': 'number',
                        'format': 'float',
                        'example': 90.0,
                        'description': 'Nuevo porcentaje de avance (0-100)'
                    }
                },
                'required': ['avance']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Avance actualizado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Avance actualizado exitosamente',
                    'data': {
                        'id': 1,
                        'avance': 90.0,
                        'estado': 'en_progreso'
                    }
                }
            }
        },
        400: {
            'description': 'Campo avance faltante o datos inválidos'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def update_avance_usuario_modulo(usuario_id, modulo_id):
    try:
        data = request.get_json()
        if 'avance' not in data:
            return jsonify({'error': 'El campo "avance" es requerido'}), 400
        
        actualizar_avance_usuario_modulo(usuario_id, modulo_id, data['avance'])
        desarrollo_actualizado = obtener_desarrollo_usuario_modulo(usuario_id, modulo_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Avance actualizado exitosamente',
            'data': desarrollo_actualizado
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/desarrollos/estadisticas', methods=['GET'])
@swag_from({
    'tags': ['Desarrollos'],
    'description': 'Obtener estadísticas de desarrollos',
    'responses': {
        200: {
            'description': 'Estadísticas de desarrollos',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'data': {
                        'top_usuarios': [
                            {
                                'usuario_id': 1,
                                'nombre': 'Juan Pérez',
                                'avance_promedio': 95.5
                            }
                        ],
                        'top_modulos': [
                            {
                                'modulo_id': 1,
                                'nombre': 'Fundamentos',
                                'avance_promedio': 88.2
                            }
                        ]
                    }
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def get_estadisticas_desarrollos():
    try:
        top_usuarios = obtener_usuarios_top_avance(10)
        top_modulos = obtener_modulos_top_avance(10)
        
        return jsonify({
            'status': 'success',
            'data': {
                'top_usuarios': top_usuarios,
                'top_modulos': top_modulos
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/desarrollos/<int:desarrollo_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Desarrollos'],
    'description': 'Eliminar desarrollo por ID',
    'parameters': [
        {
            'name': 'desarrollo_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del desarrollo a eliminar'
        }
    ],
    'responses': {
        200: {
            'description': 'Desarrollo eliminado exitosamente',
            'examples': {
                'application/json': {
                    'status': 'success',
                    'message': 'Desarrollo eliminado exitosamente'
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def delete_desarrollo(desarrollo_id):
    try:
        eliminar_desarrollo(desarrollo_id)
        return jsonify({
            'status': 'success',
            'message': 'Desarrollo eliminado exitosamente'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#------------------------------------------ Biblioteca---------------------------------#

@app.route('/api/biblioteca', methods=['POST'])
@swag_from({
    'tags': ['Biblioteca'],
    'description': 'Crear un nuevo recurso en la biblioteca',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'titulo': {
                        'type': 'string',
                        'example': 'Introducción a Python',
                        'description': 'Título del recurso'
                    },
                    'autor': {
                        'type': 'string', 
                        'example': 'Juan Pérez',
                        'description': 'Autor del recurso'
                    },
                    'tipo': {
                        'type': 'string',
                        'example': 'libro',
                        'description': 'Tipo de recurso (libro, artículo, video, etc.)'
                    },
                    'url': {
                        'type': 'string',
                        'example': 'https://ejemplo.com/recurso',
                        'description': 'URL del recurso'
                    },
                    'descripcion': {
                        'type': 'string',
                        'example': 'Recurso introductorio sobre Python',
                        'description': 'Descripción del recurso'
                    },
                    'palabras_clave': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ['python', 'programación', 'introducción'],
                        'description': 'Palabras clave del recurso'
                    }
                },
                'required': ['titulo', 'tipo']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Recurso creado exitosamente',
            'examples': {
                'application/json': {
                    'success': True,
                    'message': 'Recurso creado exitosamente',
                    'id': 1
                }
            }
        },
        400: {
            'description': 'Datos inválidos o faltantes'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def crear_recurso_biblioteca_route():
    try:
        data = request.get_json()
        
        data_validada = validar_recurso_biblioteca(data)
        
        nuevo_id = crear_recurso_biblioteca(data_validada)
        
        return jsonify({
            'success': True,
            'message': 'Recurso creado exitosamente',
            'id': nuevo_id
        }), 201
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/biblioteca', methods=['GET'])
@swag_from({
    'tags': ['Biblioteca'],
    'description': 'Obtener todos los recursos de la biblioteca',
    'responses': {
        200: {
            'description': 'Lista de recursos de la biblioteca',
            'examples': {
                'application/json': {
                    'success': True,
                    'data': [
                        {
                            'id': 1,
                            'titulo': 'Introducción a Python',
                            'autor': 'Juan Pérez',
                            'tipo': 'libro'
                        }
                    ],
                    'total': 1
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_todos_recursos_biblioteca():
    try:
        recursos = obtener_recursos_biblioteca()
        return jsonify({
            'success': True,
            'data': recursos,
            'total': len(recursos)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/biblioteca/<int:id_biblioteca>', methods=['GET'])
@swag_from({
    'tags': ['Biblioteca'],
    'description': 'Obtener un recurso específico por ID',
    'parameters': [
        {
            'name': 'id_biblioteca',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del recurso de la biblioteca'
        }
    ],
    'responses': {
        200: {
            'description': 'Recurso encontrado',
            'examples': {
                'application/json': {
                    'success': True,
                    'data': {
                        'id': 1,
                        'titulo': 'Introducción a Python',
                        'autor': 'Juan Pérez',
                        'tipo': 'libro',
                        'descripcion': 'Recurso introductorio sobre Python'
                    }
                }
            }
        },
        404: {
            'description': 'Recurso no encontrado'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_recurso_biblioteca(id_biblioteca):
    try:
        recurso = obtener_recurso_biblioteca_por_id(id_biblioteca)
        
        if not recurso:
            return jsonify({
                'success': False,
                'error': 'Recurso no encontrado'
            }), 404
            
        return jsonify({
            'success': True,
            'data': recurso
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/biblioteca/buscar', methods=['GET'])
@swag_from({
    'tags': ['Biblioteca'],
    'description': 'Buscar recursos por término de búsqueda',
    'parameters': [
        {
            'name': 'q',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Término de búsqueda'
        }
    ],
    'responses': {
        200: {
            'description': 'Resultados de búsqueda',
            'examples': {
                'application/json': {
                    'success': True,
                    'data': [
                        {
                            'id': 1,
                            'titulo': 'Introducción a Python',
                            'autor': 'Juan Pérez'
                        }
                    ],
                    'total_resultados': 1,
                    'termino_busqueda': 'python'
                }
            }
        },
        400: {
            'description': 'Parámetro de búsqueda faltante'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def buscar_recursos_biblioteca_route():
    try:
        termino = request.args.get('q', '')
        
        if not termino:
            return jsonify({
                'success': False,
                'error': 'Parámetro de búsqueda (q) requerido'
            }), 400
            
        recursos = buscar_recursos_biblioteca(termino)
        
        return jsonify({
            'success': True,
            'data': recursos,
            'total_resultados': len(recursos),
            'termino_busqueda': termino
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/biblioteca/<int:id_biblioteca>', methods=['PUT'])
@swag_from({
    'tags': ['Biblioteca'],
    'description': 'Actualizar un recurso existente',
    'parameters': [
        {
            'name': 'id_biblioteca',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del recurso a actualizar'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'titulo': {'type': 'string', 'example': 'Python Avanzado'},
                    'autor': {'type': 'string', 'example': 'María García'},
                    'tipo': {'type': 'string', 'example': 'artículo'},
                    'url': {'type': 'string', 'example': 'https://ejemplo.com/avanzado'},
                    'descripcion': {'type': 'string', 'example': 'Conceptos avanzados de Python'},
                    'palabras_clave': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ['python', 'avanzado', 'programación']
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Recurso actualizado exitosamente',
            'examples': {
                'application/json': {
                    'success': True,
                    'message': 'Recurso actualizado exitosamente'
                }
            }
        },
        400: {
            'description': 'Datos inválidos o error en actualización'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def actualizar_recurso_biblioteca_route(id_biblioteca):
    try:
        data = request.get_json()
        
        data_validada = validar_recurso_biblioteca(data, es_actualizacion=True)
        
        resultado = actualizar_recurso_biblioteca(id_biblioteca, data_validada)
        
        if not resultado:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el recurso'
            }), 400
            
        return jsonify({
            'success': True,
            'message': 'Recurso actualizado exitosamente'
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/biblioteca/<int:id_biblioteca>', methods=['DELETE'])
@swag_from({
    'tags': ['Biblioteca'],
    'description': 'Eliminar un recurso de la biblioteca',
    'parameters': [
        {
            'name': 'id_biblioteca',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del recurso a eliminar'
        }
    ],
    'responses': {
        200: {
            'description': 'Recurso eliminado exitosamente',
            'examples': {
                'application/json': {
                    'success': True,
                    'message': 'Recurso eliminado exitosamente'
                }
            }
        },
        400: {
            'description': 'No se pudo eliminar el recurso'
        },
        404: {
            'description': 'Recurso no encontrado'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def eliminar_recurso_biblioteca_route(id_biblioteca):
    try:
        resultado = eliminar_recurso_biblioteca(id_biblioteca)
        
        if not resultado:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar el recurso'
            }), 400
            
        return jsonify({
            'success': True,
            'message': 'Recurso eliminado exitosamente'
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/biblioteca/estadisticas', methods=['GET'])
@swag_from({
    'tags': ['Biblioteca'],
    'description': 'Obtener estadísticas de la biblioteca',
    'responses': {
        200: {
            'description': 'Estadísticas de la biblioteca',
            'examples': {
                'application/json': {
                    'success': True,
                    'data': {
                        'total_recursos': 150,
                        'por_tipo': {
                            'libros': 50,
                            'articulos': 75,
                            'videos': 25
                        },
                        'recursos_recientes': 10
                    }
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_estadisticas_biblioteca_route():
    try:
        estadisticas = obtener_estadisticas_biblioteca()
        return jsonify({
            'success': True,
            'data': estadisticas
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/biblioteca/recientes', methods=['GET'])
@swag_from({
    'tags': ['Biblioteca'],
    'description': 'Obtener los recursos más recientes',
    'parameters': [
        {
            'name': 'limite',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 10,
            'description': 'Límite de recursos a obtener'
        }
    ],
    'responses': {
        200: {
            'description': 'Recursos más recientes',
            'examples': {
                'application/json': {
                    'success': True,
                    'data': [
                        {
                            'id': 1,
                            'titulo': 'Nuevo Recurso',
                            'fecha_creacion': '2024-01-15'
                        }
                    ],
                    'limite': 10
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_recursos_recientes_route():
    try:
        limite = request.args.get('limite', 10, type=int)
        recursos = obtener_recursos_recientes(limite)
        
        return jsonify({
            'success': True,
            'data': recursos,
            'limite': limite
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/biblioteca/contar', methods=['GET'])
@swag_from({
    'tags': ['Biblioteca'],
    'description': 'Contar el total de recursos en la biblioteca',
    'responses': {
        200: {
            'description': 'Total de recursos',
            'examples': {
                'application/json': {
                    'success': True,
                    'total': 150
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def contar_recursos_biblioteca_route():
    try:
        total = contar_recursos_biblioteca()
        return jsonify({
            'success': True,
            'total': total
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/biblioteca/palabra-clave/<string:palabra_clave>', methods=['GET'])
@swag_from({
    'tags': ['Biblioteca'],
    'description': 'Buscar recursos por palabra clave específica',
    'parameters': [
        {
            'name': 'palabra_clave',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Palabra clave para buscar'
        }
    ],
    'responses': {
        200: {
            'description': 'Recursos encontrados por palabra clave',
            'examples': {
                'application/json': {
                    'success': True,
                    'data': [
                        {
                            'id': 1,
                            'titulo': 'Introducción a Python',
                            'palabras_clave': ['python', 'programación']
                        }
                    ],
                    'total_resultados': 1,
                    'palabra_clave': 'python'
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def buscar_por_palabra_clave_route(palabra_clave):
    try:
        recursos = obtener_recursos_por_palabra_clave(palabra_clave)
        
        return jsonify({
            'success': True,
            'data': recursos,
            'total_resultados': len(recursos),
            'palabra_clave': palabra_clave
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


#--------------------------- Modifica ----------------------#

from flasgger import swag_from

@app.route('/api/modificaciones', methods=['GET', 'POST'])
@swag_from({
    'tags': ['Modificaciones'],
    'description': 'Obtener todas las modificaciones o crear una nueva',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': False,
            'description': 'Datos para crear una nueva modificación (solo POST)',
            'schema': {
                'type': 'object',
                'properties': {
                    'idUsuarios': {
                        'type': 'integer',
                        'example': 1,
                        'description': 'ID del usuario que realiza la modificación'
                    },
                    'idBiblioteca': {
                        'type': 'integer',
                        'example': 1,
                        'description': 'ID del recurso de biblioteca modificado'
                    },
                    'tipo_modificacion': {
                        'type': 'string',
                        'example': 'actualización',
                        'description': 'Tipo de modificación (creación, actualización, eliminación)'
                    },
                    'descripcion': {
                        'type': 'string',
                        'example': 'Actualización del título del recurso',
                        'description': 'Descripción de la modificación realizada'
                    }
                },
                'required': ['idUsuarios', 'idBiblioteca', 'tipo_modificacion']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de todas las modificaciones (GET)',
            'examples': {
                'application/json': [
                    {
                        'idModifica': 1,
                        'idUsuarios': 1,
                        'idBiblioteca': 1,
                        'tipo_modificacion': 'actualización',
                        'fecha_modificacion': '2024-01-15 10:30:00'
                    }
                ]
            }
        },
        201: {
            'description': 'Modificación creada exitosamente (POST)',
            'examples': {
                'application/json': {
                    'idModifica': 1,
                    'mensaje': 'Modificación creada exitosamente'
                }
            }
        },
        400: {
            'description': 'Datos JSON requeridos o inválidos'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def manejar_modificaciones():
    try:
        if request.method == 'GET':
            modificaciones = obtener_modificaciones()
            return jsonify([dict(row) for row in modificaciones]), 200
        
        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Datos JSON requeridos'}), 400
            
            id_modifica = crear_modificacion(data)
            return jsonify({'idModifica': id_modifica, 'mensaje': 'Modificación creada exitosamente'}), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/usuario/<int:id_usuario>', methods=['GET'])
@swag_from({
    'tags': ['Modificaciones'],
    'description': 'Obtener modificaciones por usuario',
    'parameters': [
        {
            'name': 'id_usuario',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario'
        }
    ],
    'responses': {
        200: {
            'description': 'Modificaciones del usuario',
            'examples': {
                'application/json': [
                    {
                        'idModifica': 1,
                        'idBiblioteca': 1,
                        'tipo_modificacion': 'actualización',
                        'fecha_modificacion': '2024-01-15 10:30:00'
                    }
                ]
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_modificaciones_usuario(id_usuario):
    try:
        modificaciones = obtener_modificaciones_por_usuario(id_usuario)
        return jsonify([dict(row) for row in modificaciones]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/biblioteca/<int:id_biblioteca>', methods=['GET'])
@swag_from({
    'tags': ['Modificaciones'],
    'description': 'Obtener modificaciones por recurso de biblioteca',
    'parameters': [
        {
            'name': 'id_biblioteca',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del recurso de biblioteca'
        }
    ],
    'responses': {
        200: {
            'description': 'Modificaciones del recurso',
            'examples': {
                'application/json': [
                    {
                        'idModifica': 1,
                        'idUsuarios': 1,
                        'tipo_modificacion': 'actualización',
                        'fecha_modificacion': '2024-01-15 10:30:00'
                    }
                ]
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_modificaciones_biblioteca(id_biblioteca):
    try:
        modificaciones = obtener_modificaciones_por_biblioteca(id_biblioteca)
        return jsonify([dict(row) for row in modificaciones]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/biblioteca/<int:id_biblioteca>/ultima', methods=['GET'])
@swag_from({
    'tags': ['Modificaciones'],
    'description': 'Obtener la última modificación de un recurso de biblioteca',
    'parameters': [
        {
            'name': 'id_biblioteca',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del recurso de biblioteca'
        }
    ],
    'responses': {
        200: {
            'description': 'Última modificación del recurso',
            'examples': {
                'application/json': {
                    'idModifica': 1,
                    'idUsuarios': 1,
                    'idBiblioteca': 1,
                    'tipo_modificacion': 'actualización',
                    'fecha_modificacion': '2024-01-15 10:30:00'
                }
            }
        },
        404: {
            'description': 'No se encontraron modificaciones para este recurso'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_ultima_modificacion(id_biblioteca):
    try:
        modificacion = obtener_ultima_modificacion_biblioteca(id_biblioteca)
        if modificacion:
            return jsonify(dict(modificacion)), 200
        else:
            return jsonify({'mensaje': 'No se encontraron modificaciones para este recurso'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/historial', methods=['GET'])
@swag_from({
    'tags': ['Modificaciones'],
    'description': 'Obtener historial completo de modificaciones',
    'responses': {
        200: {
            'description': 'Historial de modificaciones',
            'examples': {
                'application/json': [
                    {
                        'idModifica': 1,
                        'idUsuarios': 1,
                        'idBiblioteca': 1,
                        'tipo_modificacion': 'actualización',
                        'fecha_modificacion': '2024-01-15 10:30:00',
                        'nombre_usuario': 'Juan Pérez',
                        'titulo_recurso': 'Introducción a Python'
                    }
                ]
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_historial():
    try:
        historial = obtener_historial_modificaciones()
        return jsonify([dict(row) for row in historial]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/usuario/<int:id_usuario>/contar', methods=['GET'])
@swag_from({
    'tags': ['Modificaciones'],
    'description': 'Contar total de modificaciones por usuario',
    'parameters': [
        {
            'name': 'id_usuario',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario'
        }
    ],
    'responses': {
        200: {
            'description': 'Total de modificaciones del usuario',
            'examples': {
                'application/json': {
                    'idUsuarios': 1,
                    'total_modificaciones': 15
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def contar_modificaciones_usuario(id_usuario):
    try:
        total = contar_modificaciones_por_usuario(id_usuario)
        return jsonify({'idUsuarios': id_usuario, 'total_modificaciones': total}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/rango-fechas', methods=['GET'])
@swag_from({
    'tags': ['Modificaciones'],
    'description': 'Obtener modificaciones por rango de fechas',
    'parameters': [
        {
            'name': 'fecha_inicio',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'required': True,
            'description': 'Fecha de inicio (YYYY-MM-DD)'
        },
        {
            'name': 'fecha_fin',
            'in': 'query',
            'type': 'string',
            'format': 'date',
            'required': True,
            'description': 'Fecha de fin (YYYY-MM-DD)'
        }
    ],
    'responses': {
        200: {
            'description': 'Modificaciones en el rango de fechas',
            'examples': {
                'application/json': [
                    {
                        'idModifica': 1,
                        'idUsuarios': 1,
                        'idBiblioteca': 1,
                        'tipo_modificacion': 'actualización',
                        'fecha_modificacion': '2024-01-15 10:30:00'
                    }
                ]
            }
        },
        400: {
            'description': 'Parámetros de fecha requeridos'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_modificaciones_por_fecha():
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({'error': 'Los parámetros fecha_inicio y fecha_fin son requeridos'}), 400
        
        modificaciones = obtener_modificaciones_rango_fechas(fecha_inicio, fecha_fin)
        return jsonify([dict(row) for row in modificaciones]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/usuarios-activos', methods=['GET'])
@swag_from({
    'tags': ['Modificaciones'],
    'description': 'Obtener usuarios más activos (con más modificaciones)',
    'parameters': [
        {
            'name': 'limite',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 10,
            'description': 'Límite de usuarios a retornar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de usuarios más activos',
            'examples': {
                'application/json': [
                    {
                        'idUsuarios': 1,
                        'nombre': 'Juan Pérez',
                        'total_modificaciones': 25,
                        'ultima_modificacion': '2024-01-15 10:30:00'
                    }
                ]
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_usuarios_activos():
    try:
        limite = request.args.get('limite', default=10, type=int)
        usuarios = obtener_usuarios_mas_activos(limite)
        return jsonify([dict(row) for row in usuarios]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/recursos-modificados', methods=['GET'])
@swag_from({
    'tags': ['Modificaciones'],
    'description': 'Obtener recursos más modificados',
    'parameters': [
        {
            'name': 'limite',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 10,
            'description': 'Límite de recursos a retornar'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de recursos más modificados',
            'examples': {
                'application/json': [
                    {
                        'idBiblioteca': 1,
                        'titulo': 'Introducción a Python',
                        'total_modificaciones': 10,
                        'ultima_modificacion': '2024-01-15 10:30:00'
                    }
                ]
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_recursos_modificados():
    try:
        limite = request.args.get('limite', default=10, type=int)
        recursos = obtener_recursos_mas_modificados(limite)
        return jsonify([dict(row) for row in recursos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/estadisticas', methods=['GET'])
@swag_from({
    'tags': ['Modificaciones'],
    'description': 'Obtener estadísticas generales de modificaciones',
    'responses': {
        200: {
            'description': 'Estadísticas de modificaciones',
            'examples': {
                'application/json': {
                    'total_modificaciones': 150,
                    'modificaciones_hoy': 5,
                    'modificaciones_esta_semana': 25,
                    'modificaciones_este_mes': 80,
                    'usuarios_activos_total': 15,
                    'recursos_modificados_total': 45
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_estadisticas():
    try:
        estadisticas = obtener_estadisticas_modificaciones()
        return jsonify(estadisticas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#----------------------------- Rutas -------------------------------#

@app.route('/api/rutas', methods=['GET'])
@swag_from({
    'tags': ['Archivos'],
    'description': 'Obtener todas las rutas de archivos',
    'responses': {
        200: {
            'description': 'Lista de todas las rutas',
            'examples': {
                'application/json': {
                    'rutas': [
                        {
                            'idRuta': 1,
                            'idReferencia': 1,
                            'idTablas': 'biblioteca',
                            'ruta_archivo': '/uploads/documento.pdf',
                            'nombre_archivo': 'documento.pdf',
                            'fecha_subida': '2024-01-15 10:30:00'
                        }
                    ]
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_todas_rutas_endpoint():
    try:
        rutas = obtener_todas_rutas()
        return jsonify({'rutas': rutas}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rutas/<idTablas>/<int:id_referencia>', methods=['GET'])
@swag_from({
    'tags': ['Archivos'],
    'description': 'Obtener rutas de archivos por recurso específico',
    'parameters': [
        {
            'name': 'idTablas',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Tipo de tabla (ej: biblioteca, usuarios, modulos)'
        },
        {
            'name': 'id_referencia',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del recurso'
        }
    ],
    'responses': {
        200: {
            'description': 'Rutas del recurso específico',
            'examples': {
                'application/json': {
                    'rutas': [
                        {
                            'idRuta': 1,
                            'ruta_archivo': '/uploads/documento.pdf',
                            'nombre_archivo': 'documento.pdf',
                            'fecha_subida': '2024-01-15 10:30:00'
                        }
                    ]
                }
            }
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def obtener_rutas_recurso(idTablas, id_referencia):
    try:
        rutas = obtener_rutas_por_referencia(id_referencia, idTablas)
        return jsonify({'rutas': rutas}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload/<idTablas>/<int:id_referencia>', methods=['POST'])
@swag_from({
    'tags': ['Archivos'],
    'description': 'Subir un archivo asociado a un recurso',
    'parameters': [
        {
            'name': 'idTablas',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Tipo de tabla (ej: biblioteca, usuarios, modulos)'
        },
        {
            'name': 'id_referencia',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del recurso'
        },
        {
            'name': 'archivo',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Archivo a subir'
        }
    ],
    'consumes': ['multipart/form-data'],
    'responses': {
        200: {
            'description': 'Archivo subido exitosamente',
            'examples': {
                'application/json': {
                    'mensaje': 'Archivo subido exitosamente',
                    'data': {
                        'idRuta': 1,
                        'nombre_archivo': 'documento.pdf',
                        'ruta_archivo': '/uploads/documento.pdf',
                        'tamaño': 1024000
                    }
                }
            }
        },
        400: {
            'description': 'No se proporcionó archivo o nombre vacío'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def subir_archivo(idTablas, id_referencia):
    try:
        if 'archivo' not in request.files:
            return jsonify({'error': 'No se proporcionó archivo'}), 400
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            return jsonify({'error': 'Nombre de archivo vacío'}), 400
        
        resultado = archivo_service.subir_archivo(archivo, id_referencia, idTablas)
        
        return jsonify({
            'mensaje': 'Archivo subido exitosamente',
            'data': resultado
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rutas/<int:id_ruta>', methods=['DELETE'])
@swag_from({
    'tags': ['Archivos'],
    'description': 'Eliminar un archivo por ID de ruta',
    'parameters': [
        {
            'name': 'id_ruta',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la ruta/archivo a eliminar'
        }
    ],
    'responses': {
        200: {
            'description': 'Archivo eliminado exitosamente',
            'examples': {
                'application/json': {
                    'mensaje': 'Archivo eliminado exitosamente'
                }
            }
        },
        404: {
            'description': 'Archivo no encontrado'
        },
        500: {
            'description': 'Error interno del servidor'
        }
    }
})
def eliminar_ruta_endpoint(id_ruta):
    try:
        eliminado = archivo_service.eliminar_archivo(id_ruta)
        if eliminado:
            return jsonify({'mensaje': 'Archivo eliminado exitosamente'}), 200
        else:
            return jsonify({'error': 'Archivo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
  # Añade debug=True para ver errores