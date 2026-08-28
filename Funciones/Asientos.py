import random

FILA = 10
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
    for i in matriz:
        print(*i)

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
        y = 3
    else:
        y=4
    
    if matriz[x][y] == "X":
        print("Asiento ocupado")
    else:
        print("Asiento libre")
