from Funciones.Asientos import ModificarAsiento
from Funciones.ReservaPasaje import reservas

def CancelarReserva():
    if len(reservas) == 0:
        print("No hay reservas realizadas.")
        print(2 * "\n")
        return
    else:
        print("Cancelar reserva")

        for i in range(len(reservas)):
            print( i + 1 , " - ", reservas[i])

        opcion = int(input("Ingrese la reserva que queres cancelar: "))
        opcion = str(opcion)

        while int(opcion) < 1 or int(opcion) > len(reservas) or not opcion.isdigit():
            print("Opción inválida. Por favor, seleccione una reserva válida.")
            opcion = int(input("Ingrese la reserva que queres cancelar: "))

        reserva = reservas[opcion - 1]

        asiento = reserva[2]


        numero = int(asiento[:-1])
        letra = asiento[-1].upper()

        ModificarAsiento(numero, letra)

        reservas.remove(reserva)

        print("Pasaje cancelado correctamente")



