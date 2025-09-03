# helpers/__init__.py
from .database_helpers import ejecutar_consulta
from .ficha_helpers import (
    obtener_todas_fichas,
    crear_ficha,
    obtener_ficha_por_id,
    actualizar_ficha,
    eliminar_ficha,
    buscar_fichas_por_texto
)
from .usuarios_helpers import (
    crear_usuario,
    obtener_todos_usuarios,
    obtener_usuario_por_id,
    obtener_usuario_por_correo,
    obtener_usuario_por_documento,
    actualizar_usuario,
    eliminar_usuario,
    obtener_usuarios_por_ficha,
    buscar_usuarios_por_nombre,
    validar_usuario_data,
    validar_correo
)
from .evaluacion_helpers import (
    crear_evaluacion,
    obtener_todas_evaluaciones,
    obtener_evaluacion_por_id,
    actualizar_evaluacion,
    eliminar_evaluacion,
    obtener_evaluaciones_por_calificacion,
    buscar_evaluaciones_por_pregunta,
    obtener_evaluaciones_sin_calificar,
    actualizar_calificacion,
    obtener_evaluaciones_con_imagen,
    contar_evaluaciones_totales,
    validar_evaluacion_data
)

from .contenido_helpers import (
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
    validar_contenido_data
)

from .desarrollo_helpers import (
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
    eliminar_desarrollo_usuario_modulo,
    obtener_avance_promedio_usuario,
    obtener_avance_promedio_modulo,
    obtener_usuarios_top_avance,
    obtener_modulos_top_avance,
    verificar_desarrollo_existente,
    validar_desarrollo_data
)
from .modulo_helpers import (
    crear_modulo,
    obtener_todos_modulos,
    obtener_modulo_por_id,
    actualizar_modulo,
    eliminar_modulo,
    buscar_modulos_por_nombre,
    buscar_modulos_por_descripcion,
    contar_modulos_totales,
    obtener_modulos_paginados,
    obtener_ultimos_modulos,
    obtener_estadisticas_modulos,
    validar_modulo_data
)

from .biblioteca_helpers import (
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
from .modifica_helpers import (
    validar_modificacion_data,
    crear_modificacion,
    obtener_modificaciones,
    obtener_modificacion_por_id,
    obtener_modificaciones_por_usuario,
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
from .rutas_helpers import (
    crear_ruta_archivo,
    obtener_rutas_por_referencia,
    obtener_ruta_por_id,
    eliminar_ruta,
    obtener_todas_rutas,
    contar_rutas_por_tabla
)
