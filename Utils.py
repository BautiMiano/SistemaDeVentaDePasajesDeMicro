import re, time, random, json, os
from Datos import distancias, micros, patentes, viajes, ventas, matriz, FILAS, COLUMNAS, TARIFAPORKM

ARCHIVO_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),"datos.json")

############################## Json ##################################
#OK
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
        print("Datos guardados correctamente.")

    except OSError as mensaje:
        print("Error al guardar los datos:", mensaje)

    finally:
        try:
            arch.close()
        except NameError:
            pass
#OK
def CargarDatos():
    try:
        arch = open(ARCHIVO_JSON, "rt", encoding="UTF8")
        datos = json.load(arch)

    except FileNotFoundError:
        print("Todavía no existe un archivo de datos.")
        return

    except (OSError, json.JSONDecodeError) as mensaje:
        print("Error al cargar los datos:", mensaje)
        return

    finally:
        try:
            arch.close()
        except NameError:
            pass

    distancias.clear()
    distancias.update(datos.get("distancias", {}))

    micros.clear()
    micros.extend(datos.get("micros", []))

    patentes.clear()
    patentes.update(datos.get("patentes", []))

    viajes.clear()
    viajes.extend(datos.get("viajes", []))

    ventas.clear()
    ventas.extend(datos.get("ventas", []))

    print("Datos cargados correctamente.")

############################## Menu ##################################
#OK
def menu_principal():
    print("=" * 45)
    print("SISTEMA DE GESTIÓN".center(45))
    print("=" * 45)
    print("")
    print("1 - Ventas")
    print("2 - Consultas")
    print("3 - Viajes")
    print("4 - Micros")
    print("5 - Salir")

    print("")
    print("-" * 45)
    opcion = input("Seleccione una opcion: ")
    print("")
    return opcion
#OK
def menu_ventas():
    print("=" * 45)
    print("VENTAS".center(45))
    print("=" * 45)
    print("")
    print("1 - Registrar venta de pasaje")
    print("2 - Ver ventas")
    print("3 - Buscar venta")
    print("4 - Modificar venta")
    print("5 - Cancelar venta")
    print("6 - volver atras")
    print("")

    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion
#OK
def menu_consultas():
    print("="*45)
    print("CONSULTAS".center(45))
    print("="*45)
    print("")
    print("1 - Consultar ventas por destino")
    print("2 - Consultar ventas por fecha")
    print("3 - Consultar ventas por usuario")
    print("4 - volver atras")
    print("")

    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion
#OK
def menu_viajes():
    print("="*45)
    print("Viajes".center(45))
    print("="*45)
    print("")
    print("1 - Consultar disponibilidad")
    print("2 - Agregar destinos")
    print("3 - Eliminar destinos")
    print("4 - Ver destinos")
    print("5 - volver atras")
    print("")
    
    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion
#OK
def menu_micros():
    print("="*45)
    print("Viajes".center(45))
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

############################## Micros ##################################
#OK
def RegistrarMicro():
    patente = input("Ingrese la patente del micro: ").upper().strip()
    while not re.match(r"^[A-Z]{2}[0-9]{3}[A-Z]{2}$", patente):
        print("Error, no se ingreso el formato valido")
        patente = input("Ingrese otra patente: ").strip().upper()

    while patente == "" or patente in patentes:
        if patente == "":
            print("Error: la patente no puede estar vacía.")
        else:
            print("Error: esa patente ya está registrada.")
        patente = input("Ingrese otra patente: ").strip().upper()

    micro = {
        "patente" : patente
    }
    micros.append(micro)
    patentes.add(patente)
    GuardarDatos()
    print("Micro registrado correctamente")
#MODIFICAR (dejar para el final)
def DarBajaMicro():
    if not micros:
        print("No hay micros registrados.")
        return
    while True:
        print("Menu para dar micros de baja")
        for numero, micro in enumerate(micros, start = 1):
            print(f"{numero}. {micro['patente']}")
        Sel_micro = input("Seleccione el micro (ingrese el número): ")
        print("Ingrese X para salir")
        if Sel_micro.upper() == "X":
            return 
        while not Sel_micro.isdigit() or int(Sel_micro) < 1 or int(Sel_micro) > len(micros):
            print("Error: opción inválida.")
            Sel_micro = input("Seleccione el micro (ingrese el número): ")
            if Sel_micro.upper() == "X":
                return
        patente = micros[int(Sel_micro) - 1]["patente"]
        tiene_viajes = False
        for viaje in viajes:
            if viaje["patente"] == patente and viaje["estado"] == "programado":
                tiene_viajes = True
                break
        if tiene_viajes:
            print("-" * 50,"\n")
            print("Denegado, el micro seleccionado tiene al menos un viaje programado")
            print("Seleccione otro micro o ingrese X para salir")
            print("\n-" * 50)
        else:
            print("-" * 50,"\n")
            print("Micro identificado, baja realizada.")
            print(f"Patente eliminada: {patente}")
            print("\n-" * 50)
            micros.pop(int(Sel_micro) - 1)
            patentes.remove(patente)    
            if not micros:
                print("No quedan micros registrados.")
                return
#OK 
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

def MicrosPorDestinos(destino):
    micros_disponibles = []
    for micro in micros:
        if destino in micro["destinos"]:
            micros_disponibles.append(micro)

    if not micros_disponibles:
        print("No hay micros para ese destino")
        return []
    return micros_disponibles

############################## Destinos ##################################
#OK
def AgregarDestino():

    destino = input("Ingrese el nombre del destino: ").strip().title()

    # Validar que el destino no esté vacío ni repetido
    while destino == "" or destino in distancias:
        if destino == "":
            print("Error: el destino no puede estar vacío.")
        else:
            print("Error: ese destino ya está registrado.")

        destino = input("Ingrese otro destino: ").strip().title()

    # Solicitar y validar la distancia
    while True:
        try:
            distancia = int(input("Ingrese la distancia en kilómetros desde Buenos Aires: "))

            if distancia <= 0:
                print("Error: la distancia debe ser mayor que cero.")
                continue

            break

        except ValueError:
            print("Error: ingrese una distancia válida en números.")

    # Guardar el destino y su distancia
    distancias[destino] = distancia
    GuardarDatos()

    print(f"Destino '{destino}' registrado correctamente.")
#OK
def VerDestinos():
    if not distancias:
        print("\nNo hay destinos registrados.")
        return

    print("\n" + "=" * 40)
    print("DESTINOS REGISTRADOS".center(40))
    print("=" * 40)

    for i, (destino, distancia) in enumerate(distancias.items(), start=1):
        print(f"{i}. {destino} - {distancia} km")

    print("=" * 40)
#AGREGAR FUNCION PARA ELIMINAR DESTINOS (dejar para el final)

############################## Viajes ##################################

#seleccionar destino -> seleccionar fecha -> asignarle un micro(un micro no 
# puede tener 2 viajes un mismo dia) -> CrearMatriz() -> guardar datos
def RegistrarViaje():
    print("mañana lo hago")

def VerViajes():
    print("=" * 50)
    print("VIAJES PROGRAMADOS".center(50))
    print("=" * 50)
    for viaje in viajes:
        print(f"ID: {viaje['id']}, Salida: {viaje['salida']}, Destino: {viaje['destino']}, Fecha: {viaje['fecha']}, Patente: {viaje['patente']}, Estado: {viaje['estado']}")

def Seleccionar_Destinos():

    destinos_agregados = []
    while True:
        for numero, (destino, distancia) in enumerate(distancias.items(), start = 1):
            print(f"{numero}. {destino} - {distancia} km")
        print("ingrese X para dejar de agregar destinos.")
        Sel_destino = input("Seleccione el destino (ingrese el número): ")
        if Sel_destino.upper() == "X":
            if not destinos_agregados:
                print("Debe seleccionar al menos un destino.")
            else:
                break
        while not Sel_destino.isdigit() or int(Sel_destino) < 1 or int(Sel_destino) > len(distancias):        
            print("Error: opción inválida.")
            Sel_destino = input("Seleccione el destino (ingrese el número): ")
        destino = list(distancias.keys())[int(Sel_destino) - 1]
        if destino not in destinos_agregados:
            print("Destino agendado")
            destinos_agregados.append(destino)
        else:
            print("Ya esta agendado el destino, intente con otro")
    return 

############################## Asientos ##################################

def CrearMatriz():
    for f in range(FILAS + 1):
        matriz.append([0] * COLUMNAS)

    for f in range(FILAS + 1):
        for c in range(COLUMNAS):

            if c == 2:
                continue
            else:
                estado = random.randint(0, 1)
                asientos_libres = 0
                asientos_ocupados = 0

                if estado == 0: #O = Libre
                    matriz[f][c] = "O"
                    asientos_libres = asientos_libres + 1
                    
                else:
                    matriz[f][c] = "X" #X = ocupado
                    asientos_ocupados = asientos_ocupados + 1

    return matriz
    
def ImprimirMatriz(matriz):

    print("")
    print("     ASIENTOS")
    print("    A B   C D")
    print("   -----------")

    for f in range(0, len(matriz)):
        print(f"{f:>2}  {matriz[f][0]} {matriz[f][1]}   {matriz[f][2]} {matriz[f][3]}")

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

######################################  Ventas ###############################

def RegistrarVenta():

    # 1. Obtener los destinos con viajes programados
    destinos = []

    for viaje in viajes:
        if viaje["estado"] == "programado":
            if viaje["destino"] not in destinos:
                destinos.append(viaje["destino"])

    if not destinos:
        print("No hay destinos disponibles.")
        return None

    # 2. Seleccionar destino
    print("\nSELECCIONAR DESTINO")

    for i, destino in enumerate(destinos, start=1):
        print(f"{i}. {destino}")

    while True:
        opcion = input("Seleccione un destino (X para cancelar): ").strip()

        if opcion.upper() == "X":
            return None

        if opcion.isdigit() and 1 <= int(opcion) <= len(destinos):
            destino_elegido = destinos[int(opcion) - 1]
            break

        print("Opción inválida.")

    # 3. Obtener los viajes disponibles para ese destino
    viajes_destino = []

    for viaje in viajes:
        if (
            viaje["destino"] == destino_elegido
            and viaje["estado"] == "programado"
        ):
            viajes_destino.append(viaje)

    if not viajes_destino:
        print("No hay viajes disponibles para ese destino.")
        return None

    # 4. Mostrar fechas disponibles para el destino
    print(f"\nFECHAS DISPONIBLES PARA {destino_elegido.upper()}")

    for i, viaje in enumerate(viajes_destino, start=1):
        print(f"{i}. {viaje['fecha']}")

    while True:
        opcion = input("Seleccione una fecha (X para cancelar): ").strip()

        if opcion.upper() == "X":
            return None

        if opcion.isdigit() and 1 <= int(opcion) <= len(viajes_destino):
            viaje_elegido = viajes_destino[int(opcion) - 1]
            break

        print("Opción inválida.")

    # 5. Mostrar los asientos del viaje elegido
    matriz = viaje_elegido["asientos"]
    ImprimirMatriz(matriz)

    # 6. Seleccionar y ocupar un asiento
    while True:
        asiento = input(
            "Seleccione un asiento (ejemplo: 2A, X para cancelar): "
        ).strip().upper()

        if asiento == "X":
            return None

        if OcuparAsiento(matriz, asiento):
            break

        print("Asiento inválido u ocupado. Intente nuevamente.")

    # 7. Devolver los datos de la venta
    venta = [
        viaje_elegido["fecha"],
        viaje_elegido["destino"],
        asiento,
        viaje_elegido["precio"],
        viaje_elegido["patente"]
    ]

    return venta

############################# Funciones extras #############################

def ValidarFechas():
    fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")
    while True:
        try:
            partes = fecha.split("/")
            if len(partes) != 3:
                print("Error: use el formato DD/MM/AAAA.")
                fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")
                continue

            if len(partes[0]) != 2 or len(partes[1]) != 2 or len(partes[2]) != 4:
                print("Error formato numerico: ingrese la fecha en el formato correcto DD/MM/AAAA 00/00/0000.")
                fecha = input("Ingresiguale la fecha del viaje (DD/MM/AAAA): ")
                continue

            try:
                dia = int(partes[0])
            except ValueError:
                print("Error de formato: ingrese día con números.")
                fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")
                continue

            try:
                mes = int(partes[1])
            except ValueError:
                print("Error de formato: ingrese mes con números.")
                fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")
                continue

            try:
                anio = int(partes[2])
            except ValueError:
                print("Error de formato: ingrese año con números.")
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

                    if anio < anio_actual or (anio == anio_actual and mes < mes_actual) or (anio == anio_actual and mes == mes_actual and dia < dia_actual):
                        print("Error, no se pueden ingresar fechas anteriores a hoy.")
                    else:
                        break

            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")            

        except ValueError:
            print("Error: ingrese día, mes y año con números.")
            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")
    return fecha


def BuscarViajePorMicroFecha(viajes, patente, fecha, indice=0):

    if indice >= len(viajes):
        return None

    viaje = viajes[indice]

    if viaje["patente"] == patente and viaje["fecha"] == fecha:
        return viaje

    return BuscarViajePorMicroFecha(viajes, patente, fecha, indice + 1)


########################################################################################
