"""
Script para ejecutar pruebas de rendimiento del sistema de alquiler de vehículos
"""
from tests.performance_test import PruebasRendimiento

if __name__ == "__main__":
    print("Ejecutando pruebas de rendimiento...")
    pruebas = PruebasRendimiento()
    pruebas.ejecutar_pruebas() 