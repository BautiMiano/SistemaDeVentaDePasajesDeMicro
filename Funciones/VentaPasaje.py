from Funciones.Asientos import asientos, ImprimirMatriz, RellenarMatriz, ElegirAsiento, matriz
from Funciones.ReservaPasaje import AgregarReserva
def VentaPasajes():
    print("=" * 50)
    print("COMPRA DE PASAJE".center(50))
    print("=" * 50)
    print("")

    print("DESTINOS".center(50))
    print("-" * 50)

    for i in range(len(destinos)):
        print(f"{i + 1:>2} - {destinos[i]}")

    print("-" * 50)

    opcion1 = int(input("Seleccione un destino: "))

    print("")
    print("FECHAS DISPONIBLES".center(50))
    print("-" * 50)

    for i in range(len(fechas)):
            print(f"{i + 1:>2} - {fechas[i]}")

    print("-" * 50)
    
    opcion2 = int(input("Seleccione una fecha: "))

    print("")
    print("Mostrando asientos disponibles para", destinos[opcion1-1], "el", fechas[opcion2-1])
    ImprimirMatriz(matriz)

    print("")
    asiento = input("Seleccione un asiento disponible: ")
    
    numero = int(asiento[:-1])
    letra = asiento[-1].upper()

    resultado = ElegirAsiento(numero, letra)


    while resultado == 0 :
         asiento = input("Seleccione un asiento disponible: ")

         numero = int(asiento[:-1])
         letra = asiento[-1].upper()
         resultado = ElegirAsiento(numero, letra)


    reserva = [destinos[opcion1 - 1], fechas[opcion2 - 1], asiento] 
    AgregarReserva(reserva)
    return reserva



destinos = ["Mar del Plata", "Pinamar", "Cobos", "Villa Gesel", "San Bernardo"]
fechas = ["7/12/26","14/12/26","21/12/26","28/12/26","4/1/27","11/1/27","18/1/27"]    



    


    


    