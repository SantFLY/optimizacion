from dataclasses import dataclass
from typing import Optional

@dataclass
class Vehiculo:
    modelo: str
    tipo: str
    precio_base: float
    id: Optional[int] = None
    disponible: bool = True

    @property
    def tipo_normalizado(self) -> str:
        """Retorna el tipo de vehículo normalizado"""
        return self.tipo.lower()

    def __str__(self) -> str:
        return f"{self.modelo} ({self.tipo}) - USD ${self.precio_base:,.2f}/día" 