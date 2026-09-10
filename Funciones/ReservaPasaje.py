from Datos.Reservas import reservas
from Funciones.Asientos import ModificarAsiento

def AgregarReserva(reserva):
    reservas.append(reserva)
    return


def VerReserva():
    print("--- Reservas ---")

    if len(reservas) == 0:
        print("No hay reservas realizadas.")
        print(2 * "\n")
        return
    else:
        for i in range(len(reservas)):
            desntino = reservas[i][0]
            fecha = reservas[i][1]
            asiento = reservas[i][2]

            print(i + 1, "-", desntino, "-", fecha, "- Asiento", asiento)

def CancelarReserva():
    print("Cancelar reserva")

    for i in range(len(reservas)):
        print( i + 1 , " - ", reservas[i])

    opcion = int(input("Ingrese la reserva que queres cancelar: "))

    reserva = reservas[opcion - 1]

    asiento = reserva[2]


    numero = int(asiento[:-1])
    letra = asiento[-1].upper()

    ModificarAsiento(numero, letra)

    reservas.remove(reserva)

    print("Pasaje cancelado correctamente")

