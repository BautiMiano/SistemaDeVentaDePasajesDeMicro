FILAS = 10
COLUMNAS = 6

def CrearMatriz():
    matriz = []
    for f in range(FILAS + 1):
        matriz.append([0] * COLUMNAS)
    RellenarMatriz(matriz)
    return matriz

def RellenarMatriz(matriz):
    for f in range(FILAS + 1):
        for c in range(COLUMNAS):
            if c == 3:
                matriz[f][c] = " "
            elif c == 0:
                matriz[f][c] = f
            elif f == 0:
                matriz[f][c] = " "
                matriz[f][1] = "A"
                matriz[f][2] = "B"
                matriz[f][4] = "C"
                matriz[f][5] = "D"
            else:
                matriz[f][c] = "O"

def ImprimirMatriz(matriz):

    print("")
    print("     ASIENTOS")
    print("    A B   C D")
    print("   -----------")

    for f in range(1, len(matriz)):
        print(f"{f:>2}  {matriz[f][1]} {matriz[f][2]}   {matriz[f][4]} {matriz[f][5]}")

    print("")
    print("O = Disponible")
    print("X = Ocupado")

def ElegirAsiento(matriz, asiento):
    try:
        asiento = asiento.upper().strip()
        x = int(asiento[:-1])
        y = asiento[-1]

        if x < 1 or x > FILAS:
            print("El número de fila es inválido.")
            return 0

        if y == "A":
            y = 1
        elif y == "B":
            y = 2
        elif y == "C":
            y = 4
        elif y == "D":
            y = 5
        else:
            print("La letra del asiento es inválida.")
            return 0

        if matriz[x][y] == "X":
            print("El asiento seleccionado ya está ocupado.")
            return 0
        else:
            print(f"El asiento {asiento} está disponible.")
            return 1

    except ValueError:
        print("Formato inválido. Ingrese un asiento como 1A o 10D.")
        return 0

def CancelarAsiento(matriz,asiento):

    try:
        asiento = asiento.upper().strip()
        x = int(asiento[:-1])
        y = asiento[-1]

        if x < 1 or x > FILAS:
            print("Número de fila inválido.")
            return 0

        if y == "A":
            y = 1
        elif y == "B":
            y = 2
        elif y == "C":
            y = 4
        elif y == "D":
            y = 5
        else:
            print("Letra de asiento inválida.")
            return 0

        if matriz[x][y] == "X":
            matriz[x][y] = "O"
            print("Asiento cancelado correctamente.")
            return 1
        else:
            print("Ese asiento ya está libre.")
            return 0

    except ValueError:
        print("Formato inválido. Ingrese un asiento como 1A o 10D.")
        return 0

def OcuparAsiento(matriz, asiento):
    try:
        asiento = asiento.upper().strip()
        x = int(asiento[:-1])
        y = asiento[-1]

        if x < 1 or x > FILAS:
            print("Número de fila inválido.")
            return 0

        if y == "A":
            y = 1
        elif y == "B":
            y = 2
        elif y == "C":
            y = 4
        elif y == "D":
            y = 5
        else:
            print("Letra de asiento inválida.")
            return 0

        if matriz[x][y] == "X":
            print("El asiento ya está ocupado.")
            return 0

        matriz[x][y] = "X"
        print(f"El asiento {asiento} fue ocupado correctamente.")
        return 1

    except ValueError:
        print("Formato inválido. Ingrese un asiento como 1A o 10D.")
        return 0

def Contar_Asientos_Libres(asientos):
    asientos_libres = 0
    for fil in range(1, FILAS + 1):
        for col in range(COLUMNAS):
            if col != 0 and col != 3:
                if asientos[fil][col] == "O":
                    asientos_libres += 1
    return asientos_libres