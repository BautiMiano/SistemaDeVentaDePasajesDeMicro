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

# Qué hace: lee el archivo datos.json al arrancar el programa y copia su contenido a las
#   estructuras globales (distancias, micros, patentes, viajes y ventas). Si el archivo no
#   existe, el programa arranca vacío. Si está dañado o no se puede leer, muestra el error.
# Recibe: nada.
# Devuelve: nada. Modifica directamente las estructuras globales.
# Cómo funciona: abre el archivo en modo lectura ("rt") dentro de un try y lo convierte a
#   un diccionario con json.load(). En el finally lo cierra, con un try/except NameError por
#   si el archivo nunca se llegó a abrir. La variable "cargado" indica si la lectura salió
#   bien: solo en ese caso se copian los datos. Se usa .get(clave, valor) para que no falle
#   si en el archivo falta alguna clave.
# Estructuras y temas: archivos, JSON, excepciones (FileNotFoundError, ValueError, OSError),
#   diccionarios, listas y conjuntos.
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

# Qué hace: guarda todos los datos del sistema en datos.json. Se llama cada vez que termina
#   una operación que cambia algo (una venta, un viaje, un micro, una terminal), así no se
#   pierde nada aunque se cierre el programa.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: arma un diccionario "datos" con las cinco estructuras. El conjunto
#   "patentes" se convierte a lista con list() porque JSON no puede guardar conjuntos. Abre
#   el archivo en modo escritura ("wt"), que lo crea si no existe o lo reemplaza si ya
#   existe, lo graba con json.dump() y lo cierra en el finally.
# Estructuras y temas: archivos, JSON, excepciones (OSError), diccionarios, listas y conjuntos.
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

# Qué hace: muestra el menú principal con las 6 opciones del sistema y le pide al usuario
#   que elija una.
# Recibe: nada.
# Devuelve: la opción que escribió el usuario, como texto (string). main.py la convierte a
#   número con ConvertirOpcion().
# Estructuras y temas: cadenas ("=" * 50 dibuja la línea y .center(50) centra el título).
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

# Qué hace: muestra el menú de Ventas (registrar, ver, buscar o volver) y pide una opción.
# Recibe: nada.
# Devuelve: la opción escrita por el usuario, como texto.
# Estructuras y temas: cadenas (.center() y repetición con *).
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

# Qué hace: muestra las tres formas de buscar una venta (por viaje y asiento, por DNI o por
#   nombre) y pide una opción.
# Recibe: nada.
# Devuelve: la opción escrita por el usuario, como texto.
# Estructuras y temas: cadenas (.center() y repetición con *).
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

# Qué hace: muestra qué se puede hacer con una venta ya encontrada (cancelarla, cambiar el
#   asiento o volver) y pide una opción.
# Recibe: nada.
# Devuelve: la opción escrita, como texto y sin espacios (.strip()), porque GestionarVenta
#   la compara directamente con "1", "2" y "3".
# Estructuras y temas: cadenas (.center(), .strip() y repetición con *).
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

# Qué hace: muestra el menú de Informes (recaudación por destino, por mes y total) y pide
#   una opción.
# Recibe: nada.
# Devuelve: la opción escrita por el usuario, como texto.
# Estructuras y temas: cadenas (.center() y repetición con *).
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

# Qué hace: muestra el menú de Viajes (consultar disponibilidad, registrar un viaje o ver
#   los viajes) y pide una opción.
# Recibe: nada.
# Devuelve: la opción escrita por el usuario, como texto.
# Estructuras y temas: cadenas (.center() y repetición con *).
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

# Qué hace: muestra el menú de Micros (ver, registrar o dar de baja) y pide una opción.
# Recibe: nada.
# Devuelve: la opción escrita por el usuario, como texto.
# Estructuras y temas: cadenas (.center() y repetición con *).
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

# Qué hace: muestra el menú de Terminales (ver, agregar o eliminar) y pide una opción.
# Recibe: nada.
# Devuelve: la opción escrita por el usuario, como texto.
# Estructuras y temas: cadenas (.center() y repetición con *).
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

# Qué hace: vende un pasaje. Es la opción "Registrar venta de pasaje" del menú Ventas.
# Recibe: nada (todo se pide por teclado).
# Devuelve: nada. Agrega la venta a la lista "ventas" y marca el asiento en la matriz.
# Cómo funciona, paso a paso:
#   1. Si no hay viajes cargados, avisa y termina.
#   2. Arma la lista "destinos" solo con los destinos que tienen al menos un viaje, sin
#      repetir (usando "not in"). Así nunca se ofrece un destino sin viajes.
#   3. Muestra los destinos numerados, con 0 para volver, y pide uno. Controla que sea un
#      número (try/except ValueError) y que esté en rango. Si elige 0, la variable "volver"
#      hace que la función termine.
#   4. Arma "viajes_destino" con los viajes a ese destino, los muestra y el usuario elige
#      uno con ElegirDeLista().
#   5. Toma la matriz de asientos del viaje. Si está completo (ocupados == FILAS * COLUMNAS)
#      avisa y termina.
#   6. Muestra el mapa de asientos y el usuario elige uno con ElegirAsiento(), que ya lo
#      marca como ocupado ("X").
#   7. Calcula el precio: distancia entre salida y destino multiplicada por TARIFAPORKM.
#   8. Pide el DNI. Si ese DNI ya compró antes (BuscarVentasPorDni, que es recursiva), usa
#      el mismo nombre. Si es nuevo, pide el nombre con IngresarNombre().
#   9. Muestra el resumen y pide confirmación. Si responde N, libera el asiento y termina
#      sin guardar nada.
#   10. Si confirma, arma el diccionario "venta", lo agrega a "ventas" y guarda el archivo.
# Estructuras y temas: listas, diccionarios, matriz de asientos, excepciones, cadenas
#   (f-strings, .upper(), .center()) y búsqueda recursiva.
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

# Qué hace: muestra todas las ventas de un viaje que elige el usuario.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: muestra la lista de viajes con VerViajes() y pide el ID de uno. Si no es
#   un número, avisa y termina. Busca el viaje con BuscarViajePorId() (recursiva); si no
#   existe, avisa. Después recorre la lista "ventas" y muestra con MostrarVenta() las que
#   tienen ese "viaje_id", contándolas con la variable "cantidad". Al final muestra el total
#   o avisa que el viaje no tiene ventas.
# Estructuras y temas: listas, diccionarios, excepciones (ValueError) y recursividad.
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

# Qué hace: muestra por pantalla todos los datos de una venta.
# Recibe: venta, que es un diccionario de la lista "ventas".
# Devuelve: nada.
# Cómo funciona: imprime cada campo con f-strings. El precio se muestra con puntos de miles
#   usando FormatoPrecio(). El DNI se lee con .get('dni', '-'), que muestra un guión si la
#   venta no tuviera DNI en lugar de dar error.
# Estructuras y temas: diccionarios y cadenas (f-strings).
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

# Qué hace: cancela una venta: libera el asiento y la borra de la lista "ventas".
# Recibe: venta (el diccionario de la venta) y matriz (la matriz de asientos de su viaje).
# Devuelve: nada.
# Cómo funciona: primero pide confirmación con Confirmar(); si responde N, no hace nada.
#   Si confirma, vuelve a poner el asiento en "O" con LiberarAsiento(), saca la venta de la
#   lista con .remove() y guarda el archivo. Como las listas y los diccionarios son mutables,
#   el cambio en la matriz queda hecho en el viaje sin necesidad de devolverla.
# Estructuras y temas: listas, diccionarios y matriz.
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

# Qué hace: es la búsqueda 1, "Por viaje y asiento". El usuario elige un viaje y un asiento
#   y la función busca la venta de ese asiento.
# Recibe: nada.
# Devuelve: el diccionario de la venta encontrada, o None si no hay viajes, si el ID no es
#   válido o si ese asiento no tiene venta. main.py llama a GestionarVenta() solo si no es
#   None.
# Cómo funciona: muestra los viajes, pide el ID y busca el viaje con BuscarViajePorId().
#   Muestra su mapa de asientos, pide el asiento (con .upper() y .strip(), así "3b " sirve
#   igual que "3B") y busca la venta con BuscarVentaPorAsiento(). Las dos búsquedas son
#   recursivas.
# Estructuras y temas: listas, diccionarios, excepciones, cadenas y recursividad.
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

# Qué hace: es la búsqueda 2, "Por DNI". Busca todas las ventas de un DNI y deja elegir una.
# Recibe: nada.
# Devuelve: el diccionario de la venta elegida, o None si no hay ventas con ese DNI o si
#   el usuario elige volver.
# Cómo funciona: pide el DNI con IngresarDni(), que ya lo valida. BuscarVentasPorDni()
#   (recursiva) devuelve una lista con todas las coincidencias. Si está vacía avisa; si no,
#   ElegirVentaDeLista() muestra las ventas y devuelve la que se elija.
# Estructuras y temas: listas, diccionarios y recursividad.
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

# Qué hace: es la búsqueda 3, "Por nombre". Busca las ventas cuyo pasajero tenga en el
#   nombre el texto que escriba el usuario, y deja elegir una.
# Recibe: nada.
# Devuelve: el diccionario de la venta elegida, o None si no hay coincidencias o si el
#   usuario elige volver.
# Cómo funciona: pide un texto y no acepta que esté vacío (ciclo while). La búsqueda
#   encuentra coincidencias parciales y sin importar mayúsculas: "per" encuentra a
#   "Juan Perez". BuscarVentasPorNombre() (recursiva) devuelve la lista de coincidencias y
#   ElegirVentaDeLista() deja elegir una.
# Estructuras y temas: listas, diccionarios, cadenas y recursividad.
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

# Qué hace: cuando una búsqueda encuentra ventas, deja elegir una de ellas.
# Recibe: lista, una lista de ventas (diccionarios) que devolvió una búsqueda.
# Devuelve: el diccionario de la venta elegida, o None si el usuario elige 0 (volver).
# Cómo funciona: si hay una sola venta, la devuelve directamente sin preguntar. Si hay
#   varias, las muestra numeradas (armando cada renglón con += ) y pide un número entre 0 y
#   la cantidad. Controla que sea un número (try/except) y que esté en rango. La variable
#   "elegida" empieza en None y se sale del ciclo con break, para que el return quede fuera
#   del ciclo como pide la materia.
# Estructuras y temas: listas, diccionarios, excepciones y cadenas.
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

# Qué hace: después de encontrar una venta, permite cancelarla o cambiarle el asiento.
# Recibe: venta, el diccionario de la venta encontrada.
# Devuelve: nada.
# Cómo funciona: busca el viaje de la venta con BuscarViajePorId() para obtener su matriz
#   de asientos. Muestra la venta y el menú de gestión, y lo repite hasta que la opción sea
#   "1", "2" o "3". Con 1 llama a CancelarVenta(), con 2 a CambiarAsiento(), y con 3 no hace
#   nada y vuelve al menú de búsqueda.
# Estructuras y temas: diccionarios, matriz y recursividad.
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

# Qué hace: busca en la lista "viajes" el viaje que tiene un ID determinado, en forma
#   recursiva.
# Recibe: viaje_id (número entero). "inicio" y "fin" marcan el pedazo de la lista donde se
#   busca. Desde afuera se llama solo con el ID: inicio vale 0 por omisión y fin empieza en
#   None, y en la primera llamada se completa con len(viajes).
# Devuelve: el diccionario del viaje, o None si no existe.
# Cómo funciona ("divide y vencerás", Clase 10):
#   - Caso base 1: el pedazo está vacío (fin - inicio == 0), entonces devuelve None.
#   - Caso base 2: el pedazo tiene un solo viaje. Si es el del ID buscado lo devuelve; si
#     no, devuelve None.
#   - Caso recursivo: parte el pedazo a la mitad (medio = (inicio + fin) // 2), busca en la
#     mitad izquierda y, si no lo encontró, busca en la mitad derecha.
#   Como cada vez parte a la mitad, la cantidad de llamadas encadenadas es muy chica (con
#   1000 viajes son unos 10 niveles), así nunca se llega al RecursionError.
# Estructuras y temas: recursividad, listas, diccionarios y parámetros con valor por omisión.
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

# Qué hace: busca en la lista "ventas" la venta de un viaje y un asiento determinados, en
#   forma recursiva. La usa la búsqueda 1 ("Por viaje y asiento").
# Recibe: viaje_id (número del viaje) y asiento (texto, por ejemplo "3B"). "inicio" y "fin"
#   funcionan igual que en BuscarViajePorId().
# Devuelve: el diccionario de la venta, o None si ese asiento no tiene venta.
# Cómo funciona: igual que BuscarViajePorId(). Los casos base son el pedazo vacío o de un
#   solo elemento, donde se compara que coincidan el viaje_id y el asiento. El caso recursivo
#   parte la lista a la mitad y busca primero en la izquierda y después en la derecha.
# Estructuras y temas: recursividad, listas y diccionarios.
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

# Qué hace: busca todas las ventas de un DNI, en forma recursiva.
# Recibe: dni (texto). "inicio" y "fin" marcan el pedazo de la lista. "encontrados" es la
#   lista donde se van juntando los resultados entre una llamada y otra.
# Devuelve: una lista con todas las ventas de ese DNI (vacía si no hay ninguna).
# Cómo funciona: los casos base son el pedazo vacío o de un solo elemento (si el DNI
#   coincide, se agrega a "encontrados"). En el caso recursivo busca en las dos mitades, sin
#   frenar en la primera coincidencia, porque una persona puede tener varios pasajes.
#   "encontrados" empieza en None y se crea la lista en la primera llamada. Si fuera
#   encontrados=[] en el def, Python usaría la misma lista en todas las búsquedas y se
#   mezclarían los resultados de una búsqueda con los de la anterior.
# Estructuras y temas: recursividad, listas, diccionarios y parámetros con valor por omisión.
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

# Qué hace: busca todas las ventas cuyo nombre de pasajero contenga un texto, en forma
#   recursiva.
# Recibe: texto (lo que escribió el usuario). "inicio", "fin" y "encontrados" funcionan
#   igual que en BuscarVentasPorDni().
# Devuelve: una lista con las ventas que coinciden (vacía si no hay ninguna).
# Cómo funciona: igual que BuscarVentasPorDni(), pero la comparación pasa el texto y el
#   nombre a minúsculas con .lower() y usa "in" para ver si el texto está dentro del nombre.
#   Así "per" o "PEREZ" encuentran a "Juan Perez".
# Estructuras y temas: recursividad, listas, diccionarios y cadenas.
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

# Qué hace: cuenta cuántos asientos ocupados tiene un viaje.
# Recibe: asientos, la matriz de 10 filas x 4 columnas del viaje.
# Devuelve: la cantidad de asientos ocupados (número entero).
# Cómo funciona: recorre la matriz fila por fila y, dentro de cada fila, asiento por
#   asiento, sumando 1 en "ocupados" cada vez que encuentra una "X". Se usa para saber si un
#   viaje está completo, para mostrar los lugares libres y para calcular la recaudación.
# Estructuras y temas: matrices (recorrido sin subíndices, Clase 04).
def ContarAsientosOcupados(asientos):
    ocupados = 0

    for fila in asientos:
        for asiento in fila:
            if asiento == "X":
                ocupados += 1

    return ocupados

# Qué hace: muestra el mapa de asientos de un viaje.
# Recibe: matriz, la matriz de asientos del viaje.
# Devuelve: nada.
# Cómo funciona: imprime el encabezado con las columnas A B, el pasillo y C D. Después
#   imprime cada fila con su número alineado a la derecha ({f+1:>2}) y los cuatro asientos,
#   "O" si está libre y "X" si está ocupado. Al final muestra la referencia de los símbolos.
# Estructuras y temas: matrices y cadenas (f-strings con ancho y alineación).
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

# Qué hace: pide un asiento, controla que sea válido y que esté libre, y lo marca como
#   ocupado.
# Recibe: matriz, la matriz de asientos del viaje.
# Devuelve: el asiento elegido como texto y normalizado (por ejemplo "3B"; si se escribe
#   "03b" devuelve "3B").
# Cómo funciona: el asiento se escribe como número de fila más letra. Con rebanadas se
#   separan las dos partes: asiento[:-1] es la fila y asiento[-1] es la letra. La fila se
#   pasa a número y la letra a columna (A=0, B=1, C=2, D=3) con if/elif. Se controla que la
#   fila esté entre 1 y FILAS, que la letra sea A, B, C o D y que el asiento no tenga "X".
#   Si se escribe algo sin formato (por ejemplo "A" o nada), el except (ValueError,
#   IndexError) muestra el error. Cuando el asiento es válido, se pone "X" en la matriz.
#   Ojo: el asiento queda ocupado apenas se elige. Si después la venta no se confirma,
#   RegistrarVenta() lo libera con LiberarAsiento().
# Estructuras y temas: matrices, cadenas (rebanadas, .upper(), .strip()) y excepciones.
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

# Qué hace: deja libre un asiento de la matriz (vuelve a ponerle "O").
# Recibe: matriz (la matriz de asientos del viaje) y asiento (texto, por ejemplo "3B").
# Devuelve: nada. Modifica la matriz que recibe.
# Cómo funciona: separa la fila y la letra con rebanadas igual que ElegirAsiento(), pasa la
#   letra a número de columna y pone "O" en esa posición. No valida el asiento porque solo
#   se la llama con asientos que salen de ventas que ya existen.
# Estructuras y temas: matrices y cadenas (rebanadas).
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

# Qué hace: le cambia el asiento a una venta.
# Recibe: venta (el diccionario de la venta) y matriz (la matriz de asientos de su viaje).
# Devuelve: nada.
# Cómo funciona: libera el asiento actual con LiberarAsiento(), muestra el mapa (donde el
#   asiento anterior ya aparece libre y se puede volver a elegir), pide el nuevo con
#   ElegirAsiento(), lo guarda en venta["asiento"] y graba el archivo.
# Estructuras y temas: diccionarios y matrices.
def CambiarAsiento(venta, matriz):
    asiento_anterior = venta["asiento"]

    LiberarAsiento(matriz, asiento_anterior)

    print("Seleccione el nuevo asiento:")
    ImprimirMatriz(matriz)

    nuevo_asiento = ElegirAsiento(matriz)

    venta["asiento"] = nuevo_asiento

    GuardarDatos()

    print("Asiento modificado correctamente.")

# Qué hace: crea la matriz de asientos vacía de un viaje nuevo.
# Recibe: nada.
# Devuelve: una matriz (lista de listas) de FILAS x COLUMNAS, es decir 10 x 4, con todos
#   los asientos en "O" (libres).
# Cómo funciona: por cada fila agrega a la matriz una lista de COLUMNAS elementos "O",
#   creada con la repetición ["O"] * COLUMNAS. Es la "Alternativa 3" de la Clase 04.
# Estructuras y temas: matrices y listas.
def CrearMatriz():
    matriz = []

    for f in range(FILAS):
        matriz.append(["O"] * COLUMNAS)

    return matriz

############################## Informes ##############################

# Qué hace: muestra cuánto se recaudó con los viajes a cada destino.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: recorre todos los viajes y va sumando la recaudación de cada uno
#   (CalcularRecaudacionViaje) en el diccionario "recaudacion_por_destino", cuya clave es el
#   destino. Si el destino ya está en el diccionario se le suma; si no, se crea. Al final
#   muestra los destinos ordenados alfabéticamente con sorted(), alineados con {destino:<15}
#   y con el precio formateado con FormatoPrecio().
# Estructuras y temas: diccionarios, listas y cadenas (f-strings con alineación).
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

# Qué hace: muestra cuánto se recaudó en cada mes, en orden cronológico.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: la lista "meses" sirve para mostrar el nombre del mes (meses[mes - 1]).
#   Para cada viaje, separa la fecha con .split("/") y arma la clave (año, mes), que es una
#   tupla. Se usa una tupla porque las claves de un diccionario tienen que ser inmutables, y
#   porque al ordenarlas se compara primero el año y después el mes: así sorted() deja
#   Diciembre 2026 antes que Enero 2027. La clave se desempaqueta con "anio, mes = clave".
#   La recaudación se va acumulando igual que en el informe por destino.
# Estructuras y temas: tuplas, diccionarios, listas y cadenas (.split(), f-strings).
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

# Qué hace: muestra cuánto se recaudó en total, sumando todos los viajes.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: suma en "recaudacion_total" (con +=) la recaudación de cada viaje,
#   calculada con CalcularRecaudacionViaje(), y la muestra con FormatoPrecio(). Si no hay
#   viajes muestra $0.
# Estructuras y temas: listas y diccionarios.
def MostrarRecaudacionTotal():
    recaudacion_total = 0

    for viaje in viajes:
        recaudacion_total += CalcularRecaudacionViaje(viaje)

    print("=" * 50)
    print("RECAUDACIÓN TOTAL".center(50))
    print("=" * 50)
    print(f"Recaudación total: ${FormatoPrecio(recaudacion_total)}")
    print("-" * 50)

# Qué hace: calcula cuánto dinero se recaudó con un viaje.
# Recibe: viaje, un diccionario de la lista "viajes".
# Devuelve: la recaudación del viaje (número entero).
# Cómo funciona: multiplica la cantidad de asientos ocupados (ContarAsientosOcupados) por
#   los km entre la salida y el destino y por TARIFAPORKM. Da lo mismo que sumar el precio de
#   cada venta del viaje, porque todas tienen ese mismo precio.
# Estructuras y temas: diccionarios y matrices.
def CalcularRecaudacionViaje(viaje):
    asientos_ocupados = ContarAsientosOcupados(viaje["asientos"])
    kilometros = distancias[viaje["salida"]][viaje["destino"]]

    return asientos_ocupados * kilometros * TARIFAPORKM

############################## Viajes ################################

# Qué hace: muestra una tabla con todos los viajes y sus lugares libres, y después el mapa
#   de asientos del viaje que elija el usuario.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: para que la tabla quede alineada, primero calcula el ancho de cada columna
#   según el texto más largo (con max() y len()). Después arma el encabezado y cada fila por
#   partes con +=, usando .rjust() y .ljust() para alinear, y f-strings con ancho. Los
#   lugares libres son FILAS * COLUMNAS menos los ocupados. Al final el usuario elige un
#   viaje con ElegirDeLista() y se muestran sus datos y su mapa con ImprimirMatriz().
# Estructuras y temas: listas, diccionarios, matrices y cadenas (.rjust(), .ljust(),
#   f-strings).
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

# Qué hace: registra un viaje nuevo. Es la opción "Registrar viaje" del menú Viajes.
# Recibe: nada (todo se pide por teclado).
# Devuelve: nada. Agrega el viaje a la lista "viajes".
# Cómo funciona, paso a paso:
#   1. Controla que haya al menos 2 terminales y al menos 1 micro.
#   2. Calcula el ID nuevo: 1 si no hay viajes, o el ID del último viaje + 1. Funciona
#      porque los viajes siempre se agregan al final, así el último tiene el ID más alto.
#   3. Elige la salida con ElegirTerminal() y el destino con ElegirDestino(), que no
#      muestra la terminal de salida.
#   4. Muestra los micros numerados y se elige uno con ElegirDeLista().
#   5. Pide la fecha con IngresarFecha() y controla que ese micro no tenga otro viaje ese
#      mismo día (variable "ocupado", con un for y break). Si lo tiene, pide otra fecha.
#   6. Crea la matriz de asientos vacía con CrearMatriz().
#   7. La línea comentada llama a GenerarVentasAlAzar(), que llena el viaje con pasajeros
#      de prueba. Está comentada para que los viajes nuevos arranquen sin ventas; para
#      volver a usarla hay que sacarle el #.
#   8. Guarda en el diccionario "viaje" el id, la salida, el destino, la patente, la fecha
#      y los asientos, lo agrega a "viajes" y graba el archivo.
# Estructuras y temas: diccionarios, listas y matrices.
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

# Qué hace: llena un viaje con pasajeros al azar, para tener datos de prueba.
# Recibe: los datos del viaje: salida, destino, fecha, matriz (sus asientos), patente y
#   viaje_id.
# Devuelve: la matriz, con los asientos ocupados marcados con "X". También agrega una venta
#   a la lista "ventas" por cada asiento ocupado.
# Cómo funciona: recorre la matriz asiento por asiento. random.randint(0, 1) decide si el
#   asiento se ocupa (la mitad de las veces). Si se ocupa, se pone "X", se arma el nombre
#   del asiento (fila + letra, por ejemplo "3B"), se elige un nombre y un apellido al azar
#   de las listas "nombres" y "apellidos", se genera un DNI al azar de 8 números y se crea
#   la venta con el precio del viaje. Hoy no se usa porque su llamada en RegistrarViaje()
#   está comentada; se usó para cargar los viajes de prueba.
# Estructuras y temas: matrices, listas, diccionarios y números al azar (módulo random).
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

# Qué hace: muestra todos los viajes programados con su ID, salida, destino, fecha y
#   patente.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: recorre la lista "viajes" y muestra los datos de cada uno. También la usan
#   VerVentas() y SeleccionarVentaPorAsiento(), para que el usuario vea los IDs antes de
#   elegir uno.
# Estructuras y temas: listas, diccionarios y cadenas (f-strings).
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

# Qué hace: muestra todos los micros con los destinos a los que tienen viajes.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: por cada micro recorre los viajes y arma la lista "destinos_micro" con los
#   destinos de los viajes de ese micro, sin repetir (usando "not in"). Si no tiene viajes,
#   muestra "Sin viajes asignados".
# Estructuras y temas: listas y diccionarios.
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

# Qué hace: registra un micro nuevo a partir de su patente.
# Recibe: nada.
# Devuelve: nada. Agrega el micro a "micros" y su patente a "patentes".
# Cómo funciona: pide la patente y la pasa a mayúsculas con .upper(). La valida con la
#   expresión regular ^[A-Z][A-Z][0-9][0-9][0-9][A-Z][A-Z]$, que pide 2 letras, 3 números y
#   2 letras (por ejemplo AB123CD). También controla que no esté en el conjunto "patentes":
#   se usa un conjunto porque no admite repetidos y es rápido para ver si un dato está.
#   Mientras la patente no sea válida o esté repetida, la vuelve a pedir.
# Estructuras y temas: expresiones regulares, conjuntos, listas, diccionarios y cadenas.
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

# Qué hace: da de baja un micro y borra también sus viajes y las ventas de esos viajes.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: muestra los micros numerados, se elige uno con ElegirDeLista() y se pide
#   confirmación con Confirmar(). Si confirma, saca el micro de la lista con .remove() y su
#   patente del conjunto con .discard(). Después arma con listas por comprensión los viajes
#   y las ventas que NO son de ese micro, y los copia a las listas originales con .clear() y
#   .extend(). No se hace "viajes = viajes_nuevos" porque, dentro de una función, eso crearía
#   una variable local nueva y la lista original no cambiaría.
# Estructuras y temas: listas (listas por comprensión), conjuntos y diccionarios.
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

# Qué hace: muestra todas las terminales con la distancia a cada una de las demás.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: "distancias" es un diccionario de diccionarios: la clave de afuera es una
#   terminal y su valor es otro diccionario con los km a cada una de las otras. Por ejemplo,
#   distancias["Buenos Aires"]["Rosario"] vale 300. La función recorre las terminales
#   numerándolas con enumerate() y, para cada una, recorre su diccionario interno.
# Estructuras y temas: diccionarios (anidados) y cadenas (f-strings).
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

# Qué hace: agrega una terminal nueva y pide la distancia a cada una de las que ya existen.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: pide el nombre y lo limpia: " ".join(terminal.split()) junta los espacios
#   de más y .title() pone la primera letra de cada palabra en mayúscula (así "  san   luis"
#   queda "San Luis"). Lo valida con una expresión regular que solo acepta letras (con
#   tildes, ñ y ü) y espacios, y controla que la terminal no exista ("in" sobre las claves
#   del diccionario). Después pide con IngresarKm() la distancia a cada terminal existente y
#   la guarda en el diccionario "kms". Finalmente agrega la terminal a "distancias" y, en
#   cada una de las otras, agrega la distancia hacia la nueva: cada distancia queda guardada
#   en los dos sentidos para poder consultarla desde cualquiera de las dos terminales.
# Estructuras y temas: diccionarios, cadenas (.split(), .join(), .title()) y expresiones
#   regulares.
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

# Qué hace: pide la distancia en km entre dos terminales, hasta que se escriba un número
#   válido.
# Recibe: terminal y otra, los nombres de las dos terminales (para mostrarlos en la
#   pregunta).
# Devuelve: la distancia, como número entero mayor que cero.
# Cómo funciona: repite la pregunta con un while True. Si lo escrito no es un número, el
#   except ValueError muestra el error; si es cero o negativo, el continue vuelve a
#   preguntar. Cuando el número es válido, el break sale del ciclo y el return devuelve el
#   valor (el return queda fuera del ciclo, como pide la materia).
# Estructuras y temas: excepciones (ValueError).
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

# Qué hace: elimina una terminal y borra también los viajes y las ventas que salían o
#   llegaban a ella.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: se elige la terminal con ElegirTerminal() y se pide confirmación. Si
#   confirma, la saca de "distancias" con .pop() y también del diccionario interno de cada
#   una de las otras terminales. Después, con listas por comprensión, se quedan solo los
#   viajes y ventas que no salen ni llegan a esa terminal, y se copian a las listas
#   originales con .clear() y .extend() (por el mismo motivo que en DarBajaMicro).
# Estructuras y temas: diccionarios (anidados) y listas (listas por comprensión).
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

# Qué hace: muestra las terminales numeradas y deja elegir una.
# Recibe: nada.
# Devuelve: el nombre de la terminal elegida (texto).
# Cómo funciona: arma una lista con las claves de "distancias" (list(distancias.keys())),
#   la muestra numerada con enumerate() y usa ElegirDeLista() para que se elija una.
# Estructuras y temas: diccionarios y listas.
def ElegirTerminal():
    terminales = list(distancias.keys())

    print("\n" + "=" * 50)
    print("TERMINALES".center(50))
    print("=" * 50)

    for i, terminal in enumerate(terminales):
        print(f"{i + 1} - {terminal}")

    return ElegirDeLista(terminales, "Seleccione la terminal: ")

# Qué hace: muestra los destinos posibles desde una terminal de salida y deja elegir uno.
# Recibe: salida, el nombre de la terminal de salida.
# Devuelve: el nombre del destino elegido (texto).
# Cómo funciona: arma la lista "destinos" con todas las terminales menos la de salida,
#   porque no se puede viajar a la misma terminal. Los muestra numerados con la distancia
#   entre paréntesis, por ejemplo "2 - Rosario (300 km)", y usa ElegirDeLista().
# Estructuras y temas: diccionarios, listas y cadenas.
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

# Qué hace: función general para elegir un elemento de cualquier lista escribiendo su
#   número. La usan las pantallas que eligen terminales, destinos, micros y viajes.
# Recibe: lista (la lista de donde se elige) y mensaje (el texto de la pregunta).
# Devuelve: el elemento elegido de la lista, no el número que se escribió.
# Cómo funciona: repite la pregunta hasta que se escriba un número entre 1 y la cantidad de
#   elementos. Si no es un número, el except ValueError muestra el error; si está fuera de
#   rango, el continue vuelve a preguntar. Sale del ciclo con break y el return queda fuera
#   del ciclo. Como la lista se muestra empezando en 1, devuelve lista[opcion - 1].
# Estructuras y temas: listas y excepciones (ValueError).
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

# Qué hace: pide el DNI de un pasajero hasta que sea válido.
# Recibe: nada.
# Devuelve: el DNI, como texto.
# Cómo funciona: lo valida con la expresión regular ^[0-9]...[0-9]?$: siete [0-9]
#   obligatorios y un octavo con "?", que significa "0 o 1 vez". Así acepta DNI de 7 u 8
#   números, sin puntos ni espacios. Se guarda como texto porque no se hacen cuentas con él.
# Estructuras y temas: expresiones regulares y cadenas.
def IngresarDni():
    dni = input("Ingrese el DNI del pasajero (sin puntos): ").strip()

    while not re.search(r"^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]?$", dni):
        print("Error: el DNI debe tener 7 u 8 números, sin puntos ni espacios.")
        dni = input("Ingrese el DNI del pasajero (sin puntos): ").strip()

    return dni

# Qué hace: pide el nombre completo de un pasajero hasta que sea válido.
# Recibe: nada.
# Devuelve: el nombre limpio y con mayúscula inicial en cada palabra (por ejemplo,
#   "  juan   perez " queda "Juan Perez").
# Cómo funciona: limpia los espacios con " ".join(nombre.split()) y aplica .title(). Lo
#   valida con una expresión regular que solo acepta letras (incluye tildes, ñ y ü) y
#   espacios, y con len(nombre.split()) controla que tenga al menos dos palabras (nombre y
#   apellido). Si no cumple, muestra el error y vuelve a preguntar.
# Estructuras y temas: cadenas (.split(), .join(), .title()) y expresiones regulares.
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

# Qué hace: devuelve un número con puntos de miles, para mostrar precios. Por ejemplo,
#   1234567 queda "1.234.567". Es una función recursiva.
# Recibe: numero, un número entero.
# Devuelve: el número con los puntos, como texto.
# Cómo funciona:
#   - Caso base: si el número es menor que 1000 no lleva puntos, entonces se devuelve tal
#     cual con str().
#   - Caso recursivo: se formatea la parte de los miles (numero // 1000) llamando a la misma
#     función, y se le agrega un punto y los últimos 3 números (numero % 1000). El :03 del
#     f-string completa con ceros adelante, así 1005 queda "1.005" y no "1.5".
#   Ejemplo: FormatoPrecio(1234567) = FormatoPrecio(1234) + ".567"
#                                   = FormatoPrecio(1) + ".234" + ".567" = "1.234.567"
# Estructuras y temas: recursividad y cadenas (f-strings con relleno de ceros).
def FormatoPrecio(numero):
    if numero < 1000:
        return str(numero)
    else:
        return FormatoPrecio(numero // 1000) + "." + f"{numero % 1000:03}"

# Qué hace: hace una pregunta de sí o no (S/N) y devuelve la respuesta. Se usa antes de dar
#   de baja un micro, eliminar una terminal, confirmar una venta y cancelar una venta.
# Recibe: mensaje, el texto de la pregunta. La función le agrega " (S/N): " al final.
# Devuelve: True si se respondió S, o False si se respondió N.
# Cómo funciona: aplica .strip() y .upper() a la respuesta, así "s" o " n " también sirven.
#   Mientras no sea S ni N, muestra el error y vuelve a preguntar. Al final devuelve el
#   resultado de la comparación respuesta == "S", que es True o False.
# Estructuras y temas: cadenas (.strip(), .upper()) y valores booleanos.
def Confirmar(mensaje):
    respuesta = input(mensaje + " (S/N): ").strip().upper()

    while respuesta != "S" and respuesta != "N":
        print("Error: responda S o N.")
        respuesta = input(mensaje + " (S/N): ").strip().upper()

    return respuesta == "S"

# Qué hace: pide la fecha de un viaje y la controla hasta que sea válida.
# Recibe: nada.
# Devuelve: la fecha como texto, en formato "DD/MM/AAAA" (así se guarda en el archivo).
# Cómo funciona: controla la fecha en pasos y, si alguno falla, muestra el error y la
#   vuelve a pedir:
#   1. Que tenga tres partes separadas por "/" (con .split("/")).
#   2. Que el día y el mes tengan 2 números y el año 4.
#   3. Que las tres partes sean números (try/except ValueError).
#   4. Que el mes esté entre 1 y 12.
#   5. Que el día exista en ese mes. El diccionario "dias_por_mes" tiene los días de cada
#      mes, y febrero pasa a 29 si el año es bisiesto (divisible por 4 y no por 100, o
#      divisible por 400).
#   6. Que la fecha esté entre hoy y un año desde hoy. La fecha de hoy se obtiene con
#      time.localtime(). Las fechas se comparan como tuplas (año, mes, día), que se comparan
#      elemento a elemento: primero el año, después el mes y después el día.
# Estructuras y temas: cadenas (.split(), .strip()), diccionarios, tuplas y excepciones.
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
