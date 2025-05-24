import sqlite3
import os
from typing import List, Optional
from models import Vehiculo, Alquiler
from datetime import datetime

class DatabaseService:
    def __init__(self, db_name: str = 'alquiler_vehiculos.db'):
        """
        Inicializa el servicio de base de datos
        
        Args:
            db_name: Nombre del archivo de base de datos
        """
        os.makedirs('database', exist_ok=True)
        self.db_path = os.path.join('database', db_name)
        self.inicializar_db()
        self.migrar_db()  # Ejecutar migraciones si son necesarias

    def migrar_db(self):
        """Realiza las migraciones necesarias en la base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Verificar si la columna activo existe
            cursor.execute("PRAGMA table_info(alquileres)")
            columnas = [info[1] for info in cursor.fetchall()]
            
            if 'activo' not in columnas:
                # Crear tabla temporal con la nueva estructura
                cursor.execute('''
                    CREATE TABLE alquileres_temp (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        vehiculo_id INTEGER,
                        fecha_inicio TEXT NOT NULL,
                        fecha_fin TEXT,
                        dias INTEGER NOT NULL,
                        precio_final REAL NOT NULL,
                        descuento_aplicado REAL NOT NULL,
                        activo BOOLEAN DEFAULT 1,
                        FOREIGN KEY (vehiculo_id) REFERENCES vehiculos (id)
                    )
                ''')
                
                # Copiar datos existentes
                cursor.execute('''
                    INSERT INTO alquileres_temp 
                    (id, vehiculo_id, fecha_inicio, dias, precio_final, descuento_aplicado, activo)
                    SELECT id, vehiculo_id, fecha_inicio, dias, precio_final, descuento_aplicado, 1
                    FROM alquileres
                ''')
                
                # Eliminar tabla antigua y renombrar la nueva
                cursor.execute('DROP TABLE alquileres')
                cursor.execute('ALTER TABLE alquileres_temp RENAME TO alquileres')
            
            conn.commit()

    def inicializar_db(self):
        """Inicializa la base de datos con las tablas necesarias"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla de vehículos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vehiculos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    modelo TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    precio_base REAL NOT NULL,
                    disponible BOOLEAN DEFAULT 1
                )
            ''')
            
            # Tabla de alquileres
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alquileres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehiculo_id INTEGER,
                    fecha_inicio TEXT NOT NULL,
                    fecha_fin TEXT,
                    dias INTEGER NOT NULL,
                    precio_final REAL NOT NULL,
                    descuento_aplicado REAL NOT NULL,
                    activo BOOLEAN DEFAULT 1,
                    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos (id)
                )
            ''')
            
            conn.commit()

    def agregar_vehiculo(self, vehiculo: Vehiculo) -> int:
        """
        Agrega un nuevo vehículo a la base de datos
        
        Args:
            vehiculo: Instancia de Vehiculo a agregar

        Returns:
            ID del vehículo agregado
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO vehiculos (modelo, tipo, precio_base, disponible) VALUES (?, ?, ?, ?)',
                (vehiculo.modelo, vehiculo.tipo, vehiculo.precio_base, vehiculo.disponible)
            )
            conn.commit()
            return cursor.lastrowid

    def obtener_vehiculo(self, vehiculo_id: int) -> Optional[Vehiculo]:
        """
        Obtiene un vehículo por su ID
        
        Args:
            vehiculo_id: ID del vehículo a buscar

        Returns:
            Instancia de Vehiculo o None si no existe
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM vehiculos WHERE id = ?', (vehiculo_id,))
            row = cursor.fetchone()
            
            if row:
                return Vehiculo(
                    id=row[0],
                    modelo=row[1],
                    tipo=row[2],
                    precio_base=row[3],
                    disponible=bool(row[4])
                )
            return None

    def obtener_vehiculos_disponibles(self) -> List[Vehiculo]:
        """
        Obtiene la lista de vehículos disponibles
        
        Returns:
            Lista de instancias de Vehiculo
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM vehiculos WHERE disponible = 1')
            return [
                Vehiculo(
                    id=row[0],
                    modelo=row[1],
                    tipo=row[2],
                    precio_base=row[3],
                    disponible=bool(row[4])
                )
                for row in cursor.fetchall()
            ]

    def actualizar_disponibilidad_vehiculo(self, vehiculo_id: int, disponible: bool) -> bool:
        """
        Actualiza el estado de disponibilidad de un vehículo
        
        Args:
            vehiculo_id: ID del vehículo
            disponible: Nuevo estado de disponibilidad

        Returns:
            True si se actualizó correctamente, False si no
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE vehiculos SET disponible = ? WHERE id = ?',
                (disponible, vehiculo_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def obtener_vehiculos_alquilados(self) -> List[Vehiculo]:
        """
        Obtiene la lista de vehículos que están alquilados
        
        Returns:
            Lista de instancias de Vehiculo
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM vehiculos WHERE disponible = 0')
            return [
                Vehiculo(
                    id=row[0],
                    modelo=row[1],
                    tipo=row[2],
                    precio_base=row[3],
                    disponible=bool(row[4])
                )
                for row in cursor.fetchall()
            ]

    def obtener_alquileres_activos(self) -> List[dict]:
        """
        Obtiene la lista de alquileres activos
        
        Returns:
            Lista de diccionarios con la información de los alquileres activos
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.*, v.modelo, v.tipo
                FROM alquileres a
                JOIN vehiculos v ON a.vehiculo_id = v.id
                WHERE a.activo = 1
                ORDER BY a.fecha_inicio DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]

    def finalizar_alquiler(self, alquiler_id: int) -> bool:
        """
        Finaliza un alquiler y marca el vehículo como disponible
        
        Args:
            alquiler_id: ID del alquiler a finalizar

        Returns:
            True si se finalizó correctamente, False si no
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                # Iniciar transacción
                cursor.execute('BEGIN TRANSACTION')
                
                # Obtener el vehiculo_id del alquiler
                cursor.execute('SELECT vehiculo_id FROM alquileres WHERE id = ?', (alquiler_id,))
                result = cursor.fetchone()
                if not result:
                    return False
                
                vehiculo_id = result[0]
                
                # Actualizar el alquiler
                cursor.execute('''
                    UPDATE alquileres 
                    SET activo = 0, fecha_fin = ? 
                    WHERE id = ? AND activo = 1
                ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), alquiler_id))
                
                if cursor.rowcount == 0:
                    return False
                
                # Marcar el vehículo como disponible
                cursor.execute(
                    'UPDATE vehiculos SET disponible = 1 WHERE id = ?',
                    (vehiculo_id,)
                )
                
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False

    def registrar_alquiler(self, alquiler: Alquiler) -> int:
        """
        Registra un nuevo alquiler en la base de datos y marca el vehículo como no disponible
        
        Args:
            alquiler: Instancia de Alquiler a registrar

        Returns:
            ID del alquiler registrado
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                # Iniciar transacción
                cursor.execute('BEGIN TRANSACTION')
                
                # Registrar el alquiler
                cursor.execute(
                    '''INSERT INTO alquileres 
                       (vehiculo_id, fecha_inicio, dias, precio_final, descuento_aplicado, activo)
                       VALUES (?, ?, ?, ?, ?, 1)''',
                    (alquiler.vehiculo_id, alquiler.fecha_inicio, alquiler.dias,
                     alquiler.precio_final, alquiler.descuento_aplicado)
                )
                
                # Marcar vehículo como no disponible
                cursor.execute(
                    'UPDATE vehiculos SET disponible = 0 WHERE id = ?',
                    (alquiler.vehiculo_id,)
                )
                
                # Confirmar transacción
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                # Si algo sale mal, revertir cambios
                conn.rollback()
                raise e

    def obtener_historial_alquileres(self) -> List[dict]:
        """
        Obtiene el historial completo de alquileres
        
        Returns:
            Lista de diccionarios con la información de los alquileres
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.*, v.modelo, v.tipo
                FROM alquileres a
                JOIN vehiculos v ON a.vehiculo_id = v.id
                ORDER BY a.fecha_inicio DESC
            ''')
            return [dict(row) for row in cursor.fetchall()] 