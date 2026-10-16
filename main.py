from Funciones.VentaPasaje import VentaPasajes
from Menu import menu_inicio, menu_principal
from Funciones.ReservaPasaje import VerReserva, CancelarReserva
from Funciones.Registro import registro, login


def main():

    while True:
        try:
            opcion = int(menu_principal())

            if opcion == 1:
                opcion = int(menu_ventas())

                if opcion == 1:
                    
                if opcion == 2:

                if opcion == 3:

                if opcion == 4:

                if opcion == 5:

                else:
                    print("Saliendo...")
                    break

            elif opcion == 2:
                opcion = int(menu_consultas())

                if opcion == 1:

                if opcion == 2:

                if opcion == 3:

                else:

            elif opcion == 3:
                opcion = int(menu_viajes())

                if opcion == 1:

                if opcion == 2:

                if opcion == 3:

                else:

            else:
                print("Saliendo...")

        except ValueError:
            print("Error: Ingrese un número válido.")
