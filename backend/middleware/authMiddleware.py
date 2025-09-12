from flask import session, jsonify

def login_required(func):
    """Middleware para verificar si el usuario está logueado"""
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Debes iniciar sesión'}), 401
        return func(*args, **kwargs)
    return wrapper

def get_current_user():
    """Obtener usuario actual desde la sesión"""
    return {
        'id': session.get('user_id'),
        'username': session.get('username'),
        'email': session.get('email')
    } if session.get('user_id') else None