import re, time, random, json, os
from Datos import (distancias, micros, patentes, viajes, ventas, pasajeros,
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
        "ventas": ventas,
        "pasajeros": pasajeros,
    }

    try:
        arch = open(ARCHIVO_JSON, "wt", encoding="UTF8")
        json.dump(datos, arch,indent=4)
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

    pasajeros.clear()
    pasajeros.update(datos.get("pasajeros", {}))

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
    print("2 - Ver ventas ")
    print("3 - Buscar venta de pasajero")
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

def menu_micros():
    print("="*45)
    print("MICROS".center(45))
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
        print("Error, no se ingreso el formato valido (ab123cd).")
        patente = input("Ingrese otra patente: ").strip().upper()

    while patente == "" or patente in patentes:
        if patente in patentes:
          print("Error: esa patente ya está registrada.")
        else:
          print("Error: formato inválido (ej. AB123CD).")
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

    opcion = PedirOpcion("Seleccione el micro a dar de baja (0 para volver): ", 0, len(micros))
    if opcion == 0:
        return

    confirmar = input(f"¿Está seguro que desea dar de baja el micro {micros[opcion - 1]['patente']}? (S/N): ").strip().upper()
    if confirmar != "S":
        print("Operación cancelada.")
        return

    patente = micros[opcion - 1]["patente"]

    micros.pop(opcion - 1)

    if patente in patentes:
        patentes.remove(patente)

    viajes_nuevos = []

    for viaje in viajes:
        if viaje["patente"] != patente:
            viajes_nuevos.append(viaje)

    ids_eliminados = []
    viajes_nuevos = []

    for viaje in viajes:
        if viaje["patente"] != patente:
            viajes_nuevos.append(viaje)

    viajes[:] = viajes_nuevos
    EliminarVentasDeViajes(ids_eliminados)

    GuardarDatos()

    print(f"Micro con patente {patente} dado de baja correctamente.")
    print("También se eliminaron sus viajes asociados.")


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
            confirmar= input("¿Está seguro que desea eliminar un destino? (S/N): ").strip().upper()
            if confirmar != "S":
                print("Operación cancelada.")
                return
            opcion = int(input("Seleccione el destino a eliminar: "))

            if opcion < 1 or opcion > len(destinos):
                print("Error: opción fuera de rango.")
                continue

            break

        except ValueError:
            print("Error: debe ingresar un número.")

    destino = destinos[opcion - 1]

    distancias.pop(destino)

    ids_eliminados = []
    for viaje in viajes:
        if viaje["destino"] == destino:
            ids_eliminados.append(viaje["id"])

    viajes[:] = [viaje for viaje in viajes if viaje["destino"] != destino]

    EliminarVentasDeViajes(ids_eliminados)

    GuardarDatos()

    print(f"Destino '{destino}' eliminado correctamente.")
    print("También se eliminaron sus viajes asociados.")

############################## Viajes ##################################

#FUNCIONANDO, ARREGLAR: UN MICRO NO PUEDE TENER 2 VIAJES UN MISMO DIA,
# SE PUEDE AGREGAR ELEGIR EL LUGAR DE SALIDA
def RegistrarViaje():
    if len(distancias) == 0:
        print("Primero tiene que registrar al menos un destino.")
        return
    if len(micros) == 0:
        print("Primero tiene que registrar al menos un micro.")
        return

    VerDestinos()
    destinos = list(distancias.keys())
    opcion = PedirOpcion("Seleccione un destino (0 para volver): ", 0, len(destinos))
    if opcion == 0:
        return
    destino_elegido = destinos[opcion - 1]

    VerMicros()
    patente = input("Ingrese la patente del micro: ").strip().upper()
    while patente not in patentes:
        print("Error: esa patente no está registrada.")
        patente = input("Ingrese la patente del micro: ").strip().upper()

    fecha = ValidarFechas()

    for viaje in viajes:
        if viaje["patente"] == patente and viaje["fecha"] == fecha:
            print(f"Error: el micro {patente} ya tiene un viaje el {fecha}.")
            return

    viaje = {
        "id": NuevoIdViaje(),
        "destino": destino_elegido,
        "patente": patente,
        "fecha": fecha,
        "asientos": CrearMatriz()
    }

    viajes.append(viaje)
    GuardarDatos()
    print(f"Viaje registrado correctamente con ID {viaje['id']}.")

def NuevoIdViaje():
    if len(viajes) == 0:
        return 1
    mayor = 0
    for viaje in viajes:
        if viaje["id"] > mayor:
            mayor = viaje["id"]
    return mayor + 1



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

def CancelarVenta():
    print("=" * 50)
    print("CANCELAR VENTA".center(50))
    print("=" * 50)

    venta = SeleccionarVenta()
    if len(venta) == 0:
        return

    confirmar = input(f"¿Cancelar el asiento {venta['asiento']} a {venta['destino']} "
                      f"del {venta['fecha']}? (S/N): ").strip().upper()
    if confirmar != "S":
        print("Operación cancelada. La venta sigue vigente.")
        return

    indice_viaje = BuscarViajePorId(venta.get("viaje_id", -1))
    if indice_viaje != -1:
        CancelarAsiento(viajes[indice_viaje]["asientos"], venta["asiento"])

    ventas.remove(venta)
    GuardarDatos()
    print("Venta cancelada correctamente. El asiento quedó libre.")

def ModificarVenta():
    print("=" * 50)
    print("MODIFICAR VENTA".center(50))
    print("=" * 50)

    venta = SeleccionarVenta()
    if len(venta) == 0:
        return

    print("\n1 - Cambiar asiento")
    print("0 - Volver")
    opcion = PedirOpcion("Seleccione una opción: ", 0, 2)

    if opcion == 0:
        return

    if opcion == 1:
        indice_viaje = BuscarViajePorId(venta.get("viaje_id", -1))
        if indice_viaje == -1:
            print("No se encontró el viaje de esta venta.")
            return

        matriz = viajes[indice_viaje]["asientos"]
        ImprimirMatriz(matriz)
        print(f"Asiento actual: {venta['asiento']}")

        asiento_nuevo, fila, columna = ElegirAsiento(matriz)

        CancelarAsiento(matriz, venta["asiento"])
        matriz[fila][columna] = "X"
        venta["asiento"] = asiento_nuevo
        print(f"Asiento cambiado a {asiento_nuevo}.")

    else:
        dni = venta.get("dni", "")
        if dni not in pasajeros:
            print("No se encontraron los datos de este pasajero.")
            return



    GuardarDatos()

def BuscarVenta():
    print("=" * 50)
    print("BUSCAR VENTAS POR DNI".center(50))
    print("=" * 50)

    dni = PedirDNI()
    encontradas = BuscarVentasPorDNI(dni)

    if len(encontradas) == 0:
        print("No hay ventas para ese DNI.")
        return

    if dni in pasajeros:
        pasajero = pasajeros[dni]
        print(f"\nPasajero: {pasajero['nombre']} {pasajero['apellido']} - Tel: {pasajero['telefono']}")
    
    for venta in encontradas:
        print("-" * 50)
        print(f"Viaje ID: {venta.get('viaje_id', '-')}")
        print(f"Destino: {venta['destino']}")
        print(f"Fecha: {venta['fecha']}")
        print(f"Asiento: {venta['asiento']}")
        print(f"Precio: ${venta['precio']}")

def VerVentas():
    print("=" * 50)
    print("VENTAS REGISTRADAS".center(50))
    print("=" * 50)

    if len(ventas) == 0:
        print("No hay ventas registradas.")
        return

    for i in range(len(ventas)):
        venta = ventas[i]
        dni = venta.get("dni", "-")

        if dni in pasajeros:
            pasajero = pasajeros[dni]
            nombre_completo = f"{pasajero['nombre']} {pasajero['apellido']}"
        else:
            nombre_completo = "Pasajero desconocido"

        print(f"Venta N°: {i + 1}")
        print(f"Pasajero: {nombre_completo} (DNI {dni})")
        print(f"Destino: {venta['destino']}")
        print(f"Fecha: {venta['fecha']}")
        print(f"Asiento: {venta['asiento']}")
        print(f"Patente: {venta['patente']}")
        print(f"Precio: ${venta['precio']}")
        print("-" * 50)

def BuscarVentasPorDNI(dni, indice=0):
    if indice == len(ventas):
        return []

    resto = BuscarVentasPorDNI(dni, indice + 1)

    if ventas[indice].get("dni") == dni:
        return [ventas[indice]] + resto
    return resto

def EliminarVentasDeViajes(ids_eliminados):
    ventas[:] = [
        venta for venta in ventas
        if venta.get("viaje_id") not in ids_eliminados
    ]



def BuscarViajePorId(viaje_id):
    for i in range(len(viajes)):
        if viajes[i]["id"] == viaje_id:
            return i
    return -1

############################## Asientos ##################################
#OK
def CrearMatriz():
    matriz = []

    for f in range(FILAS):
        matriz.append(["O"] * COLUMNAS)

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

def ElegirAsiento(matriz):
    while True:
        asiento = input("Ingrese el asiento (ej. 1A o 10D): ").upper().strip()
        fila, columna = ConvertirAsiento(asiento)

        if fila == -1:
            print(f"Asiento inválido. Use una fila del 1 al {FILAS} y una letra de A a D.")
            continue

        if matriz[fila][columna] == "X":
            print("El asiento seleccionado ya está ocupado.")
            continue

        return asiento, fila, columna


def ConvertirAsiento(asiento):
    letras = "ABCD"
    asiento = asiento.upper().strip()

    try:
        fila = int(asiento[:-1])
        columna = letras.index(asiento[-1])
    except (ValueError, IndexError):
        return -1,-1
    
    if fila < 1 or fila > FILAS:
        return -1,-1

    return fila - 1, columna

def CancelarAsiento(matriz, asiento):
    fila, columna = ConvertirAsiento(asiento)

    if fila == -1:
        print("Asiento inválido.")
        return False

    if matriz[fila][columna] == "O":
        print("Ese asiento ya está libre.")
        return False

    matriz[fila][columna] = "O"
    return True

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

#####################################  Ventas ###############################
def PedirOpcion(mensaje, minimo, maximo):
    while True:
        try:
            opcion = int(input(mensaje))
            if opcion < minimo or opcion > maximo:
                print(f"Error: ingrese un número entre {minimo} y {maximo}.")
                continue
            return opcion
        except ValueError:
            print("Error: debe ingresar un número.")


def RegistrarVenta():
    if len(viajes) == 0:
        print("No hay viajes registrados. Primero registre un viaje.")
        return

    destinos_con_viajes = []
    for viaje in viajes:
        if viaje["destino"] not in destinos_con_viajes:
            destinos_con_viajes.append(viaje["destino"])

    print("\nDESTINOS CON VIAJES PROGRAMADOS")
    for i in range(len(destinos_con_viajes)):
        print(f"{i + 1} - {destinos_con_viajes[i]}")

    opcion = PedirOpcion("\nSeleccione un destino (0 para volver): ", 0, len(destinos_con_viajes))
    if opcion == 0:
        return
    destino_elegido = destinos_con_viajes[opcion - 1]

    viajes_destino = []
    for viaje in viajes:
        if viaje["destino"] == destino_elegido:
            viajes_destino.append(viaje)

    print("\nVIAJES PARA", destino_elegido.upper())
    for i in range(len(viajes_destino)):
        viaje = viajes_destino[i]
        libres = FILAS * COLUMNAS - ContarAsientosOcupados(viaje["asientos"])
        print(f"{i + 1} - ID: {viaje['id']} | Fecha: {viaje['fecha']} | "
              f"Micro: {viaje['patente']} | Libres: {libres}")

    opcion_viaje = PedirOpcion("\nSeleccione un viaje (0 para volver): ", 0, len(viajes_destino))

    if opcion_viaje == 0:
        return
    viaje_elegido = viajes_destino[opcion_viaje - 1]

    matriz = viaje_elegido["asientos"]
    if ContarAsientosOcupados(matriz) == FILAS * COLUMNAS:
        print("Ese viaje no tiene asientos disponibles.")
        return

    ImprimirMatriz(matriz)
    asiento, fila, columna = ElegirAsiento(matriz)

    print("\nDATOS DEL PASAJERO")
    dni = ObtenerPasajero()

    precio = distancias[destino_elegido] * TARIFAPORKM
    pasajero = pasajeros[dni]

    print("\n" + "=" * 40)
    print("RESUMEN DE LA VENTA".center(40))
    print("=" * 40)
    print(f"Pasajero: {pasajero['nombre']} {pasajero['apellido']} (DNI {dni})")
    print(f"Destino: {destino_elegido}")
    print(f"Fecha: {viaje_elegido['fecha']}")
    print(f"Asiento: {asiento}")
    print(f"Precio: ${precio}")
    print("=" * 40)

    confirmar = input("¿Confirmar la venta? (S/N): ").strip().upper()
    if confirmar != "S":
        print("Venta cancelada. El asiento sigue libre.")
        return

    matriz[fila][columna] = "X"

    venta = {
        "viaje_id": viaje_elegido["id"],
        "dni": dni,
        "destino": destino_elegido,
        "fecha": viaje_elegido["fecha"],
        "patente": viaje_elegido["patente"],
        "asiento": asiento,
        "precio": precio
    }
    ventas.append(venta)
    GuardarDatos()
    print("Venta registrada correctamente.")


def SeleccionarVenta():
    dni = PedirDNI()
    encontradas = BuscarVentasPorDNI(dni)

    if len(encontradas) == 0:
        print("No hay ventas para ese DNI.")
        return {}

    print("\nVENTAS DEL PASAJERO")
    for i in range(len(encontradas)):
        venta = encontradas[i]
        print(f"{i + 1} - Viaje ID: {venta.get('viaje_id', '-')} | {venta['destino']} | "
              f"Fecha: {venta['fecha']} | Asiento: {venta['asiento']}")

    opcion = PedirOpcion("\nSeleccione la venta (0 para volver): ", 0, len(encontradas))
    if opcion == 0:
        return {}
    return encontradas[opcion - 1]
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

######################################  Informes ###############################

def InformeVentasPorDestino():
    recaudacionPorDestino = {}
    for venta in ventas:
        destino = venta["destino"]
        if destino in recaudacionPorDestino:
            recaudacionPorDestino[destino] += venta["precio"]
        else:
            recaudacionPorDestino[destino] = venta["precio"]

    print("=" * 50)
    print("INFORME DE VENTAS POR DESTINO".center(50))
    print("=" * 50)

    if len(recaudacionPorDestino) == 0:
        print("No hay ventas registradas.")
        return

    for destino in recaudacionPorDestino:
        print(f"Destino: {destino}")
        print(f"Recaudación: ${recaudacionPorDestino[destino]}")
        print("-" * 50)


def InformeVentasPorFecha():
    recaudacionPorFecha = {}
    for venta in ventas:
        fecha = venta["fecha"]
        if fecha in recaudacionPorFecha:
            recaudacionPorFecha[fecha] += venta["precio"]
        else:
            recaudacionPorFecha[fecha] = venta["precio"]

    print("=" * 50)
    print("INFORME DE VENTAS POR FECHA".center(50))
    print("=" * 50)

    if len(recaudacionPorFecha) == 0:
        print("No hay ventas registradas.")
        return

    for fecha in recaudacionPorFecha:
        print(f"Fecha: {fecha}")
        print(f"Recaudación: ${recaudacionPorFecha[fecha]}")
        print("-" * 50)


def InformeRecaudacionTotal():
    recaudacionTotal = 0
    for venta in ventas:
        recaudacionTotal += venta["precio"]

    print("=" * 50)
    print("INFORME DE RECAUDACIÓN TOTAL".center(50))
    print("=" * 50)
    print(f"Cantidad de pasajes vendidos: {len(ventas)}")
    print(f"Recaudación Total: ${recaudacionTotal}")
    print("-" * 50)
############################## Pasajeros ##################################

def PedirDNI():
    dni = input("Ingrese el DNI del pasajero: ").strip()
    while not re.match(r"^[0-9]{7,8}$", dni):
        print("Error: el DNI debe tener 7 u 8 números, sin puntos.")
        dni = input("Ingrese el DNI del pasajero: ").strip()
    return dni


def PedirTexto(campo):
    texto = " ".join(input(f"Ingrese el {campo} del pasajero: ").split()).title()
    while not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", texto):
        print(f"Error: el {campo} solo puede tener letras y no puede estar vacío.")
        texto = " ".join(input(f"Ingrese el {campo} del pasajero: ").split()).title()
    return texto


def PedirTelefono():
    telefono = input("Ingrese el teléfono del pasajero: ").strip()
    while not re.match(r"^[0-9]{8,13}$", telefono):
        print("Error: el teléfono debe tener entre 8 y 13 números.")
        telefono = input("Ingrese el teléfono del pasajero: ").strip()
    return telefono

def ObtenerPasajero():
    dni = PedirDNI()

    if dni in pasajeros:
        pasajero = pasajeros[dni]
        print(f"Pasajero ya registrado: {pasajero['nombre']} {pasajero['apellido']}")
        return dni

    print("Pasajero nuevo, complete sus datos.")
    nombre = PedirTexto("nombre")
    apellido = PedirTexto("apellido")
    telefono = PedirTelefono()

    pasajeros[dni] = {
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono
    }
    return dni


