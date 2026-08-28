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