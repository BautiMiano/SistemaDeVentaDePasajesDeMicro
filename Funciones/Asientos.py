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

def SeleccionarAsiento(matriz):
    fila = int(input("Ingrese la fila del asiento: "))
    columna = input("Ingrese la columna del asiento: ")
    if columna == "A":
        c = 1
    elif columna == "B":
        c = 2
    elif columna == "C":
        c = 4
    elif columna == "D":
        c = 5
    else:
        print("Columna inválida")
        return
    f = fila

    if matriz[f][c] == "X":
        print("Ese asiento ya está ocupado.")
    else:
        matriz[f][c] = "X"
        print("Asiento seleccionado correctamente.")