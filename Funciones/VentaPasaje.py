from Funciones.Asientos import asientos, ImprimirMatriz, RellenarMatriz, ElegirAsiento, matriz
from Funciones.ReservaPasaje import AgregarReserva
from Datos.Precio import km_destinos
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

    opcion1 = input("Seleccione un destino: ")
    while not opcion1.isdigit() or int(opcion1) < 1 or int(opcion1) > len(destinos):
        print("ERROR: Opcion invalida. Por favor, seleccione un destino válido.")
        opcion1 = input("Seleccione un destino: ")

    print("")
    print("FECHAS DISPONIBLES".center(50))
    print("-" * 50)

    for i in range(len(fechas)):
            print(f"{i + 1:>2} - {fechas[i]}")

    print("-" * 50)

    opcion2 = input("Seleccione una fecha: ")

    while not opcion2.isdigit() or int(opcion2) < 1 or  int (opcion2) > len(fechas):
        print("ERROR: Opcion invalida. Por favor, seleccione una fecha válida.")
        opcion2 = input("Seleccione una fecha: ")

    opcion1 = int(opcion1)
    opcion2 = int(opcion2)

    precio = Calculo_precio(km_destinos, opcion1)

    print("")
    print("-" * 50)
    print("ASIENTOS DISPONIBLES".center(50))
    print("-" * 50)

    print(f"Destino: {destinos[opcion1 - 1]}")
    print(f"Fecha:   {fechas[opcion2 - 1]}")
    print(f"Precio:  ${precio}")

    print("")
    ImprimirMatriz(matriz)

    print("")
    print("-" * 50)
    
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


    reserva = [destinos[opcion1 - 1], fechas[opcion2 - 1], asiento] 
    AgregarReserva(reserva)
    return reserva, opcion1

def Calculo_precio(km_destinos, opcion1):
     PRECIO_KILOMETRO = 120
     PrecioPasaje = PRECIO_KILOMETRO * km_destinos[opcion1 - 1]
     return PrecioPasaje
     


destinos = ["Mar del Plata", "Pinamar", "Cobos", "Villa Gesel", "San Bernardo"]
fechas = ["7/12/26","14/12/26","21/12/26","28/12/26","4/1/27","11/1/27","18/1/27"]    



    


    


    