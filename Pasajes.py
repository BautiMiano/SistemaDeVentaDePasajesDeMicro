from Asientos import CrearMatriz
import re
import time
##################################################
micros = [
    {"patente": "AF617ES", "destinos": ["Mar del Plata", "Pinamar"]},
    {"patente": "AG817ES", "destinos": ["Villa Gesell"]},
    {"patente": "AC427ES", "destinos": ["Cobos"]},
    {"patente": "AA852ES", "destinos": ["San Bernando"]},
    {"patente": "AB951ES", "destinos": ["Mar del Plata", "San Bernando"]}
]
ventas = []

tarifaPorKm = 100

distancias = {
    "Mar del Plata": 400,
    "Pinamar": 350,
    "Villa Gesell": 370,
    "San Bernardo": 350,
    "Cobos": 1000
}

patentes = {
    "AF617ES",
    "AG817ES",
    "AC427ES",
    "AA852ES",
    "AB951ES",
}

###############################
viajes = []

viajes_programados = [
    {
        "destino": "Mar del Plata",
        "fecha": "30/10/2026",
        "patente": "AF617ES",
        "precio": tarifaPorKm * distancias["Mar del Plata"],
        "estado": "programado",
    },
    {
        "destino": "Mar del Plata",
        "fecha": "05/11/2026",
        "patente": "AG817ES",
        "precio": tarifaPorKm * distancias["Mar del Plata"],
        "estado": "programado",
    }
]

for precarga in viajes_programados:
    id_viaje_automatico = len(viajes) + 1
    viaje = {
        "id": id_viaje_automatico,
        "salida": "Buenos Aires",
        "destino": precarga["destino"],
        "fecha": precarga["fecha"],
        "patente": precarga["patente"],
        "precio": precarga["precio"],
        "estado": precarga["estado"],
        "asientos": CrearMatriz()
    }
    viajes.append(viaje)

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

def VerDestinos():
    print("Destinos Diposnible:")
    for numero, (destino, distancia) in enumerate(distancias.items(), start = 1):
        print(f"{numero}. {destino} - {distancia} km")

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
    return destinos_agregados

def MicrosPorDestinos(destino):
    micros_disponibles = []
    for micro in micros:
        if destino in micro["destinos"]:
            micros_disponibles.append(micro)

    if not micros_disponibles:
        print("No hay micros para ese destino")
        return []
    return micros_disponibles
############################## Micros ##################################

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

    micro_destinos = Seleccionar_Destinos()

    micro = {
        "patente" : patente,
        "destinos" : micro_destinos
    }
    micros.append(micro)
    patentes.add(patente)
    print("Micro registrado correctamente")

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
    
def VerMicros():
    if not micros:
        print("No hay micros registrados")
        return
    print("=" * 50)
    print("MICROS REGISTRADOS".center(50))
    print("=" * 50)
    for micro in micros:
        print(f"Patente: {micro['patente']}")
        print("Destinos disponibles:")
        for destino in micro["destinos"]:
            print(f"- {destino}")
        print("-"*30)
    
############################## Viajes ##################################

def RegistrarViaje():
    print("Destinos disponibles")
    for numero, (destino, distancia) in enumerate(distancias.items(), start = 1):
        print(f"{numero}. {destino} - {distancia} km")
    Sel_destino = input("Seleccione el destino (ingrese el número): ")
    while not Sel_destino.isdigit() or int(Sel_destino) < 1 or int(Sel_destino) > len(distancias):
        print("Error: opción inválida.")
        Sel_destino = input("Seleccione el destino (ingrese el número): ")
    destino = list(distancias.keys())[int(Sel_destino) - 1]
    micros_disponibles = MicrosPorDestinos(destino)
    if not micros_disponibles:
        return
    for numero, micro in enumerate(micros_disponibles, start = 1):
        print(f"{numero}. {micro['patente']}")
    Sel_micro = input("Seleccione el micro (ingrese el número): ")
    while not Sel_micro.isdigit() or int(Sel_micro) < 1 or int(Sel_micro) > len(micros_disponibles):
        print("Error: opción inválida.")
        Sel_micro = input("Seleccione el micro (ingrese el número): ")
    patente = micros_disponibles[int(Sel_micro) - 1]["patente"]        
    fecha = ValidarFechas()
    precio = tarifaPorKm * distancias[destino]
    estado = "programado"
    id_viaje_automatico = len(viajes) + 1
    viaje = {
            "id": id_viaje_automatico,
            "salida": "Buenos Aires",
            "destino": destino,
            "fecha": fecha,
            "patente": patente,
            "precio": precio,
            "estado": estado,
            "asientos": CrearMatriz()
        }
    viajes.append(viaje)

def VerViajes():
    print("=" * 50)
    print("VIAJES PROGRAMADOS".center(50))
    print("=" * 50)
    for viaje in viajes:
        print(f"ID: {viaje['id']}, Salida: {viaje['salida']}, Destino: {viaje['destino']}, Fecha: {viaje['fecha']}, Patente: {viaje['patente']}, Estado: {viaje['estado']}")
