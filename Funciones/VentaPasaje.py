from Funciones.Asientos import asientos, ImprimirMatriz, RellenarMatriz, matriz,SeleccionarAsiento
def VentaPasajes():
    print("Venta de pasajes")
    print(" ")
    print("---Destinos---")
    for i in range(len(destinos)):
        print(i+1,".",destinos[i])
    print(" ")
    opcion1 = int(input("Seleccione un destino: "))
    print(" ")
    print("---Fechas---")
    for i in range(len(fechas)):
            print(i+1,".",fechas[i])
    print("")
    opcion2 = int(input("Seleccione una fecha: "))
    print("")
    print("Mostrando asientos disponibles para", destinos[opcion1], "el", fechas[opcion2-1])
    RellenarMatriz(matriz)
    ImprimirMatriz(matriz)
    SeleccionarAsiento(matriz)



destinos = ["Mar del Plata", "Pinamar", "Cobos", "Villa Gesel", "San Bernardo"]
fechas = ["7/12/26","14/12/26","21/12/26","28/12/26","4/1/27","11/1/27","18/1/27"]    



    


    


    

