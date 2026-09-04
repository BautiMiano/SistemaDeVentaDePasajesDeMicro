reservas = []

def AgregarReserva(reserva):
    reservas.append(reserva)


def VerReserva():
    print("--- Reservas ---")

    for i in range(len(reservas)):
        desntino = reservas[i][0]
        fecha = reservas[i][1]
        asiento = reservas[i][2]
        print(i + 1, "-", reservas[i][0], "-", reservas[i][1], "- Asiento", reservas[i][2])