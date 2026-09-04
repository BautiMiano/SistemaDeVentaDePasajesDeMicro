reservas = []

def AgregarReserva(reserva):
    reservas.append(reserva)


def VerReserva():
    print("--- Reservas ---")

    if len(reservas) == 0:
        print("No hay reservas realizadas.")
        return
    else:
        for i in range(len(reservas)):
            desntino = reservas[i][0]
            fecha = reservas[i][1]
            asiento = reservas[i][2]

            print(i + 1, "-", desntino, "-", fecha, "- Asiento", asiento)

