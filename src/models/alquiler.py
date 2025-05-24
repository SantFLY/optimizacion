from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Alquiler:
    vehiculo_id: int
    dias: int
    precio_final: float
    descuento_aplicado: float
    fecha_inicio: str = None
    id: Optional[int] = None

    def __post_init__(self):
        if self.fecha_inicio is None:
            self.fecha_inicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self) -> str:
        return f"Alquiler por {self.dias} días - Descuento: ${self.descuento_aplicado:.2f} - Total: ${self.precio_final:.2f}" 