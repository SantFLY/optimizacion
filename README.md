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
├── src/                    # Código fuente principal
│   ├── database/          # Gestión de base de datos y consultas SQL
│   ├── models/            # Modelos de datos (Vehiculo, Alquiler, etc.)
│   ├── services/          # Servicios de negocio y lógica de la aplicación
│   ├── tests/             # Pruebas unitarias y de rendimiento
│   ├── utils/             # Utilidades y funciones auxiliares
│   ├── ui/                # Interfaz de usuario y componentes de consola
│   ├── config/            # Configuraciones y constantes
│   ├── logs/              # Archivos de registro
│   ├── main.py           # Punto de entrada principal
│   └── run_performance_tests.py  # Script para pruebas de rendimiento
│
├── Archivos Ejecutables/   # Scripts de ejecución
│   ├── Instalar dependencias.bat     # Script para instalar dependencias
│   ├── ejecucion_normal.bat          # Script para ejecución normal
│   └── ejecucion_pruebas_rendimiento.bat  # Script para pruebas de rendimiento
│
├── database/              # Archivos de base de datos SQLite
├── requirements.txt       # Dependencias del proyecto
├── LICENSE               # Archivo de licencia MIT
└── README.md             # Este archivo
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

El proyecto incluye tres archivos ejecutables (.bat) para facilitar su uso:

### 1. `Instalar dependencias.bat`
Este archivo instala todas las dependencias necesarias del proyecto.
- **Uso**: Ejecutar este archivo la primera vez o cuando se necesite actualizar las dependencias
- **Propósito**: Configuración inicial del proyecto

### 2. `ejecucion_normal.bat`
Este archivo ejecuta el programa principal con la funcionalidad estándar.
- **Uso**: Usar este archivo para el uso diario del programa
- **Propósito**: Iniciar la aplicación en modo normal

### 3. `ejecucion_pruebas_rendimiento.bat`
Este archivo ejecuta las pruebas de rendimiento del sistema.
- **Uso**: Usar cuando se quiera evaluar el rendimiento
- **Propósito**: Realizar pruebas de optimización

**Nota**: Asegúrate de tener Python instalado en tu sistema antes de ejecutar cualquiera de los archivos.

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