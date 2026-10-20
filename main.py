from Funciones.VentaPasaje import VentaPasajes
from Menu import menu_principal, menu_consultas, menu_ventas, menu_viajes
from Funciones.ReservaPasaje import VerReserva, CancelarReserva, AgregarReserva
from Funciones.Registro import registro, login


def main():
    opcion = int(menu_principal())
    while True:
        try:

            if opcion == 1:
                opcion = int(menu_ventas())

                if opcion == 1:
                    #Registrar venta de pasaje
                    AgregarReserva()
                if opcion == 2:
                    #Ver ventas
                    VerReserva()

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

            elif opcion == 2:
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

            elif opcion == 3:
                opcion = int(menu_viajes())

                if opcion == 1:
                    #Consultar disponibilidad
                    print("No disponible")

                if opcion == 2:
                    #Agregar destinos
                    print("No disponible")

                if opcion == 3:
                    #Eliminar destinos
                    print("No disponible")

                else:
                    opcion = int(menu_principal())
            else:
                print("Saliendo...")

        except ValueError:
            print("Error: Ingrese un número válido.")

main()