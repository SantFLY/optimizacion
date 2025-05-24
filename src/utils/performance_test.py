import time
from typing import Callable
from functools import wraps

def medir_tiempo(nombre: str):
    def decorador(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            inicio = time.time()
            resultado = func(*args, **kwargs)
            fin = time.time()
            tiempo_total = (fin - inicio) * 1000  # Convertir a milisegundos
            print(f"\033[33m[RENDIMIENTO] {nombre}: {tiempo_total:.2f}ms\033[0m")
            return resultado
        return wrapper
    return decorador 