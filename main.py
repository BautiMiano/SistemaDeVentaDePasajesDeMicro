from Funciones.VentaPasaje import VentaPasajes
from Menu.Menu import Menu_Sesion_Iniciada, Menu_Inicio_Sesion
from Funciones.ReservaPasaje import VerReserva
from Funciones.CancelarReserva import CancelarReserva
from Menu.Sesion import login


def main():
    Menu_Inicio_Sesion()

    while login() == True:
        print("")
        opcion = Menu_Sesion_Iniciada()
        if opcion.isdigit():
            if opcion == "1":
                VentaPasajes()

            elif opcion == "2":
                VerReserva()

            elif opcion == "3":
                CancelarReserva()

            elif opcion == "4":
                print("Saliendo del programa...")
                break

            else:
                print("Opción inválida. Por favor, elija una opción válida.")
        else:
            print("Opción inválida. Por favor, elija una opción válida.")


main()