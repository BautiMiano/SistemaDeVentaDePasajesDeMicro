from Funciones.Asientos import ModificarAsiento
from Funciones.ReservaPasaje import reservas

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

