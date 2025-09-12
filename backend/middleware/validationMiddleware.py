from flask import request, jsonify

def validate_json(schema):
    """Valida que el JSON cumpla con un esquema"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            # Aquí implementas validaciones según tu schema
            if not data:
                return jsonify({'error': 'Datos JSON requeridos'}), 400
            return func(*args, **kwargs)
        return wrapper
    return decorator
