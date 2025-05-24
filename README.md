# Sistema de Gestión de Alquiler de Vehículos 🚗

Sistema optimizado para la gestión de alquiler de vehículos con interfaz de consola, desarrollado en Python.

## Características Principales ✨

- Gestión completa de vehículos y alquileres
- Sistema de caché con TTL de 5 minutos
- Base de datos SQLite optimizada
- Interfaz de consola con colores
- Sistema de medición de rendimiento
- Cálculo de descuentos dinámicos

## Requisitos 📋

- Python 3.7+
- SQLite3
- Dependencias listadas en `requirements.txt`

## Instalación 🔧

1. Clonar el repositorio:
```bash
git clone <https://github.com/SantFLY/optimizacion>
cd <opyimizacion>
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Estructura del Proyecto 📁

```
src/
├── database/          # Archivos de base de datos y consultas SQL
├── models/           # Modelos de datos (Vehiculo, Alquiler)
├── services/         # Servicios de negocio
├── tests/           # Pruebas de rendimiento
└── ui/              # Interfaz de usuario
```

## Características Técnicas 🛠️

### Base de Datos
- SQLite con modo WAL (Write-Ahead Logging)
- Índices optimizados
- Consultas eficientes con JOINs
- Sistema de caché para consultas frecuentes

### Rendimiento
- Caché con tiempo de vida de 5 minutos
- Medición de tiempos de operación
- Sistema de pruebas de rendimiento
- Optimizaciones de memoria y disco

### Cálculo de Precios
- Sistema dinámico de descuentos
- Factores por tipo de vehículo
- Función exponencial para descuentos por tiempo

## Uso 💻

1. Ejecutar la aplicación:
```bash
python src/main.py
```

2. Ejecutar pruebas de rendimiento:
```bash
python src/run_performance_tests.py
```

## Funcionalidades 📋

1. Ver vehículos disponibles
2. Ver vehículos alquilados
3. Registrar nuevo vehículo
4. Iniciar alquiler
5. Finalizar alquiler
6. Ver historial de alquileres

## Optimizaciones de Rendimiento 🚀

- Caché en memoria para consultas frecuentes
- Índices optimizados en SQLite
- Modo WAL para mejor concurrencia
- Consultas SQL optimizadas
- Manejo eficiente de memoria

## Seguridad 🔒

- Manejo seguro de transacciones
- Validación de datos de entrada
- Manejo de errores robusto
- Rollback automático en caso de fallos

## Mantenimiento 🔧

El sistema incluye herramientas para:
- Medición de rendimiento
- Limpieza de datos de prueba
- Monitoreo de operaciones
- Gestión de caché

## Contribuir 🤝

1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit de cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Crear Pull Request

## Licencia 📄

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles 
