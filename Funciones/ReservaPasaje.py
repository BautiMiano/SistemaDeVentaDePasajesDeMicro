from Datos.Reservas import reservas
from Funciones.Asientos import ModificarAsiento

def AgregarReserva(reserva):
    reservas.append(reserva)
    return


def VerReserva(usuarioActual):
    print("=" * 65)
    print("MIS RESERVAS".center(65))
    print("=" * 65)

    tieneReservas = False

    for i in range(len(reservas)):
        if reservas[i][0] == usuarioActual:
            tieneReservas = True
            break


    if tieneReservas == False:
        print("")
        print("No hay reservas realizadas.".center(65))
        print("")
        return
        
    print(f"{'N°':<5}{'DESTINO':<25}{'FECHA':<15}{'ASIENTO':>10}")
    print("-" * 65)

    numReservas = 1

    for i in range(len(reservas)):
        if reservas[i][0] == usuarioActual:
            destino = reservas[i][1]
            fecha = reservas[i][2]
            asiento = reservas[i][3]

            print(f"{numReservas:<5}{destino:<25}{fecha:<15}{asiento:>10}")
            numReservas += 1



def CancelarReserva(usuarioActual):
    print("=" * 65)
    print("CANCELAR RESERVA".center(65))
    print("=" * 65)

    tieneReservas = False

    for i in range(len(reservas)):
        if reservas[i][0] == usuarioActual:
            tieneReservas = True
            break

    if tieneReservas == False:
        print("")
        print("No hay reservas para cancelar.".center(65))
        print("")
        return

    print(f"{'N°':<5}{'DESTINO':<25}{'FECHA':<15}{'ASIENTO':>10}")
    print("-" * 65)


    numeroReserva = 1

    for i in range(len(reservas)):
        if reservas[i][0] == usuarioActual:
            destino = reservas[i][1]
            fecha = reservas[i][2]
            asiento = reservas[i][3]
            print(f"{numeroReserva:<5}{destino:<25}{fecha:<15}{asiento:>10}")
            numeroReserva += 1




    print("-" * 65)

    opcion = input("Ingrese la reserva que queres cancelar: ")
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) >= numeroReserva:
        print("ERROR: Opcion invalida.")
        opcion = input("Ingrese la reserva que queres cancelar: ")
    opcion = int(opcion)

    numeroReserva = 1

    for i in range(len(reservas)):
        if reservas[i][0] == usuarioActual:

            if numeroReserva == opcion:

                reserva = reservas[i]

                asiento = reserva[3]

                numero = int(asiento[:-1])
                letra = asiento[-1].upper() 

                ModificarAsiento(numero, letra)

                reservas.remove(reserva)

                print("")
                print("Reserva cancelada correctamente.".center(65))
                print("")

            numeroReserva += 1