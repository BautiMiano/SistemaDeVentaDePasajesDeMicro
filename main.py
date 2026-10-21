from Funciones.VentaPasaje import VentaPasajes
from Menu import menu_principal, menu_consultas, menu_ventas, menu_viajes, menu_micros
from Funciones.ReservaPasaje import VerReserva, CancelarReserva, AgregarReserva
from Funciones.Registro import registro, login
from Pasajes import RegistrarViaje, VerViajes, RegistrarMicro, DarBajaMicro, VerMicros, VerDestinos


def main():
    opcion = int(menu_principal())
    while True:
        try:

            if opcion == 1: #MENU VENTAS
                opcion = int(menu_ventas())

                if opcion == 1:
                    #Registrar venta de pasaje
                    AgregarReserva()

                if opcion == 2:
                    #Ver ventas
                    print("No disponible")

                if opcion == 3:
                    #Buscar ventas
                    print("No disponible")

                if opcion == 4:
                    #Modificar ventas
                    print("No disponible")

                if opcion == 5:
                    #Cancelar ventas
                    CancelarReserva()

                else:
                    opcion = int(menu_principal())

            elif opcion == 2: #MENU CONSULTAS
                opcion = int(menu_consultas())

                if opcion == 1:
                    #Ventas por destino
                    print("No disponible")

                if opcion == 2:
                    #Ventas por fecha
                    print("No disponible")

                if opcion == 3:
                    #Ventas por usuario
                    print("No disponible")

                else:
                    opcion = int(menu_principal())

            elif opcion == 3: #MENU VIAJES
                opcion = int(menu_viajes())

                if opcion == 1:
                    #Consultar disponibilidad
                    VerViajes()

                if opcion == 2:
                    #Agregar destinos
                    RegistrarViaje()

                if opcion == 3:
                    #Ver destinos
                    VerDestinos()

                if opcion == 4:
                    #Eliminar destinos
                    print("No disponible")

                else:
                    opcion = int(menu_principal())

            elif opcion == 4: #MENU MICROS
                opcion = int(menu_micros())
                if opcion == 1:
                    #Ver micros
                    VerMicros()

                if opcion == 2:
                    #Registrar micros
                    RegistrarMicro()

                if opcion == 3:
                    #Dar de baja
                    DarBajaMicro()

                else:
                    opcion = int(menu_principal())

            else:
                print("Saliendo...")
                break

        except ValueError:
            print("Error: Ingrese un número válido.")

main()