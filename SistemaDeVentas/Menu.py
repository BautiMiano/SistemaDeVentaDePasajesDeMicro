def Menu():
    print("MENU - Venta de pasajes de micro")
    print("1 - Venta pasajes")
    print("2 - Ver reserva")
    print("3 - Cancelar reserva")
    print("4 - Salir")
    opcion = int(input("Eliga una opcion: "))
    return opcion

def VentaPasajes():
    print("Venta de pasajes")
    break

def VerReserva():
    print("Ver reserva")
    break

def CancelarReserva():
    print("Cancelar reserva")
    break

def Salir():
    print("Saliendo del programa...")
    break

def main():
    while True:
        opcion = Menu()
        if opcion == 1:
            VentaPasajes()
        elif opcion == 2:
            VerReserva()
            # Lógica para ver reserva
        elif opcion == 3:
            CancelarReserva()
            # Lógica para cancelar reserva
        elif opcion == 4:
            Salir()
        else:
            print("Opción inválida. Por favor, elija una opción válida.")


main()