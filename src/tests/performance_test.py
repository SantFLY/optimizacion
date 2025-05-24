import sys
import os
import sqlite3
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import DatabaseService
from models import Vehiculo, Alquiler
import time
from colorama import init, Fore, Style
from tabulate import tabulate
import random

class PruebasRendimiento:
    def __init__(self):
        self.db = DatabaseService()
        self.db_path = self.db.db_path
        self.id_inicial_vehiculos = None
        self.id_inicial_alquileres = None

    def obtener_ultimo_id(self, tabla):
        """Obtiene el último ID de una tabla"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(f"SELECT MAX(id) FROM {tabla}")
            resultado = cursor.fetchone()[0]
            return resultado if resultado is not None else 0

    def guardar_estado_inicial(self):
        """Guarda los IDs iniciales antes de las pruebas"""
        self.id_inicial_vehiculos = self.obtener_ultimo_id("vehiculos")
        self.id_inicial_alquileres = self.obtener_ultimo_id("alquileres")
        print(f"\n{Fore.YELLOW}Estado inicial guardado - Último ID vehiculos: {self.id_inicial_vehiculos}, Último ID alquileres: {self.id_inicial_alquileres}{Style.RESET_ALL}")

    def limpiar_datos_prueba(self):
        """Limpia solo los datos generados durante las pruebas"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                print(f"\n{Fore.YELLOW}Limpiando datos de prueba...{Style.RESET_ALL}")
                
                # Eliminar solo los registros creados durante las pruebas
                if self.id_inicial_alquileres is not None:
                    conn.execute("DELETE FROM alquileres WHERE id > ?", (self.id_inicial_alquileres,))
                
                if self.id_inicial_vehiculos is not None:
                    conn.execute("DELETE FROM vehiculos WHERE id > ?", (self.id_inicial_vehiculos,))
                
                conn.commit()
                
            # Optimizar la base de datos
            conn = sqlite3.connect(self.db_path)
            conn.execute("VACUUM")
            conn.close()
            
            print(f"{Fore.GREEN}Datos de prueba limpiados exitosamente.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error al limpiar datos de prueba: {str(e)}{Style.RESET_ALL}")

    def ejecutar_pruebas(self):
        """Ejecuta una serie de pruebas de rendimiento"""
        try:
            init(autoreset=True)
            print(f"\n{Fore.CYAN}=== Iniciando Pruebas de Rendimiento ==={Style.RESET_ALL}\n")
            
            # Guardar estado inicial
            self.guardar_estado_inicial()
            
            resultados = []
            
            # Prueba 1: Inserción de vehículos
            vehiculos_prueba = [generar_vehiculo_aleatorio() for _ in range(100)]
            def prueba_insercion():
                self.db.agregar_vehiculo(random.choice(vehiculos_prueba))
            resultados.append(medir_operacion(prueba_insercion, "Inserción de Vehículo", 50))
            
            # Prueba 2: Primera consulta de vehículos (sin caché)
            def prueba_primera_consulta():
                self.db.cache.clear()  # Limpiar caché
                self.db.obtener_vehiculos_disponibles()
            resultados.append(medir_operacion(prueba_primera_consulta, "Consulta sin Caché", 50))
            
            # Prueba 3: Consulta con caché
            def prueba_consulta_cache():
                self.db.obtener_vehiculos_disponibles()
            resultados.append(medir_operacion(prueba_consulta_cache, "Consulta con Caché", 50))
            
            # Prueba 4: Registro de alquileres
            def prueba_registro_alquiler():
                alquiler = Alquiler(
                    vehiculo_id=self.id_inicial_vehiculos + 1,  # Usar un ID válido de las pruebas
                    dias=random.randint(1, 30),
                    precio_final=random.uniform(100, 1000),
                    descuento_aplicado=random.uniform(0, 100)
                )
                self.db.registrar_alquiler(alquiler)
            resultados.append(medir_operacion(prueba_registro_alquiler, "Registro de Alquiler", 50))
            
            # Prueba 5: Consulta de historial
            def prueba_consulta_historial():
                self.db.obtener_historial_alquileres()
            resultados.append(medir_operacion(prueba_consulta_historial, "Consulta de Historial", 50))
            
            # Mostrar resultados
            headers = ["Operación", "Min (ms)", "Max (ms)", "Promedio (ms)", "Total (ms)"]
            tabla = [
                [
                    f"{Fore.CYAN}{r['nombre']}{Style.RESET_ALL}",
                    f"{r['min']:.2f}",
                    f"{r['max']:.2f}",
                    f"{r['promedio']:.2f}",
                    f"{r['total']:.2f}"
                ] for r in resultados
            ]
            
            print("\nResultados de las pruebas:")
            print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))
            print(f"\n{Fore.GREEN}Pruebas completadas exitosamente!{Style.RESET_ALL}")
        
        finally:
            # Limpiar solo los datos de prueba al finalizar
            self.limpiar_datos_prueba()

def generar_vehiculo_aleatorio():
    """Genera datos aleatorios para un vehículo"""
    modelos = ['Toyota Corolla', 'Honda Civic', 'Ford Mustang', 'BMW X5', 'Mercedes C200']
    tipos = ['economico', 'medio', 'premium']
    return Vehiculo(
        modelo=random.choice(modelos),
        tipo=random.choice(tipos),
        precio_base=random.uniform(50, 200)
    )

def medir_operacion(func, nombre, repeticiones=100):
    """Mide el tiempo de una operación específica"""
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.time()
        func()
        fin = time.time()
        tiempos.append((fin - inicio) * 1000)  # Convertir a milisegundos
    
    return {
        'nombre': nombre,
        'min': min(tiempos),
        'max': max(tiempos),
        'promedio': sum(tiempos) / len(tiempos),
        'total': sum(tiempos)
    }

if __name__ == "__main__":
    pruebas = PruebasRendimiento()
    pruebas.ejecutar_pruebas() 