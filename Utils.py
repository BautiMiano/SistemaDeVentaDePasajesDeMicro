import re
import time
import random
import json

############################## Datos #################################

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

############################## Json ##################################

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
        print("Error: no se pudieron cargar los datos:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass

    if cargado:
        for terminal in datos.get("distancias", {}):
            distancias[terminal] = datos["distancias"][terminal]

        micros.extend(datos.get("micros", []))

        for patente in datos.get("patentes", []):
            patentes.add(patente)

        viajes.extend(datos.get("viajes", []))
        ventas.extend(datos.get("ventas", []))

        print("Datos cargados correctamente.")

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
        print("Error: no se pudieron guardar los datos:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass

############################## Menu ##################################

def MostrarMenuPrincipal():
    print("=" * 50)
    print("SISTEMA DE GESTIÓN".center(50))
    print("=" * 50)
    print("")
    print("1 - Ventas")
    print("2 - Informes")
    print("3 - Viajes")
    print("4 - Micros")
    print("5 - Terminales")
    print("6 - Salir")
    print("")
    print("=" * 50)
    opcion = input("Seleccione una opción: ")
    print("")

    return opcion

def MostrarMenuVentas():
    print("=" * 50)
    print("VENTAS".center(50))
    print("=" * 50)
    print("")
    print("1 - Registrar venta de pasaje")
    print("2 - Ver ventas")
    print("3 - Buscar venta (cancelar / cambiar asiento)")
    print("4 - Volver atrás")
    print("")
    print("=" * 50)
    opcion = input("Seleccione una opción: ")
    print("")

    return opcion

def MostrarMenuBuscarVenta():
    print("=" * 50)
    print("BUSCAR VENTA".center(50))
    print("=" * 50)
    print("")
    print("1 - Por viaje y asiento")
    print("2 - Por DNI")
    print("3 - Por nombre")
    print("4 - Volver atrás")
    print("")
    print("=" * 50)
    opcion = input("Seleccione una opción: ")
    print("")

    return opcion

def MostrarMenuGestionVenta():
    print("=" * 50)
    print("GESTIONAR VENTA".center(50))
    print("=" * 50)
    print("")
    print("1 - Cancelar venta")
    print("2 - Modificar asiento")
    print("3 - Volver atrás")
    print("")
    print("=" * 50)
    opcion = input("Seleccione una opción: ").strip()
    print("")

    return opcion

def MostrarMenuInformes():
    print("=" * 50)
    print("INFORMES".center(50))
    print("=" * 50)
    print("")
    print("1 - Recaudación por destino")
    print("2 - Recaudación por mes")
    print("3 - Recaudación total")
    print("4 - Volver atrás")
    print("")
    print("=" * 50)
    opcion = input("Seleccione una opción: ")
    print("")

    return opcion

def MostrarMenuViajes():
    print("=" * 50)
    print("VIAJES".center(50))
    print("=" * 50)
    print("")
    print("1 - Consultar disponibilidad")
    print("2 - Registrar viaje")
    print("3 - Ver viajes")
    print("4 - Volver atrás")
    print("")
    print("=" * 50)
    opcion = input("Seleccione una opción: ")
    print("")

    return opcion

def MostrarMenuMicros():
    print("=" * 50)
    print("MICROS".center(50))
    print("=" * 50)
    print("")
    print("1 - Ver micros")
    print("2 - Registrar micro")
    print("3 - Dar micro de baja")
    print("4 - Volver atrás")
    print("")
    print("=" * 50)
    opcion = input("Seleccione una opción: ")
    print("")

    return opcion

def MostrarMenuTerminales():
    print("=" * 50)
    print("TERMINALES".center(50))
    print("=" * 50)
    print("")
    print("1 - Ver terminales")
    print("2 - Agregar terminal")
    print("3 - Eliminar terminal")
    print("4 - Volver atrás")
    print("")
    print("=" * 50)
    opcion = input("Seleccione una opción: ")
    print("")

    return opcion

############################## Ventas ################################

def RegistrarVenta():
    if len(viajes) == 0:
        print("No hay viajes registrados. Primero registre un viaje.")
        return

    destinos = []

    for viaje in viajes:
        if viaje["destino"] not in destinos:
            destinos.append(viaje["destino"])

    volver = False

    while True:
        print("\n" + "=" * 50)
        print("DESTINOS".center(50))
        print("=" * 50)

        for i, destino in enumerate(destinos):
            print(f"{i + 1} - {destino}")

        print("0 - Volver atrás")
        print("")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Error: debe ingresar un número.")
            continue

        if opcion == 0:
            volver = True
            break

        if opcion < 1 or opcion > len(destinos):
            print("Error: opción fuera de rango.")
            continue

        destino_elegido = destinos[opcion - 1]

        print("\n" + "=" * 50)
        print(f"VIAJES PARA {destino_elegido.upper()}".center(50))
        print("=" * 50)

        viajes_destino = []

        for viaje in viajes:
            if viaje["destino"] == destino_elegido:
                viajes_destino.append(viaje)

        for i in range(len(viajes_destino)):
            viaje = viajes_destino[i]
            linea = f"{i + 1} - ID: {viaje['id']} | Salida: {viaje['salida']}"
            linea += f" | Fecha: {viaje['fecha']} | Patente: {viaje['patente']}"
            print(linea)

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

    print("\n" + "=" * 50)
    print("RESUMEN DE LA VENTA".center(50))
    print("=" * 50)
    print(f"Salida: {viaje_elegido['salida']}")
    print(f"Destino: {viaje_elegido['destino']}")
    print(f"Fecha: {viaje_elegido['fecha']}")
    print(f"Nombre: {nombre}")
    print(f"DNI: {dni}")
    print(f"Asiento: {asiento_elegido}")
    print(f"Precio: ${FormatoPrecio(precio)}")
    print("=" * 50)

    if not Confirmar("¿Confirmar la venta?"):
        LiberarAsiento(matriz, asiento_elegido)
        print("Venta cancelada. El asiento quedó libre.")
        return

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

def VerVentas():
    print("=" * 50)
    print("VENTAS REGISTRADAS".center(50))
    print("=" * 50)

    VerViajes()

    if len(viajes) == 0:
        return

    try:
        id_elegido = int(input("Seleccione el ID del viaje: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return

    viaje = BuscarViajePorId(id_elegido)

    if viaje == None:
        print("Error: ID no válido.")
        return

    print("\n" + "=" * 50)
    print(f"VENTAS DEL VIAJE {viaje['id']}".center(50))
    print("=" * 50)
    print(f"{viaje['salida']} a {viaje['destino']} - {viaje['fecha']}")
    print("-" * 50)

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

    if not Confirmar(f"¿Está seguro de cancelar la venta del asiento {asiento} de {venta['nombre']}?"):
        print("Operación cancelada.")
        return

    LiberarAsiento(matriz, asiento)

    ventas.remove(venta)

    GuardarDatos()

    print("Venta cancelada correctamente.")

############################## Buscar venta ##########################

def SeleccionarVentaPorAsiento():
    print("=" * 50)
    print("BUSCAR VENTA POR VIAJE Y ASIENTO".center(50))
    print("=" * 50)

    VerViajes()

    if len(viajes) == 0:
        return None

    try:
        id_elegido = int(input("Seleccione el ID del viaje: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return None

    viaje_elegido = BuscarViajePorId(id_elegido)

    if viaje_elegido == None:
        print("Error: ID no válido.")
        return None

    ImprimirMatriz(viaje_elegido["asientos"])

    asiento = input("Ingrese el asiento que desea buscar (ej. 1A o 10D): ").upper().strip()

    venta = BuscarVentaPorAsiento(viaje_elegido["id"], asiento)

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
        linea = f"{i + 1} - {venta['nombre']} | DNI: {venta.get('dni', '-')}"
        linea += f" | {venta['destino']} | {venta['fecha']} | Asiento: {venta['asiento']}"
        print(linea)

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

    opcion = MostrarMenuGestionVenta()

    while opcion != "1" and opcion != "2" and opcion != "3":
        print("Error: opción inválida.")
        opcion = MostrarMenuGestionVenta()

    if opcion == "1":
        CancelarVenta(venta, matriz)

    elif opcion == "2":
        CambiarAsiento(venta, matriz)

############################## Búsquedas recursivas ##################

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

def BuscarVentaPorAsiento(viaje_id, asiento, inicio=0, fin=None):
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

    venta = BuscarVentaPorAsiento(viaje_id, asiento, inicio, medio)

    if venta != None:
        return venta

    return BuscarVentaPorAsiento(viaje_id, asiento, medio, fin)

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

############################## Asientos ##############################

def ContarAsientosOcupados(asientos):
    ocupados = 0

    for fila in asientos:
        for asiento in fila:
            if asiento == "X":
                ocupados += 1

    return ocupados

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
                print("Error: el número de fila es inválido.")
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
                print("Error: la letra del asiento es inválida.")
                continue

            if matriz[x - 1][y] == "X":
                print("Error: el asiento seleccionado ya está ocupado.")
                continue

            break

        except (ValueError, IndexError):
            print("Error: formato inválido. Ingrese un asiento como 1A o 10D.")

    asiento = str(x) + letra
    print(f"Asiento {asiento} seleccionado.")
    matriz[x - 1][y] = "X"

    return asiento

def LiberarAsiento(matriz, asiento):
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

def CambiarAsiento(venta, matriz):
    asiento_anterior = venta["asiento"]

    LiberarAsiento(matriz, asiento_anterior)

    print("Seleccione el nuevo asiento:")
    ImprimirMatriz(matriz)

    nuevo_asiento = ElegirAsiento(matriz)

    venta["asiento"] = nuevo_asiento

    GuardarDatos()

    print("Asiento modificado correctamente.")

def CrearMatriz():
    matriz = []

    for f in range(FILAS):
        matriz.append(["O"] * COLUMNAS)

    return matriz

############################## Informes ##############################

def MostrarInformePorDestino():
    recaudacion_por_destino = {}

    for viaje in viajes:
        destino = viaje["destino"]

        if destino in recaudacion_por_destino:
            recaudacion_por_destino[destino] += CalcularRecaudacionViaje(viaje)
        else:
            recaudacion_por_destino[destino] = CalcularRecaudacionViaje(viaje)

    print("=" * 50)
    print("RECAUDACIÓN POR DESTINO".center(50))
    print("=" * 50)

    if len(recaudacion_por_destino) == 0:
        print("No hay viajes registrados.")
        return

    for destino in sorted(recaudacion_por_destino):
        print(f"{destino:<15} : ${FormatoPrecio(recaudacion_por_destino[destino])}")

    print("-" * 50)

def MostrarInformePorMes():
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    recaudacion_por_mes = {}

    for viaje in viajes:
        partes = viaje["fecha"].split("/")
        clave = (int(partes[2]), int(partes[1]))

        if clave in recaudacion_por_mes:
            recaudacion_por_mes[clave] += CalcularRecaudacionViaje(viaje)
        else:
            recaudacion_por_mes[clave] = CalcularRecaudacionViaje(viaje)

    print("=" * 50)
    print("RECAUDACIÓN POR MES".center(50))
    print("=" * 50)

    if len(recaudacion_por_mes) == 0:
        print("No hay viajes registrados.")
        return

    for clave in sorted(recaudacion_por_mes):
        anio, mes = clave
        nombre_mes = f"{meses[mes - 1]} {anio}"
        print(f"{nombre_mes:<15} : ${FormatoPrecio(recaudacion_por_mes[clave])}")

    print("-" * 50)

def MostrarRecaudacionTotal():
    recaudacion_total = 0

    for viaje in viajes:
        recaudacion_total += CalcularRecaudacionViaje(viaje)

    print("=" * 50)
    print("RECAUDACIÓN TOTAL".center(50))
    print("=" * 50)
    print(f"Recaudación total: ${FormatoPrecio(recaudacion_total)}")
    print("-" * 50)

def CalcularRecaudacionViaje(viaje):
    asientos_ocupados = ContarAsientosOcupados(viaje["asientos"])
    kilometros = distancias[viaje["salida"]][viaje["destino"]]

    return asientos_ocupados * kilometros * TARIFAPORKM

############################## Viajes ################################

def ConsultarDisponibilidad():
    print("=" * 50)
    print("CONSULTAR DISPONIBILIDAD".center(50))
    print("=" * 50)

    if len(viajes) == 0:
        print("No hay viajes registrados.")
        return

    ancho_num = max(len("N°"), len(str(len(viajes))))
    ancho_salida = len("Salida")
    ancho_destino = len("Destino")

    for viaje in viajes:
        if len(viaje["salida"]) > ancho_salida:
            ancho_salida = len(viaje["salida"])

        if len(viaje["destino"]) > ancho_destino:
            ancho_destino = len(viaje["destino"])

    encabezado = "N°".rjust(ancho_num) + " | " + "Salida".ljust(ancho_salida)
    encabezado += " | " + "Destino".ljust(ancho_destino)
    encabezado += f" | {'Fecha':<10} | {'Patente':<7} | Lugares libres"
    print(encabezado)
    print("-" * len(encabezado))

    for i in range(len(viajes)):
        viaje = viajes[i]
        libres = FILAS * COLUMNAS - ContarAsientosOcupados(viaje["asientos"])

        fila = str(i + 1).rjust(ancho_num) + " | " + viaje["salida"].ljust(ancho_salida)
        fila += " | " + viaje["destino"].ljust(ancho_destino)
        fila += f" | {viaje['fecha']:<10} | {viaje['patente']:<7} | {libres:>14}"
        print(fila)

    viaje = ElegirDeLista(viajes, "\nSeleccione un viaje: ")

    print("\n" + "=" * 50)
    print(f"VIAJE {viaje['id']}".center(50))
    print("=" * 50)
    print(f"Salida: {viaje['salida']}")
    print(f"Destino: {viaje['destino']}")
    print(f"Fecha: {viaje['fecha']}")
    print(f"Patente: {viaje['patente']}")

    ImprimirMatriz(viaje["asientos"])

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

    print("\n" + "=" * 50)
    print("MICROS".center(50))
    print("=" * 50)

    for i in range(len(micros)):
        print(f"{i + 1} - {micros[i]['patente']}")

    micro = ElegirDeLista(micros, "Seleccione el micro: ")
    patente = micro["patente"]
    viaje["patente"] = patente

    while True:
        fecha = IngresarFecha()

        ocupado = False

        for i in viajes:
            if i["patente"] == patente and i["fecha"] == fecha:
                ocupado = True
                break

        if ocupado:
            print(f"Error: el micro {patente} ya tiene un viaje el {fecha}.")
            continue

        break

    viaje["fecha"] = fecha

    matriz = CrearMatriz()
    matriz = GenerarVentasAlAzar(salida, destino_elegido, fecha, matriz, patente, viaje["id"])
    viaje["asientos"] = matriz

    viajes.append(viaje)
    GuardarDatos()

    print("Viaje registrado correctamente.")

def GenerarVentasAlAzar(salida, destino, fecha, matriz, patente, viaje_id):
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

def VerViajes():
    print("=" * 50)
    print("VIAJES PROGRAMADOS".center(50))
    print("=" * 50)

    if len(viajes) == 0:
        print("No hay viajes programados.")
        return

    for viaje in viajes:
        print(f"ID: {viaje['id']}")
        print(f"Salida: {viaje['salida']}")
        print(f"Destino: {viaje['destino']}")
        print(f"Fecha: {viaje['fecha']}")
        print(f"Patente: {viaje['patente']}")
        print("-" * 50)

############################## Micros ################################

def VerMicros():
    print("=" * 50)
    print("MICROS REGISTRADOS".center(50))
    print("=" * 50)

    if len(micros) == 0:
        print("No hay micros registrados.")
        return

    for micro in micros:
        patente = micro["patente"]
        print(f"Patente: {patente}")
        print("Destinos asociados:")

        destinos_micro = []

        for viaje in viajes:
            if viaje["patente"] == patente and viaje["destino"] not in destinos_micro:
                destinos_micro.append(viaje["destino"])

        if len(destinos_micro) > 0:
            for destino in destinos_micro:
                print(f"- {destino}")
        else:
            print("- Sin viajes asignados")

        print("-" * 50)

def RegistrarMicro():
    patente = input("Ingrese la patente del micro (ej. AB123CD): ").upper().strip()

    while not re.search(r"^[A-Z][A-Z][0-9][0-9][0-9][A-Z][A-Z]$", patente) or patente in patentes:
        if patente in patentes:
            print("Error: esa patente ya está registrada.")
        else:
            print("Error: la patente debe tener el formato AB123CD.")

        patente = input("Ingrese otra patente: ").strip().upper()

    micro = {
        "patente" : patente
    }
    micros.append(micro)
    patentes.add(patente)
    GuardarDatos()
    print("Micro registrado correctamente.")

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

    if not Confirmar(f"¿Está seguro de dar de baja el micro {patente}? Se borrarán sus viajes y ventas."):
        print("Operación cancelada.")
        return

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

############################## Terminales ############################

def VerTerminales():
    print("=" * 50)
    print("TERMINALES REGISTRADAS".center(50))
    print("=" * 50)

    if len(distancias) == 0:
        print("No hay terminales registradas.")
        return

    for i, terminal in enumerate(distancias):
        print(f"{i + 1} - {terminal}")

        for otra in distancias[terminal]:
            print(f"     - a {otra}: {distancias[terminal][otra]} km")

    print("=" * 50)

def AgregarTerminal():
    print("=" * 50)
    print("AGREGAR TERMINAL".center(50))
    print("=" * 50)

    terminal = input("Ingrese el nombre de la terminal: ")
    terminal = " ".join(terminal.split()).title()

    while not re.search(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$", terminal) or terminal in distancias:
        if terminal in distancias:
            print("Error: esa terminal ya está registrada.")
        else:
            print("Error: el nombre de la terminal solo puede tener letras y espacios.")

        terminal = input("Ingrese otra terminal: ")
        terminal = " ".join(terminal.split()).title()

    kms = {}

    for otra in distancias:
        kms[otra] = IngresarKm(terminal, otra)

    distancias[terminal] = kms

    for otra in kms:
        distancias[otra][terminal] = kms[otra]

    GuardarDatos()

    print(f"Terminal '{terminal}' registrada correctamente.")

def IngresarKm(terminal, otra):
    while True:
        try:
            km = int(input(f"Distancia entre {terminal} y {otra} (km): "))

            if km <= 0:
                print("Error: la distancia debe ser mayor que cero.")
                continue

            break

        except ValueError:
            print("Error: ingrese una distancia válida en números.")

    return km

def EliminarTerminal():
    print("=" * 50)
    print("ELIMINAR TERMINAL".center(50))
    print("=" * 50)

    if len(distancias) == 0:
        print("No hay terminales registradas.")
        return

    terminal = ElegirTerminal()

    if not Confirmar(f"¿Está seguro de eliminar la terminal {terminal}? Se borrarán sus viajes y ventas."):
        print("Operación cancelada.")
        return

    distancias.pop(terminal)

    for otra in distancias:
        distancias[otra].pop(terminal)

    viajes_nuevos = [viaje for viaje in viajes if viaje["salida"] != terminal and viaje["destino"] != terminal]
    viajes.clear()
    viajes.extend(viajes_nuevos)

    ventas_nuevas = [venta for venta in ventas if venta["salida"] != terminal and venta["destino"] != terminal]
    ventas.clear()
    ventas.extend(ventas_nuevas)

    GuardarDatos()

    print(f"Terminal '{terminal}' eliminada correctamente.")
    print("También se eliminaron los viajes y ventas que salían o llegaban ahí.")

def ElegirTerminal():
    terminales = list(distancias.keys())

    print("\n" + "=" * 50)
    print("TERMINALES".center(50))
    print("=" * 50)

    for i, terminal in enumerate(terminales):
        print(f"{i + 1} - {terminal}")

    return ElegirDeLista(terminales, "Seleccione la terminal: ")

def ElegirDestino(salida):
    destinos = []

    for terminal in distancias:
        if terminal != salida:
            destinos.append(terminal)

    print("\n" + "=" * 50)
    print(f"DESTINOS DESDE {salida.upper()}".center(50))
    print("=" * 50)

    for i, destino in enumerate(destinos):
        print(f"{i + 1} - {destino} ({distancias[salida][destino]} km)")

    return ElegirDeLista(destinos, "Seleccione el destino: ")

############################## Funciones extras ######################

def ElegirDeLista(lista, mensaje):
    while True:
        try:
            opcion = int(input(mensaje))

            if opcion < 1 or opcion > len(lista):
                print("Error: opción fuera de rango.")
                continue

            break

        except ValueError:
            print("Error: debe ingresar un número.")

    return lista[opcion - 1]

def IngresarDni():
    dni = input("Ingrese el DNI del pasajero (sin puntos): ").strip()

    while not re.search(r"^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]?$", dni):
        print("Error: el DNI debe tener 7 u 8 números, sin puntos ni espacios.")
        dni = input("Ingrese el DNI del pasajero (sin puntos): ").strip()

    return dni

def IngresarNombre():
    while True:
        nombre = input("Ingrese el nombre completo del pasajero: ")

        nombre = " ".join(nombre.split()).title()

        if not re.search(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$", nombre):
            print("Error: el nombre solo puede contener letras y espacios.")
        elif len(nombre.split()) < 2:
            print("Error: ingrese al menos un nombre y un apellido.")
        else:
            break

    return nombre

def FormatoPrecio(numero):
    cad = str(numero)
    resultado = ""

    while len(cad) > 3:
        resultado = "." + cad[-3:] + resultado
        cad = cad[:-3]

    return cad + resultado

def Confirmar(mensaje):
    respuesta = input(mensaje + " (S/N): ").strip().upper()

    while respuesta != "S" and respuesta != "N":
        print("Error: responda S o N.")
        respuesta = input(mensaje + " (S/N): ").strip().upper()

    return respuesta == "S"

def IngresarFecha():
    fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ").strip()

    while True:
        partes = fecha.split("/")

        if len(partes) != 3:
            print("Error: use el formato DD/MM/AAAA.")
            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ").strip()
            continue

        if len(partes[0]) != 2 or len(partes[1]) != 2 or len(partes[2]) != 4:
            print("Error: el día y el mes deben tener 2 números y el año 4 (ej. 05/03/2027).")
            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ").strip()
            continue

        try:
            dia = int(partes[0])
            mes = int(partes[1])
            anio = int(partes[2])
        except ValueError:
            print("Error: ingrese día, mes y año con números.")
            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ").strip()
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

        fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ").strip()

    return fecha
