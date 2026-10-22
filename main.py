from Funciones.VentaPasaje import VentaPasajes
from Menu import menu_principal, menu_consultas, menu_ventas, menu_viajes, menu_micros
from Funciones.ReservaPasaje import VerReserva, CancelarReserva, AgregarReserva
from Funciones.Registro import registro, login
from Pasajes import RegistrarViaje, VerViajes, RegistrarMicro, DarBajaMicro, VerMicros, VerDestinos


def main():
    
    while True:
        try:
            opcion = int(menu_principal())

            if opcion < 1 or opcion > 5:
                print("Error: Ingrese un numero válido.")
                continue

            if opcion == 1: #MENU VENTAS

                while True:

                    opcion = int(menu_ventas())

                    if opcion < 1 or opcion > 6:
                        print("Error: Ingrese un numero válido.")
                        continue

                    if opcion == 1:
                        #Registrar venta de pasaje
                        AgregarReserva()

                    elif opcion == 2:
                        #Ver ventas
                        print("No disponible")

                    elif opcion == 3:
                        #Buscar ventas
                        print("No disponible")

                    elif opcion == 4:
                        #Modificar ventas
                        print("No disponible")

                    elif opcion == 5:
                        #Cancelar ventas
                        print("No disponible")

                    else:
                        break

            elif opcion == 2: #MENU CONSULTAS

                while True:
                    opcion = int(menu_consultas())

                    if opcion < 1 or opcion > 4:
                        print("Error: Ingrese un numero válido.")
                        continue
                    
                    if opcion == 1:
                        #Ventas por destino
                        print("No disponible")

                    elif opcion == 2:
                        #Ventas por fecha
                        print("No disponible")

                    elif opcion == 3:
                        #Ventas por usuario
                        print("No disponible")

                    else:
                        break

            elif opcion == 3: #MENU VIAJES
                
                while True:
                    opcion = int(menu_viajes())

                    if opcion < 1 or opcion > 5:
                        print("Error: Ingrese un numero válido.")
                        continue

                    if opcion == 1:
                        #Consultar disponibilidad
                        VerViajes()

                    elif opcion == 2:
                        #Agregar destinos
                        RegistrarViaje()

                    elif opcion == 3:
                        #Ver destinos
                        VerDestinos()

                    elif opcion == 4:
                        #Eliminar destinos
                        print("No disponible")

                    else:
                        break

            elif opcion == 4: #MENU MICROS

                while True:
                    opcion = int(menu_micros())

                    if opcion < 1 or opcion > 4:
                        print("Error: Ingrese un numero válido.")
                        continue

                    if opcion == 1:
                        #Ver micros
                        VerMicros()

                    elif opcion == 2:
                        #Registrar micros
                        RegistrarMicro()

                    elif opcion == 3:
                        #Dar de baja
                        DarBajaMicro()

                    else:
                        break

            else:
                print("Saliendo...")
                break

        except ValueError:
            print("Error: Ingrese un número válido.")

main()