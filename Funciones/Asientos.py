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

    print("")
    print("     ASIENTOS")
    print("    A B   C D")
    print("   -----------")

    for f in range(1, len(matriz)):
        print(f"{f:>2}  {matriz[f][1]} {matriz[f][2]}   {matriz[f][4]} {matriz[f][5]}")

    print("")
    print("O = Disponible")
    print("X = Ocupado")

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