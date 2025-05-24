from typing import Optional, List
import os
from models import Vehiculo, Alquiler
from services import DatabaseService, CalculadoraService
from colorama import init, Fore, Style
from tabulate import tabulate
from utils.performance_test import medir_tiempo

class ConsoleUI:
    def __init__(self):
        self.db = DatabaseService()
        self.calculadora = CalculadoraService()
        init(autoreset=True)  # Inicializar colorama

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_titulo(self, titulo: str):
        """Muestra un título formateado"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {titulo} ==={Style.RESET_ALL}")

    def input_seguro(self, mensaje: str) -> str:
        """Maneja la entrada de usuario de manera segura"""
        try:
            return input(mensaje)
        except (KeyboardInterrupt, EOFError):
            print()  # Nueva línea para mejor presentación
            raise KeyboardInterrupt
        except:
            return ""

    def mostrar_menu(self) -> str:
        """Muestra el menú principal y retorna la opción seleccionada"""
        self.limpiar_pantalla()
        self.mostrar_titulo("Sistema de Alquiler de Vehículos")
        print(f"{Fore.GREEN}1. Ver vehículos disponibles")
        print(f"{Fore.RED}2. Ver vehículos alquilados")
        print(f"{Fore.YELLOW}3. Registrar nuevo vehículo")
        print(f"{Fore.BLUE}4. Iniciar alquiler")
        print(f"{Fore.MAGENTA}5. Finalizar alquiler")
        print(f"{Fore.CYAN}6. Ver historial de alquileres")
        print(f"{Fore.WHITE}7. Salir")
        return self.input_seguro(f"\n{Fore.GREEN}Seleccione una opción: {Style.RESET_ALL}")

    @medir_tiempo("Mostrar Vehículos")
    def mostrar_vehiculos(self, vehiculos: List[Vehiculo], titulo: str):
        """Muestra una lista de vehículos en formato de tabla"""
        self.mostrar_titulo(titulo)
        if not vehiculos:
            print(f"\n{Fore.YELLOW}No hay vehículos {titulo.lower()} por el momento.{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}")
            return

        # Preparar datos para la tabla
        headers = ["ID", "Modelo", "Tipo", "Precio/día"]
        tabla = [
            [
                f"{Fore.CYAN}{v.id}{Style.RESET_ALL}",
                v.modelo,
                v.tipo.capitalize(),
                f"USD ${v.precio_base:,.2f}"
            ] for v in vehiculos
        ]
        
        print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))
        input(f"\n{Fore.GREEN}Presione Enter para continuar...{Style.RESET_ALL}")

    def registrar_vehiculo(self):
        """Maneja el registro de un nuevo vehículo"""
        self.mostrar_titulo("Registrar Nuevo Vehículo")
        try:
            modelo = self.input_seguro(f"{Fore.CYAN}Ingrese el modelo del vehículo: {Style.RESET_ALL}")
            if not modelo:
                return
            
            while True:
                tipo = self.input_seguro(f"{Fore.CYAN}Ingrese el tipo (economico/medio/premium): {Style.RESET_ALL}").lower()
                if not tipo:
                    return
                if tipo in ['economico', 'medio', 'premium']:
                    break
                print(f"{Fore.RED}Tipo inválido. Por favor, intente nuevamente.{Style.RESET_ALL}")
            
            while True:
                try:
                    precio_str = self.input_seguro(f"{Fore.CYAN}Ingrese el precio base por día (en USD): {Style.RESET_ALL}")
                    if not precio_str:
                        return
                    precio_base = float(precio_str)
                    if precio_base > 0:
                        break
                    print(f"{Fore.RED}El precio debe ser mayor a 0.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Por favor, ingrese un número válido.{Style.RESET_ALL}")
            
            vehiculo = Vehiculo(modelo=modelo, tipo=tipo, precio_base=precio_base)
            vehiculo_id = self.db.agregar_vehiculo(vehiculo)
            print(f"\n{Fore.GREEN}¡Vehículo registrado exitosamente con ID: {vehiculo_id}!{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Registro cancelado.{Style.RESET_ALL}")
        finally:
            input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}")

    def finalizar_alquiler(self):
        """Maneja la finalización de un alquiler activo"""
        self.mostrar_titulo("Finalizar Alquiler")
        alquileres = self.db.obtener_alquileres_activos()
        
        if not alquileres:
            print(f"{Fore.YELLOW}No hay alquileres activos para finalizar.")
            input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}")
            return

        # Mostrar alquileres activos en tabla
        headers = ["ID", "Vehículo", "Inicio", "Días", "Precio Final"]
        tabla = [
            [
                f"{Fore.CYAN}{a['id']}{Style.RESET_ALL}",
                f"{a['modelo']} ({a['tipo']})",
                a['fecha_inicio'],
                a['dias'],
                f"USD ${a['precio_final']:,.2f}"
            ] for a in alquileres
        ]
        
        print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))
        
        while True:
            try:
                alquiler_id = int(input(f"\n{Fore.CYAN}Ingrese el ID del alquiler a finalizar: {Style.RESET_ALL}"))
                if self.db.finalizar_alquiler(alquiler_id):
                    print(f"\n{Fore.GREEN}¡Alquiler finalizado exitosamente!{Style.RESET_ALL}")
                    break
                print(f"{Fore.RED}ID de alquiler inválido o ya finalizado.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Por favor, ingrese un número válido.{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}")

    @medir_tiempo("Mostrar Historial")
    def mostrar_historial(self):
        """Muestra el historial de alquileres en formato de tabla"""
        self.mostrar_titulo("Historial de Alquileres")
        alquileres = self.db.obtener_historial_alquileres()
        
        if not alquileres:
            print(f"{Fore.YELLOW}No hay alquileres registrados.")
            input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}")
            return

        # Preparar datos para la tabla
        headers = ["ID", "Vehículo", "Inicio", "Estado", "Días", "Descuento", "Total"]
        tabla = [
            [
                f"{Fore.CYAN}{a['id']}{Style.RESET_ALL}",
                f"{a['modelo']} ({a['tipo']})",
                a['fecha_inicio'],
                f"{Fore.GREEN}Activo{Style.RESET_ALL}" if a.get('activo', 0) else f"{Fore.RED}Finalizado{Style.RESET_ALL}",
                a['dias'],
                f"USD ${a['descuento_aplicado']:,.2f}",
                f"USD ${a['precio_final']:,.2f}"
            ] for a in alquileres
        ]
        
        print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))
        input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}")

    def seleccionar_vehiculo(self) -> Optional[Vehiculo]:
        """Permite al usuario seleccionar un vehículo disponible"""
        vehiculos = self.db.obtener_vehiculos_disponibles()
        if not vehiculos:
            print(f"{Fore.YELLOW}No hay vehículos disponibles.")
            input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}")
            return None

        # Mostrar vehículos en tabla
        headers = ["ID", "Modelo", "Tipo", "Precio/día"]
        tabla = [
            [
                f"{Fore.CYAN}{v.id}{Style.RESET_ALL}",
                v.modelo,
                v.tipo.capitalize(),
                f"USD ${v.precio_base:,.2f}"
            ] for v in vehiculos
        ]
        
        print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))
        
        while True:
            try:
                vehiculo_id = int(input(f"\n{Fore.CYAN}Seleccione el ID del vehículo: {Style.RESET_ALL}"))
                vehiculo = next((v for v in vehiculos if v.id == vehiculo_id), None)
                if vehiculo:
                    return vehiculo
                print(f"{Fore.RED}ID de vehículo inválido.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Por favor, ingrese un número válido.{Style.RESET_ALL}")

    @medir_tiempo("Calcular Alquiler")
    def calcular_alquiler(self):
        """Maneja el cálculo y registro de un nuevo alquiler"""
        self.mostrar_titulo("Iniciar Nuevo Alquiler")
        vehiculo = self.seleccionar_vehiculo()
        if not vehiculo:
            return
        
        while True:
            try:
                dias = int(input(f"{Fore.CYAN}Ingrese la cantidad de días de alquiler: {Style.RESET_ALL}"))
                if dias > 0:
                    break
                print(f"{Fore.RED}La cantidad de días debe ser mayor a 0.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Por favor, ingrese un número válido.{Style.RESET_ALL}")
        
        # Calcular precio y descuento
        precio_final, descuento = self.calculadora.calcular_precio_final(vehiculo, dias)
        _, tasa_cambio = self.calculadora.calcular_descuento_tiempo(dias, vehiculo.precio_base)
        
        # Mostrar resumen en tabla
        print("\n=== Resumen del Alquiler ===")
        resumen = [
            ["Vehículo", f"{vehiculo.modelo} ({vehiculo.tipo})"],
            ["Días", str(dias)],
            ["Precio base total", f"USD ${vehiculo.precio_base * dias:,.2f}"],
            ["Descuento", f"USD ${descuento:,.2f}"],
            ["Tasa de descuento", f"USD ${tasa_cambio:,.2f}/día"],
            [f"{Fore.GREEN}Precio final{Style.RESET_ALL}", f"{Fore.GREEN}USD ${precio_final:,.2f}{Style.RESET_ALL}"]
        ]
        print(tabulate(resumen, tablefmt="fancy_grid"))
        
        if input(f"\n{Fore.CYAN}¿Confirmar alquiler? (s/n): {Style.RESET_ALL}").lower() == 's':
            alquiler = Alquiler(
                vehiculo_id=vehiculo.id,
                dias=dias,
                precio_final=precio_final,
                descuento_aplicado=descuento
            )
            self.db.registrar_alquiler(alquiler)
            print(f"\n{Fore.GREEN}¡Alquiler registrado exitosamente!{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}")

    def ejecutar(self):
        """Ejecuta el bucle principal de la aplicación"""
        while True:
            try:
                opcion = self.mostrar_menu()
                self.limpiar_pantalla()
                
                if opcion == '1':
                    self.mostrar_vehiculos(
                        self.db.obtener_vehiculos_disponibles(),
                        "Vehículos Disponibles"
                    )
                
                elif opcion == '2':
                    self.mostrar_vehiculos(
                        self.db.obtener_vehiculos_alquilados(),
                        "Vehículos Alquilados"
                    )
                
                elif opcion == '3':
                    self.registrar_vehiculo()
                
                elif opcion == '4':
                    self.calcular_alquiler()
                
                elif opcion == '5':
                    self.finalizar_alquiler()
                
                elif opcion == '6':
                    self.mostrar_historial()
                
                elif opcion == '7':
                    self.limpiar_pantalla()
                    print(f"\n{Fore.GREEN}¡Gracias por usar el sistema!{Style.RESET_ALL}")
                    break
                
                else:
                    print(f"\n{Fore.RED}Opción inválida. Por favor, intente nuevamente.{Style.RESET_ALL}")
                    input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}")
            
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}") 