
from Funciones.VentaPasaje import VentaPasajes
from Funciones.Menu import Menu, Salir
from Funciones.ReservaPasaje import VerReserva
from Funciones.CancelarReserva import CancelarReserva


def main():
    while True:
        opcion = Menu()
        if opcion == 1:
            VentaPasajes()
        elif opcion == 2:
            VerReserva()
        elif opcion == 3:
            CancelarReserva()
        elif opcion == 4:
            Salir()
        else:
            print("Opción inválida. Por favor, elija una opción válida.")


main()