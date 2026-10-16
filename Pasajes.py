from Asientos import asientos, CrearMatriz
import random
##################################################
micros = []
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

for patente in patentes:
    micro = {
        "patente" : patente
        
    }
    micros.append(micro)

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

#def GenerarFechaAleatoria():
#    mes = random.randint(1, 12)
#    anio = random.randint(2026, 2027)
#    dias_por_mes = {
#        1: 31, 2: 28, 3: 31, 4: 30,
#        5: 31, 6: 30, 7: 31, 8: 31,
#        9: 30, 10: 31, 11: 30, 12: 31
#    }    
#    
#    if anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0):
#        dias_por_mes[2] = 29
#
#    dia = random.randint(1, dias_por_mes[mes])    
#    fecha = f"{dia:02d}/{mes:02d}/{anio}"
#    return fecha

def ValidarFechas():
#    fecha_actual = GenerarFechaAleatoria()
#    print("="*50, "\n")
#    print(f"Fecha actual generada: {fecha_actual}")
#    print("\n", "="*50)
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
                    break

            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")            

        except ValueError:
            print("Error: ingrese día, mes y año con números.")
            fecha = input("Ingrese la fecha del viaje (DD/MM/AAAA): ")
    return fecha

############################## Micros ##################################

def RegistrarMicro():
    patente = input("Ingrese la patente del micro: ").upper().strip()
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
    print("Micro registrado correctamente")

def DarBajaMicro():
    patente = input("Ingrese la patente del micro: ").upper().strip()
    while patente == "":
        print("Error: la patente no puede estar vacía.")
        patente = input("Ingrese la patente del micro: ").strip().upper()
    while patente not in patentes:
        print("Error, la pantente no existe, por favor ingrese otra patente")
        patente = input("Ingrese la patente del micro: ").strip().upper()
    
    return
    
def VerMicros():
    print("=" * 50)
    print("MICROS REGISTRADOS".center(50))
    print("=" * 50)
    for micro in micros:
        print(f"Patente: {micro['patente']}")
    
############################## Viajes ##################################

def RegistrarViaje():
    fecha = ValidarFechas()
    print("Destinos disponibles")
    for numero, (destino, distancia) in enumerate(distancias.items(), start = 1):
        print(f"{numero}. {destino} - {distancia} km")
    Sel_destino = input("Seleccione el destino (ingrese el número): ")
    while not Sel_destino.isdigit() or int(Sel_destino) < 1 or int(Sel_destino) > len(distancias):
        print("Error: opción inválida.")
        Sel_destino = input("Seleccione el destino (ingrese el número): ")
    destino = list(distancias.keys())[int(Sel_destino) - 1]
    for numero, micro in enumerate(micros, start = 1):
        print(f"{numero}. {micro['patente']}")
    Sel_micro = input("Seleccione el micro (ingrese el número): ")
    while not Sel_micro.isdigit() or int(Sel_micro) < 1 or int(Sel_micro) > len(micros):
        print("Error: opción inválida.")
        Sel_micro = input("Seleccione el micro (ingrese el número): ")
    patente = micros[int(Sel_micro) - 1]["patente"]
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
