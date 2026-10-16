# from Asientos import asientos, ImprimirMatriz, RellenarMatriz, ElegirAsiento, matriz
# from Funciones.ReservaPasaje import AgregarReserva
# from Datos import km_destinos
# from Datos import reservas
# from Asientos import ModificarAsiento

# def AgregarReserva(reserva):
#     reservas.append(reserva)
#     return


# def VerReserva(usuarioActual):
#     print("=" * 66)
#     print("MIS RESERVAS".center(65))
#     print("=" * 66)

#     tieneReservas = False

#     for i in range(len(reservas)):
#         if reservas[i][0] == usuarioActual:
#             tieneReservas = True
#             break


#     if tieneReservas == False:
#         print("")
#         print("No hay reservas realizadas.".center(65))
#         print("")
#         return
        
#     print(f"{'N°':<5}{'DESTINO':<25}{'FECHA':<15}{'ASIENTO':>10}{'Precio':>10}")
#     print("-" * 66)

#     numReservas = 1

#     for i in range(len(reservas)):
#         if reservas[i][0] == usuarioActual:
#             destino = reservas[i][1]
#             fecha = reservas[i][2]
#             asiento = reservas[i][3]
#             precio = reservas[i][4]

#             print(f"{numReservas:<5}{destino:<25}{fecha:<15}{asiento:>10} {"$":>4}{precio}")
#             numReservas += 1



# def CancelarReserva(usuarioActual):
#     print("=" * 66)
#     print("CANCELAR RESERVA".center(66))
#     print("=" * 66)

#     tieneReservas = False

#     for i in range(len(reservas)):
#         if reservas[i][0] == usuarioActual:
#             tieneReservas = True
#             break

#     if tieneReservas == False:
#         print("")
#         print("No hay reservas para cancelar.".center(65))
#         print("")
#         return

#     print(f"{'N°':<5}{'DESTINO':<25}{'FECHA':<15}{'ASIENTO':>10}{'Precio':>10}")
#     print("-" * 65)


#     numeroReserva = 1

#     for i in range(len(reservas)):
#         if reservas[i][0] == usuarioActual:
#             destino = reservas[i][1]
#             fecha = reservas[i][2]
#             asiento = reservas[i][3]
#             precio = reservas[i][4]
#             print(f"{numeroReserva:<5}{destino:<25}{fecha:<15}{asiento:>10}{precio:>10}")
#             numeroReserva += 1




#     print("-" * 65)

#     opcion = input("Ingrese la reserva que queres cancelar: ")
#     while not opcion.isdigit() or int(opcion) < 1 or int(opcion) >= numeroReserva:
#         print("ERROR: Opcion invalida.")
#         opcion = input("Ingrese la reserva que queres cancelar: ")
#     opcion = int(opcion)

#     numeroReserva = 1

#     for i in range(len(reservas)):
#         if reservas[i][0] == usuarioActual:

#             if numeroReserva == opcion:

#                 reserva = reservas[i]

#                 asiento = reserva[3]

#                 precio = reserva[4]

#                 numero = int(asiento[:-1])
#                 letra = asiento[-1].upper() 

#                 ModificarAsiento(numero, letra)

#                 reservas.remove(reserva)

#                 print("")
#                 print("Reserva cancelada correctamente.".center(65))
#                 print("")

#             numeroReserva += 1


# def VentaPasajes(usuarioActual):
#     print("=" * 50)
#     print("COMPRA DE PASAJE".center(50))
#     print("=" * 50)
#     print("")

#     print("DESTINOS".center(50))
#     print("-" * 50)

#     for i in range(len(destinos)):
#         print(f"{i + 1:>2} - {destinos[i]}")

#     print("-" * 50)

#     opcion1 = input("Seleccione un destino: ")
#     while not opcion1.isdigit() or int(opcion1) < 1 or int(opcion1) > len(destinos):
#         print("ERROR: Opcion invalida. Por favor, seleccione un destino válido.")
#         opcion1 = input("Seleccione un destino: ")

#     print("")
#     print("FECHAS DISPONIBLES".center(50))
#     print("-" * 50)

#     for i in range(len(fechas)):
#             print(f"{i + 1:>2} - {fechas[i]}")

#     print("-" * 50)

#     opcion2 = input("Seleccione una fecha: ")

#     while not opcion2.isdigit() or int(opcion2) < 1 or  int (opcion2) > len(fechas):
#         print("ERROR: Opcion invalida. Por favor, seleccione una fecha válida.")
#         opcion2 = input("Seleccione una fecha: ")

#     opcion1 = int(opcion1)
#     opcion2 = int(opcion2)

#     precio = Calculo_precio(km_destinos, opcion1)

#     print("")
#     print("-" * 50)
#     print("ASIENTOS DISPONIBLES".center(50))
#     print("-" * 50)

#     print(f"Destino: {destinos[opcion1 - 1]}")
#     print(f"Fecha:   {fechas[opcion2 - 1]}")
#     print(f"Precio:  ${precio}")

#     print("")
#     ImprimirMatriz(matriz)

#     print("")
#     print("-" * 50)
    
#     asiento = input("Seleccione un asiento disponible: ")

#     while not (asiento[:-1].isdigit() and asiento[-1].isalpha()):
#         print("Formato de asiento inválido. Por favor, ingrese un asiento válido (por ejemplo, 1A).")
#         asiento = input("Seleccione un asiento disponible: ")

#     while not (asiento[:-1].isdigit() and asiento[-1].upper() in ["A", "B", "C", "D"]) or int(asiento[:-1]) < 1 or int(asiento[:-1]) > 10:
#         print("Formato de asiento inválido. Por favor, ingrese un asiento válido (por ejemplo, 1A).")
#         asiento = input("Seleccione un asiento disponible: ")
#     numero = int(asiento[:-1])
#     letra = asiento[-1].upper()

#     resultado = ElegirAsiento(numero, letra)


#     while resultado == 0 :
#          asiento = input("Seleccione un asiento disponible: ")
#          while not (asiento[:-1].isdigit() and asiento[-1].isalpha()):
#                 print("Formato de asiento inválido. Por favor, ingrese un asiento válido (por ejemplo, 1A).")
#                 asiento = input("Seleccione un asiento disponible: ")

#          numero = int(asiento[:-1])
#          letra = asiento[-1].upper()
#          resultado = ElegirAsiento(numero, letra)
#     asiento = str(numero)+letra

#     reserva = [usuarioActual, destinos[opcion1 - 1], fechas[opcion2 - 1], asiento, precio] 
#     AgregarReserva(reserva)
#     return reserva, opcion1

# def Calculo_precio(km_destinos, opcion1):
#      PRECIO_KILOMETRO = 120
#      PrecioPasaje = PRECIO_KILOMETRO * km_destinos[opcion1 - 1]
#      return PrecioPasaje
     


# destinos = ["Mar del Plata", "Pinamar", "Cobos", "Villa Gesel", "San Bernardo"]
# fechas = ["7/12/26","14/12/26","21/12/26","28/12/26","4/1/27","11/1/27","18/1/27"]    

micros = []

TARIFAPORKM = 100

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

def RegistrarMicro():
    patente = input("Ingrese la patendel del micro: ").upper().strip()
    while patente == "":
        print("Error: la patente no puede estar vacía.")
        patente = input("Ingrese la patente del micro: ").strip().upper()

    while patente in patentes:
        print("Error: esa patente ya está registrada.")
        patente = input("Ingrese otra patente: ").strip().upper()

        while patente == "":
            print("Error: la patente no puede estar vacía.")
            patente = input("Ingrese la patente del micro: ").strip().upper()
    micro = {
        "patente" : patente
    }
    micros.append(micro)
    patentes.add(patente)
    print("Micro registrado correctamente")
    
def VerMicros():
    print("=" * 50)
    print("MICROS REGISTRADOS".center(50))
    print("=" * 50)
    for micro in micros:
        print(f"Patente: {micro['patente']}")
    


    