import math
from typing import Tuple
from models import Vehiculo

class CalculadoraService:
    # Constante de decaimiento para el cálculo de descuentos
    K_DECAIMIENTO = 0.05

    # Factores de ajuste por tipo de vehículo
    FACTORES_TIPO = {
        'economico': 0.8,
        'medio': 1.0,
        'premium': 1.2
    }

    @classmethod
    def calcular_descuento_tiempo(cls, dias: int, precio_base: float) -> Tuple[float, float]:
        """
        Se realiza el calculo del descuento usando una función exponencial y su derivada
        La función base es: f(x) = precio_base * (1 - e^(-k*x))
        La derivada es: f'(x) = precio_base * k * e^(-k*x)
        
        Args:
            dias: Número de días de alquiler
            precio_base: Precio base por día del vehículo

        Returns:
            Tuple con (descuento, tasa_cambio)
        """
        # Función principal de descuento
        descuento = precio_base * (1 - math.exp(-cls.K_DECAIMIENTO * dias))
        
        # Derivada para calcular la tasa de cambio del descuento
        tasa_cambio = precio_base * cls.K_DECAIMIENTO * math.exp(-cls.K_DECAIMIENTO * dias)
        
        return descuento, tasa_cambio
    
    @classmethod
    def calcular_precio_final(cls, vehiculo: Vehiculo, dias: int) -> Tuple[float, float]:
        """
        Calcula el precio final y el descuento para un alquiler
        
        Args:
            vehiculo: Instancia de Vehiculo
            dias: Número de días de alquiler

        Returns:
            Tuple con (precio_final, descuento)
        """
        factor = cls.FACTORES_TIPO.get(vehiculo.tipo_normalizado, 1.0)
        descuento, _ = cls.calcular_descuento_tiempo(dias, vehiculo.precio_base)
        
        precio_final = (vehiculo.precio_base * dias * factor) - descuento
        return max(precio_final, 0), descuento  # Aseguramos que el precio no sea negativo 