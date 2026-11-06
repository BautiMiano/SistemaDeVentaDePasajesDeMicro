import re, time, random, json, os
from Datos import (distancias, micros, patentes, viajes, ventas, 
                   FILAS, COLUMNAS, TARIFAPORKM)

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
    print("5 - Destinos")
    print("6 - Salir")

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
def menu_informes():
    print("="*45)
    print("CONSULTAS".center(45))
    print("="*45)
    print("")
    print("1 - Informe ventas por destino.")
    print("2 - Informe ventas por fecha.")
    print("3 - Informe la recaudación total.")
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
    print("2 - Registrar viaje")
    print("3 - Ver viajes")
    print("4 - volver atras")
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
#OK
def menu_destinos():
    print("="*45)
    print("Destinos".center(45))
    print("="*45)
    print("")
    print("1 - Ver destinos")
    print("2 - Agregar destinos")
    print("3 - Eliminar destinos")
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
#OK
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

    while True:
        try:
            opcion = int(input("Seleccione el micro a dar de baja: "))

            if opcion < 1 or opcion > len(micros):
                print("Error: opción fuera de rango.")
                continue

            break

        except ValueError:
            print("Error: debe ingresar un número.")

    patente = micros[opcion - 1]["patente"]

    micros.pop(opcion - 1)

    if patente in patentes:
        patentes.remove(patente)

    viajes_nuevos = []

    for viaje in viajes:
        if viaje["patente"] != patente:
            viajes_nuevos.append(viaje)

    viajes[:] = viajes_nuevos

    GuardarDatos()

    print(f"Micro con patente {patente} dado de baja correctamente.")
    print("También se eliminaron sus viajes asociados.")
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
#CREO QUE ES PARA BORRAR
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
#OK
def EliminarDestino():
    print("=" * 50)
    print("ELIMINAR DESTINO".center(50))
    print("=" * 50)

    if len(distancias) == 0:
        print("No hay destinos registrados.")
        return

    VerDestinos()

    destinos = list(distancias.keys())

    while True:
        try:
            opcion = int(input("Seleccione el destino a eliminar: "))

            if opcion < 1 or opcion > len(destinos):
                print("Error: opción fuera de rango.")
                continue

            break

        except ValueError:
            print("Error: debe ingresar un número.")

    destino = destinos[opcion - 1]

    distancias.pop(destino)

    viajes[:] = [
        viaje for viaje in viajes
        if viaje["destino"] != destino
    ]

    GuardarDatos()

    print(f"Destino '{destino}' eliminado correctamente.")
    print("También se eliminaron sus viajes asociados.")

############################## Viajes ##################################

#FUNCIONANDO, ARREGLAR: UN MICRO NO PUEDE TENER 2 VIAJES UN MISMO DIA,
# SE PUEDE AGREGAR ELEGIR EL LUGAR DE SALIDA
def RegistrarViaje():
    viaje = {}

    if len(viajes) == 0:
        viaje["id"] = 1
    else:
        viaje["id"] = viajes[-1]["id"] + 1

    try:

        while True:

            VerDestinos()
            print("")

            destinos = list(distancias.keys())
            
            opcion = int(input("Seleccione una opcion: "))

            if opcion < 1 or opcion > len(destinos):
                print("Error. Fuera de rango.")
                continue

            destino_elegido = destinos[opcion - 1]

            viaje["destino"] = destino_elegido
            break

        while True:
            VerMicros()

            patente = input("Ingrese la patente del micro: ").strip().upper()

            micro_elegido = None

            for micro in micros:
                if micro["patente"] == patente:
                    micro_elegido = micro
                    break

            if micro_elegido is None:
                print("Error: esa patente no está registrada.")
                continue

            viaje["patente"] = patente

            break

        fecha = ValidarFechas()
        viaje["fecha"] = fecha

        matriz = CrearMatriz()
        viaje["asientos"] = matriz

        viajes.append(viaje)
        GuardarDatos()

        print("Viaje registrado correctamente.")
        
    except ValueError:
        print("Error. Caracter invalido")
#OK
def VerViajes():
    print("=" * 50)
    print("VIAJES PROGRAMADOS".center(50))
    print("=" * 50)

    if not viajes:
        print("No hay viajes programados.")
        return

    for viaje in viajes:
        print(f"ID: {viaje['id']}")
        #print(f"Salida: {viaje['salida']}")
        print(f"Destino: {viaje['destino']}")
        print(f"Fecha: {viaje['fecha']}")
        print(f"Patente: {viaje['patente']}")
        print("-" * 50)
#A CHEQUEAR
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
#OK
def Disponibilidad():
    print("=" * 50)
    print("CONSULTAR DISPONIBILIDAD".center(50))
    print("=" * 50)

    if len(viajes) == 0:
        print("No hay viajes registrados.")
        return

    print("\nVIAJES DISPONIBLES")

    for i in range(len(viajes)):
        viaje = viajes[i]
        print(f"{i + 1} - Destino: {viaje['destino']} | "
              f"Fecha: {viaje['fecha']} | "
              f"Patente: {viaje['patente']}")

    while True:
        try:
            opcion = int(input("\nSeleccione un viaje: "))

            if opcion < 1 or opcion > len(viajes):
                print("Error: opción fuera de rango.")
                continue

            break

        except ValueError:
            print("Error: debe ingresar un número.")

    viaje = viajes[opcion - 1]

    print("\n" + "=" * 50)
    print(f"DESTINO: {viaje['destino']}")
    print(f"FECHA: {viaje['fecha']}")
    print(f"PATENTE: {viaje['patente']}")
    print("=" * 50)

    ImprimirMatriz(viaje["asientos"])

############################## Asientos ##################################
#OK
def CrearMatriz():
    matriz = []
    asientos_libres = 0
    asientos_ocupados = 0

    for f in range(FILAS):
        matriz.append([0] * COLUMNAS)

    for f in range(FILAS):
        for c in range(COLUMNAS):


            estado = random.randint(0, 1)

            if estado == 0: #O = Libre
                matriz[f][c] = "O"
                asientos_libres = asientos_libres + 1
                
            else:
                matriz[f][c] = "X" #X = ocupado
                asientos_ocupados = asientos_ocupados + 1


    return matriz
#OK    
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
#OK
def ElegirAsiento(matriz):
    while True:
        try:
                asiento = input("Ingrese el asiento (ej. 1A o 10D): ").upper().strip()
                x = int(asiento[:-1])
                y = asiento[-1]

                if x < 1 or x > FILAS:
                    print("El número de fila es inválido.")
                    continue

                if y == "A":
                    y = 0
                elif y == "B":
                    y = 1
                elif y == "C":
                    y = 2
                elif y == "D":
                    y = 3
                else:
                    print("La letra del asiento es inválida.")
                    continue

                if matriz[x - 1][y] == "X":
                    print("El asiento seleccionado ya está ocupado.")
                    continue
            
                print(f"El asiento {asiento} está disponible.")
                matriz[x - 1][y] = "X"
                return asiento

        except ValueError:
            print("Formato inválido. Ingrese un asiento como 1A o 10D.")
            continue
#CHEQUEAR
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
#CHEQUEAR
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

def ContarAsientosOcupados(asientos):
    ocupado = 0

    for fila in asientos:
        for asiento in fila:
            if asiento == "X":
                ocupado +=1
    return ocupado

######################################  Ventas ###############################

def RegistrarVenta():
    #Selecciona un destino -> Selecciona un fecha disponible para ese destino
    #se selecciona un asiento(debe actualizar estado del asiento) -> se guardan los datos
    #se muestra un resumen.

    while True:
        VerDestinos()
        print("")

        destinos = list(distancias.keys())
                    
        opcion = int(input("Seleccione una opcion: "))

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
            print("No hay viajes registrados para ese destino.")
            continue

        for i in range(len(viajes_destino)):
            viaje = viajes_destino[i]
            print(f"{i + 1} - ID: {viaje['id']} | "
                f"Fecha: {viaje['fecha']} | "
                f"Patente: {viaje['patente']}")

        break
        
    while True:
        try:
            opcion_viaje = int(input("\nSeleccione un viaje: "))

            if opcion_viaje < 1 or opcion_viaje > len(viajes_destino):
                print("Error: opción fuera de rango.")
                continue

            break

        except ValueError:
            print("Error: debe ingresar un número.")

    viaje_elegido = viajes_destino[opcion_viaje - 1]

    print("\nViaje seleccionado correctamente.")
    print(f"Destino: {viaje_elegido['destino']}")
    print(f"Fecha: {viaje_elegido['fecha']}")
    print(f"Patente: {viaje_elegido['patente']}")

    matriz = viaje_elegido["asientos"]

    ImprimirMatriz(matriz)
    asiento_elegido = ElegirAsiento(matriz)

    precio = distancias[viaje_elegido["destino"]] * TARIFAPORKM

    print("\n" + "=" * 40)
    print("RESUMEN DE LA VENTA".center(40))
    print("=" * 40)
    print(f"Destino: {viaje_elegido['destino']}")
    print(f"Fecha: {viaje_elegido['fecha']}")
    print(f"Asiento: {asiento_elegido}")
    print(f"Precio: ${precio}")
    print("=" * 40)

    venta = {
    "destino": viaje_elegido["destino"],
    "fecha": viaje_elegido["fecha"],
    "patente": viaje_elegido["patente"],
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

    if len(ventas) == 0:
        print("No hay ventas registradas.")
        return

    for i in range(len(ventas)):
        venta = ventas[i]

        print(f"Venta N°: {i + 1}")
        print(f"Destino: {venta['destino']}")
        print(f"Fecha: {venta['fecha']}")
        print(f"Patente: {venta['patente']}")
        print(f"Asiento: {venta['asiento']}")
        print(f"Precio: ${venta['precio']}")
        print("-" * 50)

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

                    # Comprobar que la fecha no sea anterior a hoy
                    if (anio, mes, dia) < (anio_actual, mes_actual, dia_actual):
                        print("Error: no se pueden ingresar fechas anteriores a hoy.")

                    # Comprobar que la fecha no supere un año desde hoy
                    elif (anio, mes, dia) > (anio_actual + 1, mes_actual, dia_actual):
                        print("Error: solo se pueden registrar viajes hasta un año desde hoy.")

                    else:
                        break

            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")            

        except ValueError:
            print("Error: ingrese día, mes y año con números.")
            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")
    return fecha

########################################################################################

######################################  Informes ###############################

def InformeVentasPorDestino():
    recaudacionPorDestino = {}

    for viaje in viajes:
        destino = viaje["destino"]

        asientosOcupados = ContarAsientosOcupados(viaje["asientos"])

        kilometros = distancias[destino]

        recaudacion = asientosOcupados * kilometros * TARIFAPORKM

        if destino in recaudacionPorDestino:
            recaudacionPorDestino[destino] += recaudacion
        else:
            recaudacionPorDestino[destino] = recaudacion

    print("=" * 50)
    print("INFORME DE VENTAS POR DESTINO".center(50))
    print("=" * 50)

    for destino in recaudacionPorDestino:
        print(f"Destino: {destino}")
        print(f"Recaudación: ${recaudacionPorDestino[destino]}")
        print("-" * 50)

def InformeVentasPorFecha():
    recaudacionPorFecha = {}

    for viaje in viajes:
        fecha = viaje["fecha"]
        destino = viaje ["destino"]

        asientosOcupados = ContarAsientosOcupados(viaje ["asientos"])\

        kilometros = distancias[destino]

        recaudacion = asientosOcupados * kilometros * TARIFAPORKM

        if fecha in recaudacionPorFecha:
            recaudacionPorFecha[fecha] += recaudacion
        else:
            recaudacionPorFecha[fecha] = recaudacion

    print("=" * 50)
    print("INFORME DE VENTAS POR FECHA".center(50))
    print("=" * 50)

    for fecha in recaudacionPorFecha:
        print(f"Fecha: {fecha}")
        print(f"Recaudación: ${recaudacionPorFecha[fecha]}")
        print("-" * 50)

def InformeRecaudacionTotal():
    recaudacionTotal = 0
    for viaje in viajes:
        destino = viaje["destino"]
        asientosOcupados = ContarAsientosOcupados(viaje["asientos"])
        kilometros = distancias[destino]
        recaudacion = asientosOcupados * kilometros * TARIFAPORKM
        recaudacionTotal += recaudacion

    print("=" * 50)
    print("INFORME DE RECAUDACIÓN TOTAL".center(50))
    print("=" * 50)
    print(f"Recaudación Total: ${recaudacionTotal}")
    print("-" * 50)


