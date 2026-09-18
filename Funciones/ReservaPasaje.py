from Datos.Reservas import reservas
from Funciones.Asientos import ModificarAsiento

def AgregarReserva(reserva):
    reservas.append(reserva)
    return


def VerReserva():
    print("=" * 65)
    print("MIS RESERVAS".center(65))
    print("=" * 65)

    if len(reservas) == 0:
        print("")
        print("No hay reservas realizadas.".center(65))
        print("")
        return
        
    print(f"{'N°':<5}{'DESTINO':<25}{'FECHA':<15}{'ASIENTO':>10}")
    print("-" * 65)

    for i in range(len(reservas)):
        destino = reservas[i][0]
        fecha = reservas[i][1]
        asiento = reservas[i][2]

        print(f"{i + 1:<5}{destino:<25}{fecha:<15}{asiento:>10}")

def CancelarReserva():
    print("=" * 65)
    print("CANCELAR RESERVA".center(65))
    print("=" * 65)

    if len(reservas) == 0:
        print("")
        print("No hay reservas para cancelar.".center(65))
        print("")
        return

    print(f"{'N°':<5}{'DESTINO':<25}{'FECHA':<15}{'ASIENTO':>10}")
    print("-" * 65)

    for i in range(len(reservas)):
        destino = reservas[i][0]
        fecha = reservas[i][1]
        asiento = reservas[i][2]

        print(f"{i + 1:<5}{destino:<25}{fecha:<15}{asiento:>10}")

    print("-" * 65)

    opcion = int(input("Ingrese la reserva que queres cancelar: "))

    reserva = reservas[opcion - 1]

    asiento = reserva[2]


    numero = int(asiento[:-1])
    letra = asiento[-1].upper()

    ModificarAsiento(numero, letra)

    reservas.remove(reserva)

    print("")
    print("Reserva cancelada correctamente.".center(65))
    print("")