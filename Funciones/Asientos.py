import random

FILA = 11
COLUMNAS = 6

matriz = []
for f in range(FILA):
    matriz.append([0] * COLUMNAS)

def asientos():
    x = random.randint(0,1)
    if x == 0:
        estado = "X" #Estado X significa ocupado
    else:
        estado = "O" #Estado O significa libre
    return estado

def ImprimirMatriz(matriz):

    print(*matriz[0])

    for f in range(1, len(matriz)):
        print(*matriz[f])

def RellenarMatriz(matriz):

    filas = len(matriz)
    columnas = len(matriz[0])
    for f in range(filas):
        for c in range(columnas):
            if c == 3:
                matriz[f][c] = " "
            elif c == 0:
                matriz[f][c] = f
            elif f == 0:
                matriz[f][0] = " "
                matriz[f][1] = "A"
                matriz[f][2] = "B"
                matriz[f][4] = "C"
                matriz[f][5] = "D"
            else:
                matriz[f][c] = asientos()

<<<<<<< HEAD
def ElegirAsiento(x, y):

    if y == "A":
        y = 1
    elif y == "B":
        y = 2
    elif y == "C":
        y = 4
    elif y == "D":
        y = 5

    if matriz[x][y] == "X":
        print("Asiento ocupado")
        return 0
    else:
        matriz[x][y] = "X"
        print("Asiento reservado correctamente")
        return 1





def CancelarAsiento(x, y):

    if y == "A":
        y = 1
    elif y == "B":
        y = 2
    elif y == "C":
        y = 4
    elif y == "D":
        y = 5

    if matriz[x][y] == "X":
        matriz[x][y] = "O"
        print("Pasaje cancelado correctamente")
    else:
        print("Ese asiento está libre")

def ModificarAsiento(x, y):

    if y == "A":
        y = 1
    elif y == "B":
        y = 2
    elif y == "C":
        y = 4
    elif y == "D":
        y = 5

    if matriz[x][y] == "X":
        matriz[x][y] = "O"
        print("Asiento liberado correctamente")
    else:
        print("Ese asiento ya está libre")  


RellenarMatriz(matriz)
=======
def SeleccionarAsiento(matriz):

    asiento = input("Seleccione un asiento (ejemplo: 1A): ")

    asiento = asiento.upper()

    fila = int(asiento[:-1])
    letra = asiento[-1]

    if letra == "A":
        columna = 1
    elif letra == "B":
        columna = 2
    elif letra == "C":
        columna = 4
    elif letra == "D":
        columna = 5
    else:
        print("Asiento inválido")
        return

    if matriz[fila][columna] == "X":
        print("Ese asiento ya está ocupado.")
    else:
        matriz[fila][columna] = "X"
        print("Asiento", asiento, "seleccionado correctamente.")
>>>>>>> 452d7d4a85816aece606e84c5c07ef4435bbf2f4
