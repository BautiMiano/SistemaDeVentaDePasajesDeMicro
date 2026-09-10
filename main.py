from Funciones.VentaPasaje import VentaPasajes
from Funciones.Menu import menu_inicio, menu_principal
from Funciones.ReservaPasaje import VerReserva, CancelarReserva
from Funciones.Login import login
from Funciones.Registro import registro


def main():

    while True:
        opcion = menu_inicio()
        if opcion == 1:
            if login():

                while True:
                    opcion2 = menu_principal()

                    if opcion2 == 1:
                        VentaPasajes()

                    elif opcion2 == 2:
                        VerReserva()

                    elif opcion2 == 3:
                        CancelarReserva()

                    elif opcion2 == 4:
                        print("Cerrando sesion...")
                        break
                    else:
                        print("opcion invalida")

        elif opcion == 2:
            registro()
        elif opcion == 3:
            print("Saliendo...")
            break
        else:
            print("opcion invalida")

    return


main()