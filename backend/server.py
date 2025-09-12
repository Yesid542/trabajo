from flask import Flask, session
from flask import Flask, jsonify, request, g
from database import get_db, init_db, close_db
from flask_cors import CORS
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
CORS(app)

@app.route('/api/auth/login', methods=['POST'])
def login():
    # Usa tu usuarios_helpers.py para verificar credenciales
    from helpers.usuarios_helpers import verify_user_credentials
    
    data = request.get_json()
    user = verify_user_credentials(data['correo'], data['contrasena'])
    
    if user:
        session['email'] = user['correo']
        return jsonify({'message': 'Login exitoso', 'user': user})
    else:
        return jsonify({'error': 'Credenciales inválidas xd'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Sesión cerrada'})

@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    user = get_current_user()
    return jsonify({'authenticated': user is not None, 'user': user})

# 🛡️ Ejemplo de ruta protegida (usa tu lógica existente + middleware)
@app.route('/api/perfil', methods=['GET'])
@login_required  # 🔐 Middleware de autenticación
def perfil():
    # Usa tus helpers existentes
    from helpers.usuarios_helpers import get_user_profile
    user_profile = get_user_profile(get_current_user()['id'])
    return jsonify(user_profile)


#---------------------------------------------- Fichas-------------------------------------------------------------#




# Inicializa la BD al iniciar la aplicación (reemplaza before_first_request)
with app.app_context():
    init_db()

@app.teardown_appcontext
def teardown_appcontext(exception):
    close_db()


@app.route("/api/data")
def get_data():
    return jsonify({"message": "Hola desde Python!"})

@app.route('/api/fichas/valida/<string:ficha>', methods=['GET'])
def validar_ficha_en_bd(ficha):
    try:
        resultado = validar_ficha(ficha)
        
        if resultado:
            return jsonify({"existe":True})
        else:
            return jsonify(False)
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/fichas', methods=['GET'])
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
    
    # server.py
@app.route('/api/fichas/<int:ficha_id>', methods=['PUT'])
def actualizar_ficha_por_id(ficha_id):
    try:
        data = request.get_json()
        
        # Validar que existan datos y el campo 'ficha'
        if not data or 'ficha' not in data:
            return jsonify({
                'status': 'error',
                'message': 'El campo "ficha" es requerido en el cuerpo de la solicitud'
            }), 400
        
        # Validar que el texto no esté vacío
        if not data['ficha'] or not data['ficha'].strip():
            return jsonify({
                'status': 'error',
                'message': 'El campo "ficha" no puede estar vacío'
            }), 400
        
        # Verificar si la ficha existe antes de actualizar
        ficha_existente = obtener_ficha_por_id(ficha_id)
        if not ficha_existente:
            return jsonify({
                'status': 'error',
                'message': f'Ficha con ID {ficha_id} no encontrada'
            }), 404
        
        # Actualizar la ficha
        actualizar_ficha(ficha_id, data['ficha'])
        
        # Obtener la ficha actualizada para retornarla
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

@app.route('/api/fichas/<int:ficha_id>', methods=['DELETE'])
def eliminar_ficha_por_id(ficha_id):
   
    try:
        # Validar que el ID sea positivo
        if ficha_id <= 0:
            return jsonify({
                'status': 'error',
                'message': 'El ID debe ser un número positivo'
            }), 400
        
        # Verificar si la ficha existe antes de eliminar
        ficha_existente = obtener_ficha_por_id(ficha_id)
        if not ficha_existente:
            return jsonify({
                'status': 'error',
                'message': f'Ficha con ID {ficha_id} no encontrada'
            }), 404
        
        # Eliminar la ficha
        eliminar_ficha(ficha_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Ficha con ID {ficha_id} eliminada exitosamente',
            'data_eliminada': ficha_existente  # Opcional: retornar lo que se eliminó
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Error interno al eliminar la ficha',
            'details': str(e)
        }), 500
    
#-------------------------------------Usuarios----------------------------------------------#

@app.route('/api/usuarios', methods=['POST'])
def add_usuario():
    try:
        data = request.get_json()
        nuevo_id = crear_usuario(data)
        return jsonify({
            'status': 'success',
            'message': 'Usuario creado exitosamente',
            'id': nuevo_id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener todos los usuarios
@app.route('/api/usuarios', methods=['GET'])
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

# Ruta para obtener usuario por ID
@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
def get_usuario_por_id(usuario_id):
    try:
        usuario = obtener_usuario_por_id(usuario_id)
        if usuario:
            return jsonify({'status': 'success', 'data': usuario}), 200
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener usuario por correo
@app.route('/api/usuarios/correo/<string:correo>', methods=['GET'])
def get_usuario_por_correo(correo):
    try:
        usuario = obtener_usuario_por_correo(correo)
        if usuario:
            return jsonify({'status': 'success', 'data': usuario}), 200
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar usuario
@app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
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

# Ruta para eliminar usuario
@app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    try:
        eliminar_usuario(usuario_id)
        return jsonify({
            'status': 'success',
            'message': 'Usuario eliminado exitosamente'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener usuarios por ficha
@app.route('/api/usuarios/ficha/<int:ficha_id>', methods=['GET'])
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

# Ruta para buscar usuarios por nombre
@app.route('/api/usuarios/buscar', methods=['GET'])
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
    
#------------------------------------------- Evaluacion----------------------------#
@app.route('/api/evaluaciones', methods=['POST'])
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

# Ruta para obtener todas las evaluaciones
@app.route('/api/evaluaciones', methods=['GET'])
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

# Ruta para obtener evaluación por ID
@app.route('/api/evaluaciones/<int:evaluacion_id>', methods=['GET'])
def get_evaluacion_por_id(evaluacion_id):
    try:
        evaluacion = obtener_evaluacion_por_id(evaluacion_id)
        if evaluacion:
            return jsonify({'status': 'success', 'data': evaluacion}), 200
        else:
            return jsonify({'error': 'Evaluación no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar evaluación
@app.route('/api/evaluaciones/<int:evaluacion_id>', methods=['PUT'])
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

# Ruta para eliminar evaluación
@app.route('/api/evaluaciones/<int:evaluacion_id>', methods=['DELETE'])
def delete_evaluacion(evaluacion_id):
    try:
        eliminar_evaluacion(evaluacion_id)
        return jsonify({
            'status': 'success',
            'message': 'Evaluación eliminada exitosamente'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para buscar evaluaciones por texto
@app.route('/api/evaluaciones/buscar', methods=['GET'])
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

# Ruta para obtener evaluaciones por calificación
@app.route('/api/evaluaciones/filtro/calificacion', methods=['GET'])
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

# Ruta para obtener estadísticas
@app.route('/api/evaluaciones/estadisticas', methods=['GET'])
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

# Ruta para obtener todos los contenidos
@app.route('/api/contenidos', methods=['GET'])
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

# Ruta para obtener contenido por ID
@app.route('/api/contenidos/<int:contenido_id>', methods=['GET'])
def get_contenido_por_id(contenido_id):
    try:
        contenido = obtener_contenido_por_id(contenido_id)
        if contenido:
            return jsonify({'status': 'success', 'data': contenido}), 200
        else:
            return jsonify({'error': 'Contenido no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar contenido
@app.route('/api/contenidos/<int:contenido_id>', methods=['PUT'])
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

# Ruta para actualizar solo el avance
@app.route('/api/contenidos/<int:contenido_id>/avance', methods=['PATCH'])
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

# Ruta para eliminar contenido
@app.route('/api/contenidos/<int:contenido_id>', methods=['DELETE'])
def delete_contenido(contenido_id):
    try:
        eliminar_contenido(contenido_id)
        return jsonify({
            'status': 'success',
            'message': 'Contenido eliminado exitosamente'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para buscar contenidos por nombre
@app.route('/api/contenidos/buscar', methods=['GET'])
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

# Ruta para obtener estadísticas de contenido
@app.route('/api/contenidos/estadisticas', methods=['GET'])
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

# Ruta para filtrar contenidos por avance
@app.route('/api/contenidos/filtro/avance', methods=['GET'])
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
#--------------------------------------------------------------- modulos --------------------------------#

@app.route('/api/modulos', methods=['POST'])
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

# Ruta para obtener todos los módulos
@app.route('/api/modulos', methods=['GET'])
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

# Ruta para obtener módulos paginados
@app.route('/api/modulos/paginados', methods=['GET'])
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

# Ruta para obtener módulo por ID
@app.route('/api/modulos/<int:modulo_id>', methods=['GET'])
def get_modulo_por_id(modulo_id):
    try:
        modulo = obtener_modulo_por_id(modulo_id)
        if modulo:
            return jsonify({'status': 'success', 'data': modulo}), 200
        else:
            return jsonify({'error': 'Módulo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar módulo
@app.route('/api/modulos/<int:modulo_id>', methods=['PUT'])
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

# Ruta para eliminar módulo
@app.route('/api/modulos/<int:modulo_id>', methods=['DELETE'])
def delete_modulo(modulo_id):
    try:
        eliminar_modulo(modulo_id)
        return jsonify({
            'status': 'success',
            'message': 'Módulo eliminado exitosamente'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para buscar módulos por nombre
@app.route('/api/modulos/buscar/nombre', methods=['GET'])
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

# Ruta para buscar módulos por descripción
@app.route('/api/modulos/buscar/descripcion', methods=['GET'])
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

# Ruta para obtener últimos módulos
@app.route('/api/modulos/ultimos', methods=['GET'])
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

# Ruta para obtener estadísticas de módulos
@app.route('/api/modulos/estadisticas', methods=['GET'])
def get_estadisticas_modulos():
    try:
        estadisticas = obtener_estadisticas_modulos()
        return jsonify({
            'status': 'success',
            'data': estadisticas
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener total de módulos
@app.route('/api/modulos/total', methods=['GET'])
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

@app.route('/api/desarrollos', methods=['POST'])
def add_desarrollo():
    try:
        data = request.get_json()
        
        # Verificar si ya existe el desarrollo
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

# Ruta para obtener todos los desarrollos
@app.route('/api/desarrollos', methods=['GET'])
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

# Ruta para obtener desarrollo por ID
@app.route('/api/desarrollos/<int:desarrollo_id>', methods=['GET'])
def get_desarrollo_por_id(desarrollo_id):
    try:
        desarrollo = obtener_desarrollo_por_id(desarrollo_id)
        if desarrollo:
            return jsonify({'status': 'success', 'data': desarrollo}), 200
        else:
            return jsonify({'error': 'Desarrollo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener desarrollos por usuario
@app.route('/api/usuarios/<int:usuario_id>/desarrollos', methods=['GET'])
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

# Ruta para obtener desarrollos por módulo
@app.route('/api/modulos/<int:modulo_id>/desarrollos', methods=['GET'])
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

# Ruta para obtener desarrollo específico usuario-módulo
@app.route('/api/usuarios/<int:usuario_id>/modulos/<int:modulo_id>/desarrollo', methods=['GET'])
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

# Ruta para actualizar avance de desarrollo
@app.route('/api/desarrollos/<int:desarrollo_id>/avance', methods=['PATCH'])
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

# Ruta para actualizar avance usuario-módulo
@app.route('/api/usuarios/<int:usuario_id>/modulos/<int:modulo_id>/avance', methods=['PATCH'])
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

# Ruta para obtener estadísticas de avance
@app.route('/api/desarrollos/estadisticas', methods=['GET'])
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

# Ruta para eliminar desarrollo
@app.route('/api/desarrollos/<int:desarrollo_id>', methods=['DELETE'])
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
def crear_recurso_biblioteca_route():
    """
    Crear un nuevo recurso en la biblioteca
    """
    try:
        data = request.get_json()
        
        # Validar datos
        data_validada = validar_recurso_biblioteca(data)
        
        # Crear recurso
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
def obtener_todos_recursos_biblioteca():
    """
    Obtener todos los recursos de la biblioteca
    """
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
def obtener_recurso_biblioteca(id_biblioteca):
    """
    Obtener un recurso específico por ID
    """
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
def buscar_recursos_biblioteca_route():
    """
    Buscar recursos por término de búsqueda
    """
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
def actualizar_recurso_biblioteca_route(id_biblioteca):
    """
    Actualizar un recurso existente
    """
    try:
        data = request.get_json()
        
        # Validar datos para actualización
        data_validada = validar_recurso_biblioteca(data, es_actualizacion=True)
        
        # Actualizar recurso
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
def eliminar_recurso_biblioteca_route(id_biblioteca):
    """
    Eliminar un recurso de la biblioteca
    """
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
def obtener_estadisticas_biblioteca_route():
    """
    Obtener estadísticas de la biblioteca
    """
    try:
        estadisticas = obtener_estadisticas_biblioteca()
        return jsonify({
            'success': True,
            'data': estadisticas
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/biblioteca/recientes', methods=['GET'])
def obtener_recursos_recientes_route():
    """
    Obtener los recursos más recientes
    """
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
def contar_recursos_biblioteca_route():
    """
    Contar el total de recursos en la biblioteca
    """
    try:
        total = contar_recursos_biblioteca()
        return jsonify({
            'success': True,
            'total': total
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/biblioteca/palabra-clave/<string:palabra_clave>', methods=['GET'])
def buscar_por_palabra_clave_route(palabra_clave):
    """
    Buscar recursos por palabra clave específica
    """
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

@app.route('/api/modificaciones', methods=['GET', 'POST'])
def manejar_modificaciones():
    try:
        if request.method == 'GET':
            # Obtener todas las modificaciones
            modificaciones = obtener_modificaciones()
            return jsonify([dict(row) for row in modificaciones]), 200
        
        elif request.method == 'POST':
            # Crear una nueva modificación
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
def obtener_modificaciones_usuario(id_usuario):
    try:
        modificaciones = obtener_modificaciones_por_usuario(id_usuario)
        return jsonify([dict(row) for row in modificaciones]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/biblioteca/<int:id_biblioteca>', methods=['GET'])
def obtener_modificaciones_biblioteca(id_biblioteca):
    try:
        modificaciones = obtener_modificaciones_por_biblioteca(id_biblioteca)
        return jsonify([dict(row) for row in modificaciones]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/biblioteca/<int:id_biblioteca>/ultima', methods=['GET'])
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
def obtener_historial():
    try:
        historial = obtener_historial_modificaciones()
        return jsonify([dict(row) for row in historial]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def eliminar_modificacion(id_modifica):
    """
    Elimina un registro de modificación
    """
    try:
        # Verificar que la modificación existe antes de eliminar
        modificacion_existente = obtener_modificacion_por_id(id_modifica)
        if not modificacion_existente:
            return False
        
        # ejecutar_consulta devuelve el número de filas afectadas (entero)
        filas_afectadas = ejecutar_consulta(
            'DELETE FROM modifica WHERE idModifica = ?', 
            (id_modifica,)
        )
        
        # Siempre retorna True si llegó aquí sin excepciones
        # (la verificación de existencia ya se hizo arriba)
        return True
        
    except Exception as e:
        raise Exception(f"Error al eliminar modificación: {str(e)}")

@app.route('/api/modificaciones/usuario/<int:id_usuario>/contar', methods=['GET'])
def contar_modificaciones_usuario(id_usuario):
    try:
        total = contar_modificaciones_por_usuario(id_usuario)
        return jsonify({'idUsuarios': id_usuario, 'total_modificaciones': total}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/rango-fechas', methods=['GET'])
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
def obtener_usuarios_activos():
    try:
        limite = request.args.get('limite', default=10, type=int)
        usuarios = obtener_usuarios_mas_activos(limite)
        return jsonify([dict(row) for row in usuarios]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/recursos-modificados', methods=['GET'])
def obtener_recursos_modificados():
    try:
        limite = request.args.get('limite', default=10, type=int)
        recursos = obtener_recursos_mas_modificados(limite)
        return jsonify([dict(row) for row in recursos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modificaciones/estadisticas', methods=['GET'])
def obtener_estadisticas():
    try:
        estadisticas = obtener_estadisticas_modificaciones()
        return jsonify(estadisticas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
#----------------------------- Rutas -------------------------------#

@app.route('/api/rutas', methods=['GET'])
def obtener_todas_rutas_endpoint():
    try:
        rutas = obtener_todas_rutas()
        return jsonify({'rutas': rutas}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@app.route('/api/rutas/<idTablas>/<int:id_referencia>', methods=['GET'])
def obtener_rutas_recurso(idTablas, id_referencia):
    try:
        rutas = obtener_rutas_por_referencia(id_referencia, idTablas)
        return jsonify({'rutas': rutas}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload/<idTablas>/<int:id_referencia>', methods=['POST'])
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
    app.run(port=5000, debug=True)  # Añade debug=True para ver errores