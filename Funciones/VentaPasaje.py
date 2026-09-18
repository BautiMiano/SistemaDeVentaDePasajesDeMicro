from Funciones.Asientos import asientos, ImprimirMatriz, RellenarMatriz, ElegirAsiento, matriz
from Funciones.ReservaPasaje import AgregarReserva
def VentaPasajes():
    print("Venta de pasajes")
    print(" ")
    print("---Destinos---")

    for i in range(len(destinos)):
        print(i+1,".",destinos[i])
    print(" ")
    opcion1 = input("Seleccione un destino: ")

    while not opcion1.isdigit() or int(opcion1) < 1 or int(opcion1) > len(destinos):
        print("ERROR: Opcion invalida. Por favor, seleccione un destino válido.")
        opcion1 = input("Seleccione un destino: ")
        

    print(" ")
    print("---Fechas---")
    for i in range(len(fechas)):
            print(i+1,".",fechas[i])
    print("")

    opcion2 = input("Seleccione una fecha: ")

    while not opcion2.isdigit() or int(opcion2) < 1 or  int (opcion2) > len(fechas):
        print("ERROR: Opcion invalida. Por favor, seleccione una fecha válida.")
        opcion2 = input("Seleccione una fecha: ")

    opcion1 = int(opcion1)
    opcion2 = int(opcion2)
    print("")
    print("Mostrando asientos disponibles para", destinos[opcion1-1], "el", fechas[opcion2-1])
    ImprimirMatriz(matriz)

    print("")
    asiento = input("Seleccione un asiento disponible: ")
    
    
    while not (asiento[:-1].isdigit() and asiento[-1].isalpha()):
        print("Formato de asiento inválido. Por favor, ingrese un asiento válido (por ejemplo, 1A).")
        asiento = input("Seleccione un asiento disponible: ")
         


    numero = int(asiento[:-1])
    letra = asiento[-1].upper()

    resultado = ElegirAsiento(numero, letra)


    while resultado == 0 :
         asiento = input("Seleccione un asiento disponible: ")

         while not (asiento[:-1].isdigit() and asiento[-1].isalpha()):
                print("Formato de asiento inválido. Por favor, ingrese un asiento válido (por ejemplo, 1A).")
                asiento = input("Seleccione un asiento disponible: ")

         numero = int(asiento[:-1])
         letra = asiento[-1].upper()
         resultado = ElegirAsiento(numero, letra)

    asiento = asiento[:-1] + asiento[-1].upper()
    reserva = [destinos[opcion1 - 1], fechas[opcion2 - 1], asiento] 
    AgregarReserva(reserva)
    return reserva



destinos = ["Mar del Plata", "Pinamar", "Cobos", "Villa Gesel", "San Bernardo"]
fechas = ["7/12/26","14/12/26","21/12/26","28/12/26","4/1/27","11/1/27","18/1/27"]    

