import signal
import sys
import os
from colorama import Fore, Style, init
from ui.console_ui import ConsoleUI

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def handler_ctrl_c(signum, frame):
    """Manejador para la señal de interrupción (Ctrl+C)"""
    limpiar_pantalla()
    print(f"\n\n{Fore.YELLOW}Programa interrumpido por el usuario.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}¡Gracias por usar el sistema!{Style.RESET_ALL}")
    os._exit(0)

def main():
    """Punto de entrada principal de la aplicación"""
    init(autoreset=True)  # Inicializar colorama
    
    # Configurar el manejador de señales
    if os.name == 'nt':  # Windows
        signal.signal(signal.SIGINT, handler_ctrl_c)
        signal.signal(signal.SIGTERM, handler_ctrl_c)
    else:  # Unix/Linux
        signal.signal(signal.SIGINT, handler_ctrl_c)
        signal.signal(signal.SIGTERM, handler_ctrl_c)
    
    try:
        app = ConsoleUI()
        app.ejecutar()
    except KeyboardInterrupt:
        handler_ctrl_c(None, None)
    except Exception as e:
        print(f"\n{Fore.RED}Error inesperado: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
