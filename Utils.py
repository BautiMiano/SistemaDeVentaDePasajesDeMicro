import re
import time
import random
import json

distancias = {}

micros = []
patentes = set()

viajes = []
ventas = []

FILAS = 10
COLUMNAS = 4
TARIFAPORKM = 100

ARCHIVO_JSON = "datos.json"

nombres = [
    "Juan", "Santiago", "Mateo", "Nicolas", "Benjamin",
    "Thiago", "Tomas", "Joaquin", "Franco", "Lucas",
    "Martin", "Agustin", "Facundo", "Matias", "Federico",
    "Ignacio", "Diego", "Gabriel", "Bruno", "Lautaro",
    "Sofia", "Valentina", "Martina", "Camila", "Lucia",
    "Catalina", "Florencia", "Julieta", "Agustina", "Micaela",
    "Paula", "Carolina", "Victoria", "Milagros", "Abril",
    "Emilia", "Sol", "Josefina", "Rocio", "Ana"
]

apellidos = [
    "Gonzalez", "Rodriguez", "Gomez", "Fernandez", "Lopez",
    "Martinez", "Perez", "Garcia", "Sanchez", "Romero",
    "Diaz", "Torres", "Alvarez", "Ruiz", "Ramirez",
    "Acosta", "Benitez", "Medina", "Herrera", "Castro",
    "Suarez", "Romano", "Silva", "Molina", "Morales",
    "Rojas", "Ortiz", "Nuñez", "Luna", "Juarez",
    "Cabrera", "Rios", "Ferreyra", "Godoy", "Moreno",
    "Sosa", "Aguirre", "Gimenez", "Vazquez", "Ledesma"
]

def GuardarDatos():
    datos = {
        "distancias": distancias,
        "micros": micros,
        "patentes": list(patentes),
        "viajes": viajes,
        "ventas": ventas
    }

    try:
        arch = open(ARCHIVO_JSON, "wt", encoding="UTF8")
        json.dump(datos, arch)
    except OSError as mensaje:
        print("Error al guardar los datos:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass

def CargarDatos():
    cargado = False

    try:
        arch = open(ARCHIVO_JSON, "rt", encoding="UTF8")
        datos = json.load(arch)
        cargado = True
    except FileNotFoundError:
        print("Todavía no existe un archivo de datos.")
    except ValueError as mensaje:
        print("Error: datos.json está dañado:", mensaje)
    except OSError as mensaje:
        print("Error al cargar los datos:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass

    if cargado:
        distancias.clear()
        for terminal in datos.get("distancias", {}):
            distancias[terminal] = datos["distancias"][terminal]

        micros.clear()
        micros.extend(datos.get("micros", []))

        patentes.clear()
        for patente in datos.get("patentes", []):
            patentes.add(patente)

        viajes.clear()
        viajes.extend(datos.get("viajes", []))

        ventas.clear()
        ventas.extend(datos.get("ventas", []))

        print("Datos cargados correctamente.")


def menu_principal():
    print("=" * 45)
    print("SISTEMA DE GESTIÓN".center(45))
    print("=" * 45)
    print("")
    print("1 - Ventas")
    print("2 - Informes")
    print("3 - Viajes")
    print("4 - Micros")
    print("5 - Terminales")
    print("6 - Salir")

    print("")
    print("-" * 45)
    opcion = input("Seleccione una opcion: ")
    print("")
    return opcion

def menu_ventas():
    print("=" * 45)
    print("VENTAS".center(45))
    print("=" * 45)
    print("")
    print("1 - Registrar venta de pasaje")
    print("2 - Ver ventas")
    print("3 - Buscar venta (cancelar / cambiar asiento)")
    print("4 - Volver atras")
    print("")

    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion

def menu_buscar_venta():
    print("=" * 45)
    print("BUSCAR VENTA".center(45))
    print("=" * 45)
    print("")
    print("1 - Por viaje y asiento")
    print("2 - Por DNI")
    print("3 - Por nombre")
    print("4 - Volver atras")
    print("")

    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion

def menu_informes():

    print("="*45)
    print("INFORMES".center(45))
    print("="*45)
    print("")
    print("1 - Informe ventas por destino.")
    print("2 - Informe ventas por mes.")
    print("3 - Informe la recaudación total.")
    print("4 - volver atras")
    print("")

    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion

def menu_viajes():
    print("="*45)
    print("Viajes".center(45))
    print("="*45)
    print("")
    print("1 - Consultar disponibilidad")
    print("2 - Registrar viaje")
    print("3 - Ver viajes")
    print("4 - volver atras")
    print("")
    
    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion

def menu_micros():
    print("="*45)
    print("Micros".center(45))
    print("="*45)
    print("")
    print("1 - Ver micros")
    print("2 - Registrar micros")
    print("3 - Dar micro de baja")
    print("4 - volver atras")
    print("")
    
    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion

def menu_terminales():
    print("="*45)
    print("Terminales".center(45))
    print("="*45)
    print("")
    print("1 - Ver terminales")
    print("2 - Agregar terminal")
    print("3 - Eliminar terminal")
    print("4 - volver atras")
    print("")

    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion

def menu_gestion_venta():

    print("="*45)
    print("Seleccione una opcion".center(45))
    print("="*45)
    print("")
    print("1. Cancelar venta")
    print("2. Modificar asiento")
    print("3. Volver al menu")

    print("="*45)
    opcion = input("Seleccione una opción: ").strip()
    print("")
    return opcion


def RegistrarMicro():

    patente = input("Ingrese la patente del micro (ej. AB123CD): ").upper().strip()

    while not re.search(r"^[A-Z][A-Z][0-9][0-9][0-9][A-Z][A-Z]$", patente) or patente in patentes:
        if patente in patentes:
            print("Error: esa patente ya está registrada.")
        else:
            print("Error, no se ingreso el formato valido")
        patente = input("Ingrese otra patente: ").strip().upper()

    micro = {
        "patente" : patente
    }
    micros.append(micro)
    patentes.add(patente)
    GuardarDatos()
    print("Micro registrado correctamente")

def DarBajaMicro():
    print("=" * 50)
    print("DAR DE BAJA MICRO".center(50))
    print("=" * 50)

    if len(micros) == 0:
        print("No hay micros registrados.")
        return

    print("\nMICROS REGISTRADOS")

    for i in range(len(micros)):
        print(f"{i + 1} - Patente: {micros[i]['patente']}")

    micro = ElegirDeLista(micros, "Seleccione el micro a dar de baja: ")
    patente = micro["patente"]

    micros.remove(micro)
    patentes.discard(patente)

    viajes_nuevos = [viaje for viaje in viajes if viaje["patente"] != patente]
    viajes.clear()
    viajes.extend(viajes_nuevos)

    ventas_nuevas = [venta for venta in ventas if venta["patente"] != patente]
    ventas.clear()
    ventas.extend(ventas_nuevas)

    GuardarDatos()

    print(f"Micro con patente {patente} dado de baja correctamente.")
    print("También se eliminaron sus viajes y ventas asociados.")

def VerMicros():

    if not micros:
        print("No hay micros registrados.")
        return

    print("=" * 50)
    print("MICROS REGISTRADOS".center(50))
    print("=" * 50)

    for micro in micros:
        patente = micro["patente"]
        print(f"Patente: {patente}")
        print("Destinos asociados:")

        destinos_micro = []

        for viaje in viajes:
            if (
                viaje["patente"] == patente
                and viaje["destino"] not in destinos_micro
            ):
                destinos_micro.append(viaje["destino"])

        if destinos_micro:
            for destino in destinos_micro:
                print(f"- {destino}")
        else:
            print("- Sin viajes asignados")

        print("-" * 30)


def IngresarKm(terminal, otra):
    while True:
        try:
            km = int(input(f"Distancia entre {terminal} y {otra} (km): "))

            if km <= 0:
                print("Error: la distancia debe ser mayor que cero.")
                continue

            return km

        except ValueError:
            print("Error: ingrese una distancia válida en números.")

def AgregarTerminal():

    terminal = input("Ingrese el nombre de la terminal: ").strip().title()

    while terminal == "" or terminal in distancias:
        if terminal == "":
            print("Error: la terminal no puede estar vacía.")
        else:
            print("Error: esa terminal ya está registrada.")

        terminal = input("Ingrese otra terminal: ").strip().title()

    kms = {}
    for otra in distancias:
        kms[otra] = IngresarKm(terminal, otra)

    distancias[terminal] = kms
    for otra in kms:
        distancias[otra][terminal] = kms[otra]

    GuardarDatos()

    print(f"Terminal '{terminal}' registrada correctamente.")

def VerTerminales():
    if not distancias:
        print("\nNo hay terminales registradas.")
        return

    print("\n" + "=" * 40)
    print("TERMINALES REGISTRADAS".center(40))
    print("=" * 40)

    for i, terminal in enumerate(distancias):
        print(f"{i + 1}. {terminal}")
        for otra in distancias[terminal]:
            print(f"     - a {otra}: {distancias[terminal][otra]} km")

    print("=" * 40)

def ElegirDeLista(lista, mensaje):
    while True:
        try:
            opcion = int(input(mensaje))

            if opcion < 1 or opcion > len(lista):
                print("Error: opción fuera de rango.")
                continue

            return lista[opcion - 1]

        except ValueError:
            print("Error: debe ingresar un número.")

def ElegirTerminal():
    terminales = list(distancias.keys())

    print("\n" + "=" * 40)
    print("TERMINALES".center(40))
    print("=" * 40)

    for i, terminal in enumerate(terminales):
        print(f"{i + 1}. {terminal}")

    return ElegirDeLista(terminales, "Seleccione la terminal: ")

def ElegirDestino(salida):
    destinos = []
    for terminal in distancias:
        if terminal != salida:
            destinos.append(terminal)

    print("\n" + "=" * 40)
    print(f"DESTINOS DESDE {salida.upper()}".center(40))
    print("=" * 40)

    for i, destino in enumerate(destinos):
        print(f"{i + 1}. {destino} - {distancias[salida][destino]} km")

    return ElegirDeLista(destinos, "Seleccione el destino: ")

def EliminarTerminal():
    print("=" * 50)
    print("ELIMINAR TERMINAL".center(50))
    print("=" * 50)

    if len(distancias) == 0:
        print("No hay terminales registradas.")
        return

    terminal = ElegirTerminal()

    distancias.pop(terminal)
    for otra in distancias:
        distancias[otra].pop(terminal)

    viajes_nuevos = [viaje for viaje in viajes
                     if viaje["salida"] != terminal and viaje["destino"] != terminal]
    viajes.clear()
    viajes.extend(viajes_nuevos)

    ventas_nuevas = [venta for venta in ventas
                     if venta["salida"] != terminal and venta["destino"] != terminal]
    ventas.clear()
    ventas.extend(ventas_nuevas)

    GuardarDatos()

    print(f"Terminal '{terminal}' eliminada correctamente.")
    print("También se eliminaron los viajes y ventas que salían o llegaban ahí.")


def RegistrarViaje():
    if len(distancias) < 2:
        print("Se necesitan al menos 2 terminales para registrar un viaje.")
        return

    if len(micros) == 0:
        print("No hay micros registrados. Primero registre un micro.")
        return

    viaje = {}

    if len(viajes) == 0:
        viaje["id"] = 1
    else:
        viaje["id"] = viajes[-1]["id"] + 1

    salida = ElegirTerminal()
    viaje["salida"] = salida

    destino_elegido = ElegirDestino(salida)
    viaje["destino"] = destino_elegido

    VerMicros()
    patente = input("Ingrese la patente del micro: ").strip().upper()

    while patente not in patentes:
        print("Error: esa patente no está registrada.")
        patente = input("Ingrese la patente del micro: ").strip().upper()

    viaje["patente"] = patente

    while True:
        fecha = ValidarFechas()

        ocupado = False
        for v in viajes:
            if v["patente"] == patente and v["fecha"] == fecha:
                ocupado = True
                break

        if ocupado:
            print(f"Error: el micro {patente} ya tiene un viaje el {fecha}.")
            continue

        break

    viaje["fecha"] = fecha

    matriz = CrearMatriz()
    matriz = CrearVenta(salida, destino_elegido, fecha, matriz, patente, viaje["id"])
    viaje["asientos"] = matriz

    viajes.append(viaje)
    GuardarDatos()

    print("Viaje registrado correctamente.")

def VerViajes():
    print("=" * 50)
    print("VIAJES PROGRAMADOS".center(50))
    print("=" * 50)

    if not viajes:
        print("No hay viajes programados.")
        return

    for viaje in viajes:
        print(f"ID: {viaje['id']}")
        print(f"Salida: {viaje['salida']}")
        print(f"Destino: {viaje['destino']}")
        print(f"Fecha: {viaje['fecha']}")
        print(f"Patente: {viaje['patente']}")
        print("-" * 50)

def Disponibilidad():
    print("=" * 50)
    print("CONSULTAR DISPONIBILIDAD".center(50))
    print("=" * 50)

    if len(viajes) == 0:
        print("No hay viajes registrados.")
        return

    print("\nVIAJES DISPONIBLES\n")

    ancho_num = max(len("N°"), len(str(len(viajes))))
    ancho_salida = len("Salida")
    ancho_destino = len("Destino")
    for viaje in viajes:
        if len(viaje["salida"]) > ancho_salida:
            ancho_salida = len(viaje["salida"])
        if len(viaje["destino"]) > ancho_destino:
            ancho_destino = len(viaje["destino"])

    encabezado = ("N°".rjust(ancho_num) + " | " + "Salida".ljust(ancho_salida) +
                  " | " + "Destino".ljust(ancho_destino) +
                  f" | {'Fecha':<10} | {'Patente':<7} | Lugares libres")
    print(encabezado)
    print("-" * len(encabezado))

    for i in range(len(viajes)):
        viaje = viajes[i]
        libres = FILAS * COLUMNAS - ContarAsientosOcupados(viaje["asientos"])

        print(str(i + 1).rjust(ancho_num) + " | " + viaje["salida"].ljust(ancho_salida) +
              " | " + viaje["destino"].ljust(ancho_destino) +
              f" | {viaje['fecha']:<10} | {viaje['patente']:<7} | {libres:>14}")

    viaje = ElegirDeLista(viajes, "\nSeleccione un viaje: ")

    print("\n" + "=" * 50)
    print(f"SALIDA: {viaje['salida']}")
    print(f"DESTINO: {viaje['destino']}")
    print(f"FECHA: {viaje['fecha']}")
    print(f"PATENTE: {viaje['patente']}")
    print("=" * 50)

    ImprimirMatriz(viaje["asientos"])

def CrearMatriz():
    matriz = []

    for f in range(FILAS):
        matriz.append(["O"] * COLUMNAS)

    return matriz

def ImprimirMatriz(matriz):

    print("")
    print("     ASIENTOS")
    print("    A B   C D")
    print("   -----------")

    for f in range(len(matriz)):
        print(f"{f+1:>2}  {matriz[f][0]} {matriz[f][1]}   {matriz[f][2]} {matriz[f][3]}")

    print("")
    print("O = Disponible")
    print("X = Ocupado")   

def ElegirAsiento(matriz):
    while True:
        try:
            asiento = input("Ingrese el asiento (ej. 1A o 10D): ").upper().strip()
            x = int(asiento[:-1])
            letra = asiento[-1]

            if x < 1 or x > FILAS:
                print("El número de fila es inválido.")
                continue

            if letra == "A":
                y = 0
            elif letra == "B":
                y = 1
            elif letra == "C":
                y = 2
            elif letra == "D":
                y = 3
            else:
                print("La letra del asiento es inválida.")
                continue

            if matriz[x - 1][y] == "X":
                print("El asiento seleccionado ya está ocupado.")
                continue

            break

        except (ValueError, IndexError):
            print("Formato inválido. Ingrese un asiento como 1A o 10D.")

    asiento = str(x) + letra
    print(f"El asiento {asiento} está disponible.")
    matriz[x - 1][y] = "X"
    return asiento

def LiberarAsiento(matriz,asiento):

    x = int(asiento[:-1]) - 1
    y = asiento[-1]

    if y == "A":
        y = 0
    elif y == "B":
        y = 1
    elif y == "C":
        y = 2
    else:
        y = 3

    matriz[x][y] = "O"

def ContarAsientosOcupados(asientos):
    ocupado = 0

    for fila in asientos:
        for asiento in fila:
            if asiento == "X":
                ocupado +=1
    return ocupado

def CambiarAsiento(venta, matriz):
    asiento_anterior = venta["asiento"]

    LiberarAsiento(matriz, asiento_anterior)

    print("Seleccione el nuevo asiento:")
    ImprimirMatriz(matriz)

    nuevo_asiento = ElegirAsiento(matriz)

    venta["asiento"] = nuevo_asiento

    GuardarDatos()

    print("Asiento modificado correctamente.")


def RegistrarVenta():

    if len(viajes) == 0:
        print("No hay viajes registrados. Primero registre un viaje.")
        return

    volver = False

    while True:
        destinos = list(distancias.keys())

        print("\n" + "=" * 40)
        print("DESTINOS".center(40))
        print("=" * 40)
        for i, destino in enumerate(destinos):
            print(f"{i + 1}. {destino}")
        print("0. Volver atras")
        print("")

        try:
            opcion = int(input("Seleccione una opcion: "))
        except ValueError:
            print("Error: debe ingresar un número.")
            continue

        if opcion == 0:
            volver = True
            break

        if opcion < 1 or opcion > len(destinos):
            print("Error. Fuera de rango.")
            continue

        destino_elegido = destinos[opcion - 1]

        print("\nVIAJES PARA", destino_elegido.upper())

        viajes_destino = []

        for viaje in viajes:
            if viaje["destino"] == destino_elegido:
                viajes_destino.append(viaje)

        if len(viajes_destino) == 0:
            print("No hay viajes registrados para ese destino. Elija otro.")
            continue

        for i in range(len(viajes_destino)):
            viaje = viajes_destino[i]
            print(f"{i + 1} - ID: {viaje['id']} | "
                f"Salida: {viaje['salida']} | "
                f"Fecha: {viaje['fecha']} | "
                f"Patente: {viaje['patente']}")

        break

    if volver:
        return

    viaje_elegido = ElegirDeLista(viajes_destino, "\nSeleccione un viaje: ")

    print("\nViaje seleccionado correctamente.")
    print(f"Salida: {viaje_elegido['salida']}")
    print(f"Destino: {viaje_elegido['destino']}")
    print(f"Fecha: {viaje_elegido['fecha']}")
    print(f"Patente: {viaje_elegido['patente']}")

    matriz = viaje_elegido["asientos"]

    if ContarAsientosOcupados(matriz) == FILAS * COLUMNAS:
        print("El viaje está completo, no quedan asientos disponibles.")
        return

    ImprimirMatriz(matriz)
    asiento_elegido = ElegirAsiento(matriz)

    precio = distancias[viaje_elegido["salida"]][viaje_elegido["destino"]] * TARIFAPORKM

    dni = IngresarDni()

    ventas_dni = BuscarVentasPorDni(dni)
    if len(ventas_dni) > 0:
        nombre = ventas_dni[0]["nombre"]
        print(f"Pasajero ya registrado: {nombre}")
    else:
        nombre = IngresarNombre()

    print("\n" + "=" * 40)
    print("RESUMEN DE LA VENTA".center(40))
    print("=" * 40)
    print(f"Salida: {viaje_elegido['salida']}")
    print(f"Destino: {viaje_elegido['destino']}")
    print(f"Fecha: {viaje_elegido['fecha']}")
    print(f"Nombre: {nombre}")
    print(f"DNI: {dni}")
    print(f"Asiento: {asiento_elegido}")
    print(f"Precio: ${FormatoPrecio(precio)}")
    print("=" * 40)

    venta = {
    "viaje_id": viaje_elegido["id"],
    "salida": viaje_elegido["salida"],
    "destino": viaje_elegido["destino"],
    "fecha": viaje_elegido["fecha"],
    "patente": viaje_elegido["patente"],
    "nombre": nombre,
    "dni": dni,
    "asiento": asiento_elegido,
    "precio": precio
}

    ventas.append(venta)
    GuardarDatos()

    print("Venta registrada correctamente.")

def CrearVenta(salida, destino, fecha, matriz, patente, viaje_id):
    precio = distancias[salida][destino] * TARIFAPORKM
    letras = ["A", "B", "C", "D"]

    for f in range(len(matriz)):
        for c in range(len(matriz[f])):

            if random.randint(0, 1) == 1:
                matriz[f][c] = "X"
                asiento = str(f + 1) + letras[c]

                nombre = nombres[random.randint(0, len(nombres) - 1)]
                apellido = apellidos[random.randint(0, len(apellidos) - 1)]
                dni = str(random.randint(15000000, 45999999))

                venta = {
                    "viaje_id": viaje_id,
                    "nombre": nombre + " " + apellido,
                    "dni": dni,
                    "salida": salida,
                    "destino": destino,
                    "fecha": fecha,
                    "patente": patente,
                    "asiento": asiento,
                    "precio": precio
                }

                ventas.append(venta)

    return matriz

def VerVentas():
    print("=" * 50)
    print("VENTAS REGISTRADAS".center(50))
    print("=" * 50)

    VerViajes()

    if not viajes:
        return

    try:
        id_elegido = int(input("Seleccione el ID del viaje: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return

    viaje = BuscarViajePorId(id_elegido)

    if viaje == None:
        print("ID no válido.")
        return

    print("\n" + "=" * 50)
    print(f"VENTAS DEL VIAJE {viaje['id']} - {viaje['salida']} a {viaje['destino']} - {viaje['fecha']}".center(50))
    print("=" * 50)

    cantidad = 0
    for venta in ventas:
        if venta["viaje_id"] == viaje["id"]:
            cantidad += 1
            print(f"Venta N°: {cantidad}")
            MostrarVenta(venta)

    if cantidad == 0:
        print("Este viaje no tiene ventas registradas.")
    else:
        print(f"Total de ventas del viaje: {cantidad}")

def MostrarVenta(venta):
    print(f"Pasajero: {venta['nombre']}")
    print(f"DNI: {venta.get('dni', '-')}")
    print(f"Salida: {venta['salida']}")
    print(f"Destino: {venta['destino']}")
    print(f"Fecha: {venta['fecha']}")
    print(f"Asiento: {venta['asiento']}")
    print(f"Patente: {venta['patente']}")
    print(f"Precio: ${FormatoPrecio(venta['precio'])}")
    print("-" * 50)

def CancelarVenta(venta, matriz):
    asiento = venta["asiento"]

    LiberarAsiento(matriz, asiento)

    ventas.remove(venta)

    GuardarDatos()

    print("Venta cancelada correctamente.")
    

def BuscarViajePorId(viaje_id, inicio=0, fin=None):
    if fin == None:
        fin = len(viajes)

    if fin - inicio == 0:
        return None

    if fin - inicio == 1:
        if viajes[inicio]["id"] == viaje_id:
            return viajes[inicio]
        return None

    medio = (inicio + fin) // 2

    viaje = BuscarViajePorId(viaje_id, inicio, medio)
    if viaje != None:
        return viaje

    return BuscarViajePorId(viaje_id, medio, fin)

def BuscarVenta(viaje_id, asiento, inicio=0, fin=None):
    if fin == None:
        fin = len(ventas)

    if fin - inicio == 0:
        return None

    if fin - inicio == 1:
        venta = ventas[inicio]
        if venta["viaje_id"] == viaje_id and venta["asiento"] == asiento:
            return venta
        return None

    medio = (inicio + fin) // 2

    venta = BuscarVenta(viaje_id, asiento, inicio, medio)
    if venta != None:
        return venta

    return BuscarVenta(viaje_id, asiento, medio, fin)

def BuscarVentasPorDni(dni, inicio=0, fin=None, encontrados=None):

    if fin == None:
        fin = len(ventas)

    if encontrados == None:
        encontrados = []

    if fin - inicio == 0:
        return encontrados

    if fin - inicio == 1:
        if ventas[inicio].get("dni") == dni:
            encontrados.append(ventas[inicio])
        return encontrados

    medio = (inicio + fin) // 2

    BuscarVentasPorDni(dni, inicio, medio, encontrados)
    BuscarVentasPorDni(dni, medio, fin, encontrados)

    return encontrados

def BuscarVentasPorNombre(texto, inicio=0, fin=None, encontrados=None):

    if fin == None:
        fin = len(ventas)

    if encontrados == None:
        encontrados = []

    if fin - inicio == 0:
        return encontrados

    if fin - inicio == 1:
        if texto.lower() in ventas[inicio]["nombre"].lower():
            encontrados.append(ventas[inicio])
        return encontrados

    medio = (inicio + fin) // 2

    BuscarVentasPorNombre(texto, inicio, medio, encontrados)
    BuscarVentasPorNombre(texto, medio, fin, encontrados)

    return encontrados


def SeleccionarVentaPorAsiento():
    print("=" * 50)
    print("BUSCAR VENTA POR VIAJE Y ASIENTO".center(50))
    print("=" * 50)

    VerViajes()

    if not viajes:
        return None

    try:
        id_elegido = int(input("Seleccione el ID del viaje: "))
    except ValueError:
        print("Debe ingresar un número.")
        return None


    viaje_elegido = BuscarViajePorId(id_elegido)

    if viaje_elegido == None:
        print("ID no válido.")
        return None

    ImprimirMatriz(viaje_elegido["asientos"])

    asiento = input("Ingrese el asiento que desea buscar (Ejemplo 3B): ").upper().strip()

    venta = BuscarVenta(viaje_elegido["id"], asiento)

    if venta == None:
        print("No se encontraron ventas para este asiento.")

    return venta

def SeleccionarVentaPorDni():
    print("=" * 50)
    print("BUSCAR VENTA POR DNI".center(50))
    print("=" * 50)

    dni = IngresarDni()

    encontradas = BuscarVentasPorDni(dni)

    if len(encontradas) == 0:
        print(f"No hay ventas para el DNI {dni}.")
        return None

    return ElegirVentaDeLista(encontradas)

def SeleccionarVentaPorNombre():
    print("=" * 50)
    print("BUSCAR VENTA POR NOMBRE".center(50))
    print("=" * 50)

    texto = input("Ingrese el nombre o apellido a buscar: ").strip()

    while texto == "":
        print("Error: debe ingresar al menos una letra.")
        texto = input("Ingrese el nombre o apellido a buscar: ").strip()

    encontradas = BuscarVentasPorNombre(texto)

    if len(encontradas) == 0:
        print(f"No hay ventas a nombre de '{texto}'.")
        return None

    return ElegirVentaDeLista(encontradas)

def ElegirVentaDeLista(lista):
    if len(lista) == 1:
        print("\nSe encontró 1 venta.")
        return lista[0]

    print(f"\nSe encontraron {len(lista)} ventas:\n")

    for i in range(len(lista)):
        venta = lista[i]
        print(f"{i + 1} - {venta['nombre']} | DNI: {venta.get('dni', '-')} | "
              f"{venta['destino']} | {venta['fecha']} | Asiento: {venta['asiento']}")

    elegida = None

    while True:
        try:
            opcion = int(input("\nSeleccione una venta (0 para volver): "))

            if opcion < 0 or opcion > len(lista):
                print("Error: opción fuera de rango.")
                continue

            if opcion != 0:
                elegida = lista[opcion - 1]

            break

        except ValueError:
            print("Error: debe ingresar un número.")

    return elegida

def GestionarVenta(venta):

    viaje = BuscarViajePorId(venta["viaje_id"])

    if viaje == None:
        print("Error: el viaje de esta venta ya no existe.")
        return


    matriz = viaje["asientos"]

    print("\nVenta seleccionada:")
    MostrarVenta(venta)

    opcion = menu_gestion_venta()

    if opcion == "1":
        CancelarVenta(venta, matriz)

    elif opcion == "2":
        CambiarAsiento(venta, matriz)

    elif opcion == "3":
        return

    else:
        print("Opción inválida.")


def ValidarFechas():
    fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")
    while True:
        partes = fecha.split("/")
        if len(partes) != 3:
            print("Error: use el formato DD/MM/AAAA.")
            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")
            continue

        if len(partes[0]) != 2 or len(partes[1]) != 2 or len(partes[2]) != 4:
            print("Error formato numerico: ingrese la fecha en el formato correcto DD/MM/AAAA 00/00/0000.")
            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")
            continue

        try:
            dia = int(partes[0])
            mes = int(partes[1])
            anio = int(partes[2])
        except ValueError:
            print("Error: ingrese día, mes y año con números.")
            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")
            continue

        if mes < 1 or mes > 12:
            print("Error: el mes debe estar entre 1 y 12.")
        else:
            dias_por_mes = {
                1: 31, 2: 28, 3: 31, 4: 30,
                5: 31, 6: 30, 7: 31, 8: 31,
                9: 30, 10: 31, 11: 30, 12: 31
            }

            if anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0):
                dias_por_mes[2] = 29

            if dia < 1 or dia > dias_por_mes[mes]:
                print("Error: el día no es válido para ese mes.")
            else:
                fecha_actual = time.localtime()

                dia_actual = fecha_actual.tm_mday
                mes_actual = fecha_actual.tm_mon
                anio_actual = fecha_actual.tm_year

                if (anio, mes, dia) < (anio_actual, mes_actual, dia_actual):
                    print("Error: no se pueden ingresar fechas anteriores a hoy.")

                elif (anio, mes, dia) > (anio_actual + 1, mes_actual, dia_actual):
                    print("Error: solo se pueden registrar viajes hasta un año desde hoy.")

                else:
                    break

        fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")

    return fecha

def IngresarNombre():
    
    while True:
        nombre = input("Ingrese el nombre completo del pasajero: ").strip()

        nombre = " ".join(nombre.split()).title()

        if not re.search(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$", nombre):
            print("Error: el nombre solo puede contener letras y espacios.")
        elif len(nombre.split()) < 2:
            print("Error: ingrese al menos un nombre y un apellido.")
        else:
            break

    return nombre

def IngresarDni():
    dni = input("Ingrese el DNI del pasajero (sin puntos): ").strip()

    while not re.search(r"^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]?$", dni):
        print("Error: el DNI debe tener 7 u 8 números, sin puntos ni espacios.")
        dni = input("Ingrese el DNI del pasajero (sin puntos): ").strip()

    return dni

def FormatoPrecio(numero):
    if numero < 1000:
        return str(numero)

    return FormatoPrecio(numero // 1000) + "." + f"{numero % 1000:03d}"

def RecaudacionViaje(viaje):
    asientosOcupados = ContarAsientosOcupados(viaje["asientos"])
    kilometros = distancias[viaje["salida"]][viaje["destino"]]
    return asientosOcupados * kilometros * TARIFAPORKM

def InformeVentasPorDestino():
    recaudacionPorDestino = {}

    for viaje in viajes:
        destino = viaje["destino"]

        if destino in recaudacionPorDestino:
            recaudacionPorDestino[destino] += RecaudacionViaje(viaje)
        else:
            recaudacionPorDestino[destino] = RecaudacionViaje(viaje)

    print("=" * 50)
    print("INFORME DE VENTAS POR DESTINO".center(50))
    print("=" * 50)

    if len(recaudacionPorDestino) == 0:
        print("No hay viajes registrados.")
        return

    for destino in recaudacionPorDestino:
        print(f"Destino: {destino}")
        print(f"Recaudación: ${FormatoPrecio(recaudacionPorDestino[destino])}")
        print("-" * 50)

def InformeVentasPorMes():
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
             "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    recaudacionPorMes = {}

    for viaje in viajes:
        partes = viaje["fecha"].split("/")
        clave = (int(partes[2]), int(partes[1]))

        if clave in recaudacionPorMes:
            recaudacionPorMes[clave] += RecaudacionViaje(viaje)
        else:
            recaudacionPorMes[clave] = RecaudacionViaje(viaje)

    print("=" * 50)
    print("INFORME DE VENTAS POR MES".center(50))
    print("=" * 50)

    if len(recaudacionPorMes) == 0:
        print("No hay viajes registrados.")
        return

    for clave in sorted(recaudacionPorMes):
        anio, mes = clave
        nombre_mes = f"{meses[mes - 1]} {anio}"
        print(f"{nombre_mes:<15} : ${FormatoPrecio(recaudacionPorMes[clave])}")

    print("-" * 50)

def InformeRecaudacionTotal():
    recaudacionTotal = 0
    for viaje in viajes:
        recaudacionTotal += RecaudacionViaje(viaje)

    print("=" * 50)
    print("INFORME DE RECAUDACIÓN TOTAL".center(50))
    print("=" * 50)
    print(f"Recaudación Total: ${FormatoPrecio(recaudacionTotal)}")
    print("-" * 50)