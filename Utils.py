import re
import time
import random
import json

############################## Datos #################################

# Estructuras de datos del sistema (se cargan desde datos.json al arrancar):
#   distancias: diccionario de diccionarios con los km entre terminales. Las claves de
#     afuera son las terminales. Ejemplo: distancias["Buenos Aires"]["Rosario"] = 300.
#   micros: lista de diccionarios, uno por micro. Ejemplo: {"patente": "AB123CD"}.
#   patentes: conjunto con las patentes de los micros, para controlar rápido que no se
#     repitan.
#   viajes: lista de diccionarios, uno por viaje, con: id, salida, destino, patente, fecha
#     y "asientos", que es la matriz de 10 x 4 ("O" = libre, "X" = ocupado).
#   ventas: lista de diccionarios, uno por pasaje vendido, con: viaje_id, salida, destino,
#     fecha, patente, nombre, dni, asiento y precio.
# Constantes:
#   FILAS y COLUMNAS: tamaño de la matriz de asientos (10 x 4 = 40 asientos por micro).
#   TARIFAPORKM: precio por kilómetro. El pasaje cuesta distancia x TARIFAPORKM.
#   ARCHIVO_JSON: nombre del archivo donde se guardan los datos.
#   nombres y apellidos: listas que usa GenerarVentasAlAzar() para inventar pasajeros.

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

# Esta función se ejecuta una sola vez, al arrancar el programa, y lo que hace es leer
# datos.json y pasar su contenido a las estructuras globales: distancias, micros, patentes,
# viajes y ventas.
#
# Abrimos el archivo en modo lectura ("rt") dentro de un try y lo convertimos a diccionario
# con json.load(). Manejamos tres errores: si el archivo no existe (FileNotFoundError)
# simplemente arrancamos vacíos, y si está dañado (ValueError) o no se puede leer (OSError)
# mostramos el error. En el finally lo cerramos, y ese close está dentro de otro try con
# except NameError porque, si el open falló, la variable arch nunca llegó a crearse.
#
# La variable cargado la usamos para copiar los datos solo si la lectura salió bien. Para
# copiarlos usamos .get(clave, valor por defecto), así si en el archivo falta alguna clave
# el programa no se rompe. Las patentes vienen del JSON como lista y acá las volvemos a
# meter en el conjunto con .add(). Usamos extend() y no una asignación (viajes = ...) porque
# la asignación crearía una variable local y la lista global quedaría vacía.
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

# Esta función guarda todo el sistema en datos.json. La llamamos al final de cada operación
# que cambia algo (una venta, un viaje, un micro, una terminal), así si se cierra el
# programa no se pierde nada.
#
# Primero armamos un diccionario datos con las cinco estructuras. Al conjunto patentes lo
# pasamos a lista con list() porque JSON no sabe guardar conjuntos. Después abrimos el
# archivo en modo escritura ("wt"), que lo crea si no existe y lo pisa si ya existe, y lo
# grabamos con json.dump(). Igual que al cargar, si hay un OSError mostramos el error, y el
# archivo se cierra en el finally con el try/except NameError.
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

# Esta función muestra el menú principal con las seis secciones del sistema y le pide al
# usuario que elija una. Devuelve lo que escribió tal cual, como texto, y en main.py lo
# convertimos a número con ConvertirOpcion().
#
# Para el diseño usamos operaciones de cadenas: "=" * 50 repite el signo igual 50 veces para
# hacer la línea, y .center(50) centra el título en ese mismo ancho. Todos los menús siguen
# este mismo formato.
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

# Esta función muestra el menú de Ventas: registrar una venta, ver las ventas de un viaje,
# buscar una venta para cancelarla o cambiarle el asiento, o volver. Funciona igual que el
# menú principal: imprime las opciones y devuelve lo que escribió el usuario como texto, que
# después se convierte con ConvertirOpcion().
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

# Este menú aparece cuando el usuario quiere buscar una venta. Le ofrecemos tres formas de
# buscarla: por viaje y asiento, por DNI o por nombre, y una cuarta opción para volver.
# Igual que los otros menús, devuelve la opción como texto.
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

# Este menú aparece cuando ya encontramos una venta, y pregunta qué hacer con ella:
# cancelarla, cambiarle el asiento o volver. La diferencia con los otros menús es que acá le
# aplicamos .strip() a la respuesta, porque GestionarVenta() la compara directamente con los
# textos "1", "2" y "3" en lugar de convertirla a número, y así un espacio de más no hace
# que la opción sea inválida.
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

# Esta función muestra el menú de Informes, donde se puede ver la recaudación por destino,
# por mes o la total. Como todos los menús, devuelve la opción como texto.
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

# Esta función muestra el menú de Viajes: consultar la disponibilidad de asientos, registrar
# un viaje nuevo o ver todos los viajes. Como todos los menús, devuelve la opción como
# texto.
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

# Esta función muestra el menú de Micros: ver los micros, registrar uno nuevo o darlo de
# baja. Como todos los menús, devuelve la opción como texto.
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

# Esta función muestra el menú de Terminales: ver las terminales, agregar una nueva o
# eliminarla. Como todos los menús, devuelve la opción como texto.
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

# Esta es la función que vende un pasaje, y es la más larga del sistema porque recorre todo
# el proceso de una venta. Primero controlamos que haya viajes cargados; si no hay, no se
# puede vender nada.
#
# Después armamos la lista destinos solo con los destinos que tienen al menos un viaje, y
# usamos "not in" para no repetirlos. Así nunca le ofrecemos al usuario un destino al que no
# va ningún micro. Mostramos los destinos numerados, con el 0 para volver, y validamos que
# lo que escriba sea un número (con try/except ValueError) y que esté en rango. Si elige 0
# ponemos la variable volver en True y salimos del ciclo con break; no hacemos el return
# adentro del while porque en la materia no se sale de una función desde adentro de un
# ciclo.
#
# Con el destino elegido armamos viajes_destino, que son los viajes que van ahí, y el
# usuario elige uno con ElegirDeLista(). Tomamos la matriz de asientos de ese viaje y, si
# está completa (los ocupados son FILAS * COLUMNAS), avisamos y terminamos.
#
# Si hay lugar, mostramos el mapa de asientos y el usuario elige uno con ElegirAsiento(),
# que ya lo marca con "X". El precio lo calculamos multiplicando los km entre la salida y el
# destino por TARIFAPORKM.
#
# Después pedimos el DNI. Si ese DNI ya compró antes (lo buscamos con BuscarVentasPorDni(),
# que es recursiva) reutilizamos su nombre, y si es nuevo se lo pedimos con
# IngresarNombre(). Esto evita que la misma persona quede cargada con dos nombres distintos.
#
# Por último mostramos un resumen y pedimos confirmación. Si dice que no, liberamos el
# asiento que habíamos marcado y no se guarda nada. Si confirma, armamos el diccionario de
# la venta, lo agregamos a la lista ventas y guardamos el archivo.
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

# Esta función muestra todas las ventas de un viaje. Primero mostramos la lista de viajes
# con VerViajes() para que el usuario vea los IDs, y le pedimos uno. Si no escribe un
# número, el except ValueError muestra el error.
#
# Con el ID buscamos el viaje usando BuscarViajePorId(), que es recursiva; si devuelve None
# es porque ese ID no existe. Después recorremos la lista ventas y mostramos, con
# MostrarVenta(), las que tienen ese viaje_id. La variable cantidad la usamos para numerar
# las ventas y, al final, para saber si el viaje no tenía ninguna o para mostrar el total.
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

# Esta función recibe una venta, que es un diccionario, y muestra todos sus datos. La
# separamos en una función porque la usamos en varios lugares: al ver las ventas de un viaje
# y al gestionar una venta encontrada.
#
# El precio lo mostramos con FormatoPrecio() para que tenga los puntos de miles. Para el DNI
# usamos .get('dni', '-') en lugar de corchetes: si alguna venta no tuviera DNI, muestra un
# guión en vez de tirar un KeyError.
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

# Esta función cancela una venta. Recibe la venta y la matriz de asientos de su viaje.
# Primero pedimos confirmación con Confirmar(), porque es una acción que no se puede
# deshacer; si dice que no, no hacemos nada.
#
# Si confirma, volvemos a poner el asiento en "O" con LiberarAsiento(), sacamos la venta de
# la lista con .remove() y guardamos el archivo. No hace falta devolver la matriz porque las
# listas son mutables: al modificarla acá adentro, el cambio queda hecho en el viaje
# original.
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

# Esta es la primera forma de buscar una venta: por viaje y asiento. Mostramos los viajes,
# pedimos el ID y buscamos el viaje con BuscarViajePorId(). Después le mostramos el mapa de
# asientos para que vea cuáles están ocupados y le pedimos el asiento. A lo que escribe le
# aplicamos .upper() y .strip(), así "3b " se toma igual que "3B".
#
# Con el ID y el asiento buscamos la venta con BuscarVentaPorAsiento(), que también es
# recursiva. La función devuelve la venta encontrada, o None si algo falló o si ese asiento
# no tiene venta; en main.py solo llamamos a GestionarVenta() cuando no es None.
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

# Esta es la segunda forma de buscar una venta: por DNI. Pedimos el DNI con IngresarDni(),
# que ya se encarga de validarlo. Después BuscarVentasPorDni(), que es recursiva, nos
# devuelve una lista con todas las ventas de ese DNI, porque una misma persona puede haber
# comprado varios pasajes.
#
# Si la lista está vacía avisamos y devolvemos None. Si no, se la pasamos a
# ElegirVentaDeLista() para que el usuario elija con cuál quiere trabajar.
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

# Esta es la tercera forma de buscar una venta: por nombre. Pedimos un texto y con un while
# no dejamos que quede vacío, porque un texto vacío coincidiría con todas las ventas.
#
# La búsqueda acepta coincidencias parciales y no distingue mayúsculas, así que escribiendo
# "per" encontramos a "Juan Perez". Eso lo hace BuscarVentasPorNombre(), que es recursiva y
# devuelve la lista de coincidencias. Igual que en la búsqueda por DNI, si no hay ninguna
# devolvemos None, y si hay, el usuario elige una con ElegirVentaDeLista().
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

# Esta función la usan las búsquedas por DNI y por nombre cuando encuentran ventas, para que
# el usuario elija una. Si hay una sola, la devolvemos directamente sin preguntar nada.
#
# Si hay varias, las mostramos numeradas, armando cada renglón por partes con +=, y pedimos
# un número entre 0 y la cantidad, donde 0 es volver. Validamos con try/except que sea un
# número y con un if que esté en rango.
#
# La variable elegida arranca en None: si el usuario elige una venta la guardamos ahí, y si
# elige 0 queda en None. Salimos del ciclo con break y el return queda afuera del while,
# como pide la materia.
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

# Esta función se llama cuando una búsqueda encontró una venta, y deja cancelarla o
# cambiarle el asiento. Para las dos cosas necesitamos la matriz de asientos del viaje, así
# que primero buscamos el viaje con BuscarViajePorId() usando el viaje_id que tiene guardado
# la venta.
#
# Después mostramos la venta y el menú de gestión, y con un while lo repetimos hasta que la
# opción sea "1", "2" o "3". Con 1 llamamos a CancelarVenta(), con 2 a CambiarAsiento(), y
# con 3 no hacemos nada y volvemos al menú de búsqueda.
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

# Esta función busca un viaje por su ID en forma recursiva, usando la técnica de "divide y
# vencerás" que vimos en la Clase 10. Los parámetros inicio y fin marcan el pedazo de la
# lista donde estamos buscando. Desde afuera la llamamos solo con el ID: inicio vale 0 por
# omisión, y fin arranca en None y en la primera llamada lo completamos con len(viajes).
#
# Tiene dos casos base. Si el pedazo está vacío, devolvemos None porque no hay nada que
# buscar. Si el pedazo tiene un solo viaje, lo comparamos: si es el ID que buscamos lo
# devolvemos, y si no, devolvemos None.
#
# En el caso recursivo partimos el pedazo a la mitad, calculando medio = (inicio + fin) //
# 2. Buscamos primero en la mitad izquierda y, solo si no lo encontramos ahí, buscamos en la
# mitad derecha.
#
# Elegimos partir a la mitad en lugar de avanzar de a un elemento porque así la profundidad
# de la recursión es muy chica: con 1000 viajes son unos 10 niveles, entonces nunca llegamos
# al límite de recursión de Python (RecursionError).
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

# Esta función busca la venta de un asiento en un viaje determinado, y la usamos en la
# búsqueda por viaje y asiento. Funciona exactamente igual que BuscarViajePorId(): parte la
# lista ventas a la mitad en cada llamada.
#
# Los casos base son el pedazo vacío, que devuelve None, y el pedazo de un solo elemento,
# donde comparamos que coincidan tanto el viaje_id como el asiento. Tenemos que comparar los
# dos porque el asiento "3B" existe en todos los viajes. En el caso recursivo buscamos
# primero en la mitad izquierda y, si no está, en la derecha.
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

# Esta función busca todas las ventas de un DNI, también en forma recursiva y partiendo la
# lista a la mitad. La diferencia con las búsquedas anteriores es que no cortamos en la
# primera coincidencia, porque una persona puede tener varios pasajes. Por eso buscamos
# siempre en las dos mitades y vamos juntando los resultados en la lista encontrados, que se
# pasa de una llamada a la otra.
#
# Los casos base son el pedazo vacío, donde no agregamos nada, y el pedazo de un solo
# elemento, donde agregamos la venta si el DNI coincide.
#
# Un detalle importante: encontrados arranca en None y la lista la creamos en la primera
# llamada. Si pusiéramos encontrados=[] directamente en el def, Python usaría siempre la
# misma lista para todas las búsquedas, y los resultados de una búsqueda se mezclarían con
# los de la anterior.
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

# Esta función busca todas las ventas cuyo nombre de pasajero contenga un texto. Funciona
# igual que BuscarVentasPorDni(): parte la lista a la mitad, busca en las dos mitades y
# junta los resultados en encontrados.
#
# Lo único que cambia es la comparación del caso base: pasamos el texto y el nombre a
# minúsculas con .lower() y usamos el operador in para ver si el texto está dentro del
# nombre. Así, escribiendo "per" o "PEREZ", encontramos a "Juan Perez".
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

# Esta función cuenta cuántos asientos ocupados tiene un viaje. Recibe la matriz de asientos
# y la recorremos sin subíndices, como en la Clase 04: el primer for toma cada fila y el
# segundo cada asiento de esa fila. Cada vez que encontramos una "X" sumamos 1.
#
# La usamos en varios lugares: para saber si un viaje está completo, para mostrar los
# lugares libres y para calcular la recaudación.
def ContarAsientosOcupados(asientos):
    ocupados = 0

    for fila in asientos:
        for asiento in fila:
            if asiento == "X":
                ocupados += 1

    return ocupados

# Esta función muestra el mapa de asientos de un viaje, como si fuera el micro visto desde
# arriba. Primero imprimimos el encabezado con las columnas A y B, el pasillo, y C y D.
# Después recorremos la matriz por filas e imprimimos el número de fila y sus cuatro
# asientos.
#
# Para el número de fila usamos {f+1:>2} en el f-string, que lo alinea a la derecha en dos
# lugares, así la fila 10 no desacomoda el dibujo. Al final mostramos la referencia: "O" es
# libre y "X" es ocupado.
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

# Esta función le pide al usuario un asiento, controla que sea válido y que esté libre, y lo
# marca como ocupado. El asiento se escribe como número de fila más letra, por ejemplo "3B".
# Para separarlo usamos rebanadas: asiento[:-1] es todo menos el último carácter, o sea la
# fila, y asiento[-1] es el último, o sea la letra. La fila la pasamos a número con int() y
# la letra a número de columna con un if/elif, donde A es 0, B es 1, C es 2 y D es 3.
#
# Controlamos que la fila esté entre 1 y FILAS, que la letra sea A, B, C o D, y que ese
# lugar de la matriz no tenga una "X". Si el usuario escribe algo sin formato, como una "A"
# sola o nada, el int() o el índice fallan y el except (ValueError, IndexError) muestra el
# error y vuelve a preguntar.
#
# Cuando el asiento es válido, ponemos la "X" en la matriz y devolvemos el asiento armado de
# nuevo con str(x) + letra; así, si escribió "03b", lo guardamos como "3B". Hay que tener en
# cuenta que el asiento queda ocupado apenas se elige: si después la venta no se confirma,
# RegistrarVenta() lo libera.
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

# Esta función hace lo contrario de ElegirAsiento(): deja libre un asiento, volviéndole a
# poner "O" en la matriz. Separa la fila y la letra con rebanadas de la misma forma, pasa la
# letra a número de columna y le resta 1 a la fila porque la matriz empieza en 0.
#
# No validamos el asiento porque a esta función solo la llamamos con asientos que vienen de
# ventas que ya existen, y que ya se validaron al venderse. No devuelve nada porque la
# matriz es mutable y el cambio queda hecho en el viaje.
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

# Esta función le cambia el asiento a una venta. Primero liberamos el asiento actual con
# LiberarAsiento(). Lo hacemos antes de mostrar el mapa a propósito, para que el asiento
# anterior aparezca libre y el pasajero pueda volver a elegirlo si se arrepiente.
#
# Después pedimos el nuevo asiento con ElegirAsiento(), que ya lo marca como ocupado, lo
# guardamos en venta["asiento"] y grabamos el archivo.
def CambiarAsiento(venta, matriz):
    asiento_anterior = venta["asiento"]

    LiberarAsiento(matriz, asiento_anterior)

    print("Seleccione el nuevo asiento:")
    ImprimirMatriz(matriz)

    nuevo_asiento = ElegirAsiento(matriz)

    venta["asiento"] = nuevo_asiento

    GuardarDatos()

    print("Asiento modificado correctamente.")

# Esta función crea la matriz de asientos de un viaje nuevo, con todos los lugares libres.
# Es una lista de listas de FILAS x COLUMNAS, o sea 10 filas de 4 asientos. Por cada fila
# agregamos una lista hecha con ["O"] * COLUMNAS, que repite la "O" cuatro veces. Es la
# "Alternativa 3" para crear matrices que vimos en la Clase 04.
#
# Usamos las constantes en lugar de poner 10 y 4 a mano, así si cambia el tamaño del micro
# se modifica en un solo lugar.
def CrearMatriz():
    matriz = []

    for f in range(FILAS):
        matriz.append(["O"] * COLUMNAS)

    return matriz

############################## Informes ##############################

# Esta función muestra cuánto se recaudó con los viajes a cada destino. Usamos un
# diccionario, recaudacion_por_destino, donde la clave es el destino y el valor es lo
# recaudado.
#
# Recorremos todos los viajes y, con CalcularRecaudacionViaje(), sumamos lo de cada uno en
# su destino: si el destino ya está en el diccionario le sumamos, y si no, lo creamos. Al
# final mostramos los destinos en orden alfabético con sorted(), alineados con {destino:<15}
# para que los montos queden en columna, y con el precio formateado con FormatoPrecio().
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

# Esta función muestra cuánto se recaudó en cada mes, en orden cronológico. La lista meses
# la usamos para mostrar el nombre del mes en lugar del número, con meses[mes - 1] porque la
# lista empieza en 0.
#
# Para cada viaje separamos la fecha con .split("/") y armamos la clave (año, mes), que es
# una tupla. Usamos una tupla por dos motivos: primero, porque las claves de un diccionario
# tienen que ser inmutables, así que una lista no se podría usar; y segundo, porque las
# tuplas se ordenan comparando elemento por elemento, primero el año y después el mes, así
# sorted() pone Diciembre 2026 antes que Enero 2027. Si usáramos solo el mes, se mezclarían
# los años.
#
# Al mostrar, desempaquetamos la tupla con anio, mes = clave. La recaudación se acumula
# igual que en el informe por destino.
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

# Esta función muestra cuánto se recaudó en total. Arrancamos recaudacion_total en 0 y le
# vamos sumando con += lo que recaudó cada viaje, calculado con CalcularRecaudacionViaje().
# Al final lo mostramos con FormatoPrecio(). Si no hay viajes, el for no entra y se muestra
# $0.
def MostrarRecaudacionTotal():
    recaudacion_total = 0

    for viaje in viajes:
        recaudacion_total += CalcularRecaudacionViaje(viaje)

    print("=" * 50)
    print("RECAUDACIÓN TOTAL".center(50))
    print("=" * 50)
    print(f"Recaudación total: ${FormatoPrecio(recaudacion_total)}")
    print("-" * 50)

# Esta función calcula cuánta plata se recaudó con un viaje. Multiplicamos la cantidad de
# asientos ocupados, que contamos con ContarAsientosOcupados(), por los km entre la salida y
# el destino y por TARIFAPORKM.
#
# Da lo mismo que sumar el precio de cada venta del viaje, porque todos los pasajes de un
# mismo viaje cuestan lo mismo. La separamos en una función porque la usan los tres
# informes.
def CalcularRecaudacionViaje(viaje):
    asientos_ocupados = ContarAsientosOcupados(viaje["asientos"])
    kilometros = distancias[viaje["salida"]][viaje["destino"]]

    return asientos_ocupados * kilometros * TARIFAPORKM

############################## Viajes ################################

# Esta función muestra una tabla con todos los viajes y cuántos lugares libres le quedan a
# cada uno, y después el mapa de asientos del viaje que elija el usuario.
#
# Para que la tabla quede alineada, primero calculamos el ancho de cada columna según el
# texto más largo: arrancamos con el largo del título y recorremos los viajes buscando la
# salida y el destino más largos. Después armamos el encabezado y cada fila por partes con
# +=, usando .rjust() y .ljust() para alinear a derecha o izquierda, y f-strings con ancho
# fijo para la fecha y la patente.
#
# Los lugares libres los calculamos como FILAS * COLUMNAS menos los ocupados. Al final el
# usuario elige un viaje con ElegirDeLista() y le mostramos sus datos y su mapa con
# ImprimirMatriz().
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

# Esta función registra un viaje nuevo. Primero controlamos que haya al menos 2 terminales,
# porque un viaje necesita una salida y un destino distintos, y al menos un micro.
#
# El ID lo calculamos así: si no hay viajes es 1, y si hay, es el ID del último más 1. Esto
# funciona porque los viajes siempre se agregan al final de la lista, entonces el último es
# el que tiene el ID más alto.
#
# Después el usuario elige la terminal de salida con ElegirTerminal() y el destino con
# ElegirDestino(), que ya no le muestra la terminal de salida. Elige el micro con
# ElegirDeLista() y le pedimos la fecha con IngresarFecha().
#
# Con la fecha controlamos que ese micro no tenga otro viaje el mismo día, porque un micro
# no puede estar en dos lugares a la vez. Para eso recorremos los viajes con la variable
# ocupado y cortamos con break en cuanto encontramos uno; si está ocupado, pedimos otra
# fecha.
#
# Por último creamos la matriz vacía con CrearMatriz(), guardamos todo en el diccionario
# viaje, lo agregamos a la lista viajes y grabamos el archivo. La línea comentada llama a
# GenerarVentasAlAzar(), que llena el viaje con pasajeros de prueba; la dejamos comentada
# para que los viajes nuevos arranquen sin ventas.
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
    # matriz = GenerarVentasAlAzar(salida, destino_elegido, fecha, matriz, patente, viaje["id"])
    viaje["asientos"] = matriz

    viajes.append(viaje)
    GuardarDatos()

    print("Viaje registrado correctamente.")

# Esta función la hicimos para tener datos de prueba: llena un viaje con pasajeros al azar.
# Recorremos la matriz asiento por asiento con dos for, y random.randint(0, 1) decide si
# cada asiento se ocupa, así que más o menos la mitad queda ocupada.
#
# Si el asiento se ocupa, ponemos la "X", armamos el nombre del asiento con la fila y la
# letra, elegimos un nombre y un apellido al azar de las listas nombres y apellidos,
# generamos un DNI al azar de 8 dígitos y agregamos la venta a la lista ventas con el precio
# del viaje. Devuelve la matriz ya cargada.
#
# Hoy no se usa, porque su llamada en RegistrarViaje() está comentada; la usamos para cargar
# los viajes de prueba.
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

# Esta función muestra todos los viajes programados con su ID, salida, destino, fecha y
# patente. Simplemente recorremos la lista viajes y mostramos los datos de cada diccionario.
# Además de usarla en el menú de Viajes, la llamamos desde VerVentas() y
# SeleccionarVentaPorAsiento(), para que el usuario vea los IDs antes de tener que escribir
# uno.
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

# Esta función muestra todos los micros y, para cada uno, los destinos a los que tiene
# viajes. Por cada micro recorremos la lista de viajes y armamos destinos_micro con los
# destinos de los viajes que tienen esa patente. Usamos "not in" para no repetir un destino
# si el micro va varias veces al mismo lugar. Si la lista queda vacía, mostramos "Sin viajes
# asignados".
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

# Esta función registra un micro nuevo a partir de su patente. Pedimos la patente y la
# pasamos a mayúsculas con .upper(), así se puede escribir en minúsculas.
#
# La validamos con la expresión regular ^[A-Z][A-Z][0-9][0-9][0-9][A-Z][A-Z]$, que pide dos
# letras, tres números y dos letras, como AB123CD; el ^ y el $ hacen que tenga que ser
# exactamente eso, sin nada antes ni después. También controlamos que la patente no esté
# repetida buscándola en el conjunto patentes. Usamos un conjunto porque no admite elementos
# repetidos y es muy rápido para preguntar si un dato está.
#
# Mientras la patente sea inválida o esté repetida, mostramos el error que corresponde y la
# volvemos a pedir. Cuando es válida, agregamos el micro a la lista micros, la patente al
# conjunto y guardamos.
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

# Esta función da de baja un micro, y junto con él borra sus viajes y las ventas de esos
# viajes, porque si el micro ya no existe esos viajes no se pueden hacer. Mostramos los
# micros numerados, el usuario elige uno con ElegirDeLista() y le pedimos confirmación. Si
# confirma, sacamos el micro de la lista con .remove() y su patente del conjunto con
# .discard().
#
# Para borrar los viajes y las ventas usamos listas por comprensión: armamos una lista nueva
# solo con los que NO son de ese micro. Después vaciamos la lista original con .clear() y le
# cargamos la nueva con .extend(). No hacemos directamente viajes = viajes_nuevos porque,
# dentro de una función, eso crearía una variable local nueva y la lista global quedaría
# igual.
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

# Esta función muestra todas las terminales con la distancia a cada una de las demás. Las
# distancias las guardamos en un diccionario de diccionarios: la clave de afuera es una
# terminal y su valor es otro diccionario con los km a cada una de las otras. Por ejemplo,
# distancias["Buenos Aires"]["Rosario"] vale 300.
#
# Recorremos las terminales numerándolas con enumerate() y, para cada una, recorremos su
# diccionario interno mostrando los km.
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

# Esta función agrega una terminal nueva y pide la distancia hasta cada una de las que ya
# existen. Primero pedimos el nombre y lo limpiamos: " ".join(terminal.split()) saca los
# espacios de más, y .title() pone en mayúscula la primera letra de cada palabra, así "  san
# luis" queda "San Luis". Lo hacemos para que la misma terminal no pueda quedar cargada dos
# veces escrita de forma distinta.
#
# Validamos el nombre con una expresión regular que solo acepta letras (incluyendo tildes, ñ
# y ü) y espacios. También controlamos con "in" que la terminal no esté ya en el
# diccionario.
#
# Después, con IngresarKm(), pedimos la distancia a cada terminal existente y la guardamos
# en el diccionario kms, que pasa a ser el diccionario interno de la terminal nueva. Por
# último, en cada una de las otras terminales agregamos la distancia hacia la nueva.
# Guardamos cada distancia en los dos sentidos para poder consultarla desde cualquiera de
# las dos terminales, sin importar cuál sea la salida y cuál el destino.
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

# Esta función pide la distancia en km entre dos terminales y no la acepta hasta que sea un
# número entero mayor que cero. Recibe los nombres de las dos terminales solo para
# mostrarlos en la pregunta.
#
# Usamos un while True: si lo que escribe no es un número, el except ValueError muestra el
# error; si es cero o negativo, mostramos el error y el continue vuelve a preguntar. Cuando
# el número es válido salimos con break, y el return queda fuera del ciclo, como pide la
# materia.
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

# Esta función elimina una terminal, y con ella todos los viajes y ventas que salían o
# llegaban ahí. El usuario elige la terminal con ElegirTerminal() y le pedimos confirmación.
#
# Si confirma, la sacamos del diccionario distancias con .pop(), y además la sacamos del
# diccionario interno de cada una de las otras terminales, porque ahí también estaba
# guardada la distancia hacia ella. Después, con listas por comprensión, nos quedamos solo
# con los viajes y ventas que no salen ni llegan a esa terminal, y los copiamos a las listas
# originales con .clear() y .extend(), por el mismo motivo que en DarBajaMicro().
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

# Esta función muestra las terminales numeradas y deja elegir una. Como las terminales son
# las claves del diccionario distancias, las pasamos a una lista con
# list(distancias.keys()), porque para elegir por número necesitamos acceder por posición.
# Las mostramos con enumerate() y el usuario elige con ElegirDeLista(). Devuelve el nombre
# de la terminal elegida.
def ElegirTerminal():
    terminales = list(distancias.keys())

    print("\n" + "=" * 50)
    print("TERMINALES".center(50))
    print("=" * 50)

    for i, terminal in enumerate(terminales):
        print(f"{i + 1} - {terminal}")

    return ElegirDeLista(terminales, "Seleccione la terminal: ")

# Esta función muestra los destinos posibles desde una terminal de salida y deja elegir uno.
# Armamos la lista destinos con todas las terminales menos la de salida, porque no tiene
# sentido un viaje que sale y llega al mismo lugar. Los mostramos numerados con la distancia
# entre paréntesis, por ejemplo "2 - Rosario (300 km)", y el usuario elige con
# ElegirDeLista().
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

# Esta es una función general que usamos en todo el sistema para elegir un elemento de una
# lista escribiendo su número: terminales, destinos, micros y viajes. La hicimos genérica
# para no repetir la misma validación en cada lugar. Recibe la lista y el mensaje de la
# pregunta.
#
# Con un while True repetimos la pregunta hasta que se escriba un número entre 1 y el largo
# de la lista: si no es un número, el except ValueError muestra el error, y si está fuera de
# rango, el continue vuelve a preguntar. Salimos con break y el return queda afuera del
# ciclo.
#
# Como al usuario le mostramos la lista empezando en 1 pero en Python empieza en 0,
# devolvemos lista[opcion - 1]. O sea que devuelve el elemento elegido, no el número.
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

# Esta función pide el DNI del pasajero hasta que sea válido. Lo validamos con una expresión
# regular que tiene siete [0-9] obligatorios y un octavo [0-9] con "?", que significa que
# puede aparecer cero o una vez. Así aceptamos DNI de 7 u 8 números, sin puntos ni espacios;
# el ^ y el $ hacen que no pueda haber nada más.
#
# Lo guardamos como texto y no como número porque no hacemos cuentas con él, solo lo
# comparamos.
def IngresarDni():
    dni = input("Ingrese el DNI del pasajero (sin puntos): ").strip()

    while not re.search(r"^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]?$", dni):
        print("Error: el DNI debe tener 7 u 8 números, sin puntos ni espacios.")
        dni = input("Ingrese el DNI del pasajero (sin puntos): ").strip()

    return dni

# Esta función pide el nombre completo del pasajero hasta que sea válido. Primero lo
# limpiamos con " ".join(nombre.split()), que saca los espacios de más, y .title(), que pone
# la primera letra de cada palabra en mayúscula; así "  juan   perez " queda "Juan Perez".
#
# Después lo validamos con una expresión regular que solo acepta letras (incluyendo tildes,
# ñ y ü) y espacios. Además, con len(nombre.split()) controlamos que tenga al menos dos
# palabras, es decir nombre y apellido. Si algo no cumple, mostramos el error y volvemos a
# preguntar.
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

# Esta función recibe un número y lo devuelve como texto con puntos de miles; por ejemplo,
# 1234567 queda "1.234.567". La hicimos recursiva.
#
# El caso base es cuando el número es menor que 1000: no lleva puntos, así que lo devolvemos
# tal cual con str().
#
# En el caso recursivo separamos el número en dos partes: numero // 1000, que son los miles,
# y numero % 1000, que son los últimos tres dígitos. A los miles los formateamos llamando
# otra vez a la misma función, y les pegamos un punto y los últimos tres dígitos. El :03 del
# f-string completa con ceros adelante, así 1005 queda "1.005" y no "1.5".
#
# Por ejemplo, FormatoPrecio(1234567) es FormatoPrecio(1234) + ".567", que a su vez es
# FormatoPrecio(1) + ".234" + ".567", y eso da "1.234.567".
def FormatoPrecio(numero):
    if numero < 1000:
        return str(numero)
    else:
        return FormatoPrecio(numero // 1000) + "." + f"{numero % 1000:03}"

# Esta función hace una pregunta de sí o no y devuelve True o False. La usamos antes de
# cualquier acción importante: confirmar o cancelar una venta, dar de baja un micro o
# eliminar una terminal. Recibe el texto de la pregunta y le agregamos " (S/N): " al final.
#
# A la respuesta le aplicamos .strip() y .upper(), así "s" o " n " también sirven. Mientras
# no sea S ni N, mostramos un error y volvemos a preguntar. Al final devolvemos respuesta ==
# "S": esa comparación ya da True o False, así que no hace falta un if.
def Confirmar(mensaje):
    respuesta = input(mensaje + " (S/N): ").strip().upper()

    while respuesta != "S" and respuesta != "N":
        print("Error: responda S o N.")
        respuesta = input(mensaje + " (S/N): ").strip().upper()

    return respuesta == "S"

# Esta función pide la fecha de un viaje y la controla hasta que sea válida. La devuelve
# como texto en formato DD/MM/AAAA, que es como la guardamos. La validación la hacemos por
# pasos, y si alguno falla mostramos el error y la volvemos a pedir.
#
# Primero, que tenga tres partes separadas por "/", usando .split("/"). Segundo, que el día
# y el mes tengan 2 dígitos y el año 4. Tercero, que las tres partes sean números, con un
# try/except ValueError. Cuarto, que el mes esté entre 1 y 12.
#
# Quinto, que el día exista en ese mes. Para eso usamos el diccionario dias_por_mes, y si el
# año es bisiesto le cambiamos febrero a 29. Un año es bisiesto si es divisible por 4 y no
# por 100, o si es divisible por 400.
#
# Por último, que la fecha esté entre hoy y un año desde hoy. La fecha de hoy la sacamos con
# time.localtime(). Para comparar fechas armamos tuplas (año, mes, día): las tuplas se
# comparan elemento por elemento, primero el año, si empatan el mes y si empatan el día, que
# es justo como se comparan las fechas.
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
