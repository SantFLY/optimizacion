"""
Consultas SQL optimizadas para el sistema de alquiler de vehículos
"""

# Consultas de Vehículos
GET_VEHICULOS_DISPONIBLES = """
SELECT v.id, v.modelo, v.tipo, v.precio_base 
FROM vehiculos v 
LEFT JOIN alquileres a ON v.id = a.vehiculo_id AND a.activo = 1
WHERE a.id IS NULL
"""

GET_VEHICULOS_ALQUILADOS = """
SELECT v.id, v.modelo, v.tipo, v.precio_base
FROM vehiculos v 
INNER JOIN alquileres a ON v.id = a.vehiculo_id 
WHERE a.activo = 1
"""

# Consultas de Alquileres
GET_HISTORIAL_ALQUILERES = """
SELECT 
    a.id,
    v.modelo,
    v.tipo,
    a.fecha_inicio,
    a.dias,
    a.precio_final,
    a.descuento_aplicado,
    a.activo,
    CASE 
        WHEN a.fecha_fin IS NOT NULL THEN a.fecha_fin
        ELSE date(a.fecha_inicio, '+' || a.dias || ' days')
    END as fecha_fin
FROM alquileres a
INNER JOIN vehiculos v ON a.vehiculo_id = v.id
ORDER BY a.fecha_inicio DESC
"""

GET_ALQUILERES_ACTIVOS = """
SELECT 
    a.id,
    v.modelo,
    v.tipo,
    a.fecha_inicio,
    a.dias,
    a.precio_final
FROM alquileres a
INNER JOIN vehiculos v ON a.vehiculo_id = v.id
WHERE a.activo = 1
ORDER BY a.fecha_inicio DESC
"""

# Consultas de Inserción/Actualización
INSERT_VEHICULO = """
INSERT INTO vehiculos (modelo, tipo, precio_base)
VALUES (?, ?, ?)
"""

INSERT_ALQUILER = """
INSERT INTO alquileres (
    vehiculo_id, 
    fecha_inicio, 
    dias, 
    precio_final, 
    descuento_aplicado, 
    activo
) VALUES (?, date('now'), ?, ?, ?, 1)
"""

UPDATE_ALQUILER_FINALIZADO = """
UPDATE alquileres 
SET activo = 0, fecha_fin = date('now')
WHERE id = ? AND activo = 1
""" 