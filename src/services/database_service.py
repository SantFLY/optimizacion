import sqlite3
import os
from typing import List, Dict, Optional
from models import Vehiculo, Alquiler
from database.queries import *
from utils.performance_test import medir_tiempo
from services.cache_service import CacheService

class DatabaseService:
    def __init__(self):
        # Obtener la ruta base del proyecto (un nivel arriba de src)
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Configurar las rutas
        self.db_dir = os.path.join(self.project_root, "src", "database")
        self.db_path = os.path.join(self.db_dir, "alquiler_vehiculos.db")
        
        # Asegurar que la carpeta database existe
        os.makedirs(self.db_dir, exist_ok=True)
        
        self.cache = CacheService(ttl_seconds=300)  # 5 minutos de TTL
        self._inicializar_db()

    def _get_connection(self):
        """Obtiene una conexión optimizada a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _inicializar_db(self):
        """Inicializa la base de datos con las tablas necesarias e índices"""
        with self._get_connection() as conn:
            # Crear tablas
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vehiculos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    modelo TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    precio_base REAL NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS alquileres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehiculo_id INTEGER NOT NULL,
                    fecha_inicio TEXT NOT NULL,
                    fecha_fin TEXT,
                    dias INTEGER NOT NULL,
                    precio_final REAL NOT NULL,
                    descuento_aplicado REAL NOT NULL,
                    activo INTEGER DEFAULT 1,
                    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos (id)
                )
            """)

            # Crear índices optimizados
            conn.execute("CREATE INDEX IF NOT EXISTS idx_vehiculos_tipo ON vehiculos(tipo)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_alquileres_activo ON alquileres(activo)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_alquileres_vehiculo ON alquileres(vehiculo_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_alquileres_fecha ON alquileres(fecha_inicio)")
            
            # Optimizar la base de datos
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")  # Write-Ahead Logging
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA temp_store = MEMORY")
            conn.execute("PRAGMA mmap_size = 30000000000")
            conn.execute("PRAGMA cache_size = -2000")  # 2MB de caché

            conn.commit()

    def __del__(self):
        """Destructor para asegurar que volvemos al directorio original"""
        if hasattr(self, 'original_dir'):
            os.chdir(self.original_dir)

    @medir_tiempo("DB: Obtener Vehículos Disponibles")
    def obtener_vehiculos_disponibles(self) -> List[Vehiculo]:
        # Intentar obtener del caché
        cached = self.cache.get('vehiculos_disponibles')
        if cached is not None:
            return cached

        with self._get_connection() as conn:
            cursor = conn.execute(GET_VEHICULOS_DISPONIBLES)
            vehiculos = [
                Vehiculo(
                    id=row['id'],
                    modelo=row['modelo'],
                    tipo=row['tipo'],
                    precio_base=row['precio_base']
                ) for row in cursor.fetchall()
            ]
            self.cache.set('vehiculos_disponibles', vehiculos)
            return vehiculos

    @medir_tiempo("DB: Obtener Vehículos Alquilados")
    def obtener_vehiculos_alquilados(self) -> List[Vehiculo]:
        # Intentar obtener del caché
        cached = self.cache.get('vehiculos_alquilados')
        if cached is not None:
            return cached

        with self._get_connection() as conn:
            cursor = conn.execute(GET_VEHICULOS_ALQUILADOS)
            vehiculos = [
                Vehiculo(
                    id=row['id'],
                    modelo=row['modelo'],
                    tipo=row['tipo'],
                    precio_base=row['precio_base']
                ) for row in cursor.fetchall()
            ]
            self.cache.set('vehiculos_alquilados', vehiculos)
            return vehiculos

    @medir_tiempo("DB: Agregar Vehículo")
    def agregar_vehiculo(self, vehiculo: Vehiculo) -> int:
        with self._get_connection() as conn:
            cursor = conn.execute(
                INSERT_VEHICULO,
                (vehiculo.modelo, vehiculo.tipo, vehiculo.precio_base)
            )
            conn.commit()
            # Invalidar caché relacionado
            self.cache.invalidate('vehiculos_disponibles')
            self.cache.invalidate('vehiculos_alquilados')
            return cursor.lastrowid

    @medir_tiempo("DB: Registrar Alquiler")
    def registrar_alquiler(self, alquiler: Alquiler) -> int:
        with self._get_connection() as conn:
            cursor = conn.execute(
                INSERT_ALQUILER,
                (
                    alquiler.vehiculo_id,
                    alquiler.dias,
                    alquiler.precio_final,
                    alquiler.descuento_aplicado
                )
            )
            conn.commit()
            # Invalidar caché
            self.cache.invalidate('vehiculos_disponibles')
            self.cache.invalidate('vehiculos_alquilados')
            self.cache.invalidate('alquileres_activos')
            self.cache.invalidate('historial_alquileres')
            return cursor.lastrowid

    @medir_tiempo("DB: Finalizar Alquiler")
    def finalizar_alquiler(self, alquiler_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.execute(UPDATE_ALQUILER_FINALIZADO, (alquiler_id,))
            conn.commit()
            # Invalidar caché
            self.cache.invalidate('vehiculos_disponibles')
            self.cache.invalidate('vehiculos_alquilados')
            self.cache.invalidate('alquileres_activos')
            self.cache.invalidate('historial_alquileres')
            return cursor.rowcount > 0

    @medir_tiempo("DB: Obtener Historial")
    def obtener_historial_alquileres(self) -> List[Dict]:
        # Intentar obtener del caché
        cached = self.cache.get('historial_alquileres')
        if cached is not None:
            return cached

        with self._get_connection() as conn:
            cursor = conn.execute(GET_HISTORIAL_ALQUILERES)
            historial = [dict(row) for row in cursor.fetchall()]
            self.cache.set('historial_alquileres', historial)
            return historial

    @medir_tiempo("DB: Obtener Alquileres Activos")
    def obtener_alquileres_activos(self) -> List[Dict]:
        # Intentar obtener del caché
        cached = self.cache.get('alquileres_activos')
        if cached is not None:
            return cached

        with self._get_connection() as conn:
            cursor = conn.execute(GET_ALQUILERES_ACTIVOS)
            alquileres = [dict(row) for row in cursor.fetchall()]
            self.cache.set('alquileres_activos', alquileres)
            return alquileres

    def agregar_vehiculos_lote(self, vehiculos: List[Vehiculo]) -> List[int]:
        """Agrega múltiples vehículos en una sola transacción"""
        with self._get_connection() as conn:
            cursor = conn.executemany(
                INSERT_VEHICULO,
                [(v.modelo, v.tipo, v.precio_base) for v in vehiculos]
            )
            conn.commit()
            # Invalidar caché
            self.cache.invalidate('vehiculos_disponibles')
            return [cursor.lastrowid - i for i in range(len(vehiculos)-1, -1, -1)] 