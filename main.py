from Utils import (RegistrarViaje, VerViajes, RegistrarMicro, DarBajaMicro, 
                   VerMicros, VerDestinos, menu_principal, menu_consultas, 
                   menu_ventas, menu_viajes, menu_micros, RegistrarVenta, 
                   AgregarDestino, CargarDatos, CrearMatriz, ImprimirMatriz,
                   matriz, menu_destinos
    )

def main():
    
    while True:
        try:
            opcion = int(menu_principal())

            if opcion < 1 or opcion > 6:
                print("Error: Ingrese un numero válido.")
                continue

            if opcion == 1: #MENU VENTAS

                while True:

                    opcion = int(menu_ventas())

                    if opcion < 1 or opcion > 6:
                        print("Error: Ingrese un numero válido.")
                        continue

                    if opcion == 1:
                        #Registrar venta de pasaje
                        RegistrarVenta()

                    elif opcion == 2:
                        #Ver ventas
                        matriz = CrearMatriz()
                        ImprimirMatriz(matriz)

                    elif opcion == 3:
                        #Buscar ventas
                        print("No disponible")

                    elif opcion == 4:
                        #Modificar ventas
                        print("No disponible")

                    elif opcion == 5:
                        #Cancelar ventas
                        print("No disponible")

                    else:
                        break

            elif opcion == 2: #MENU CONSULTAS

                while True:
                    opcion = int(menu_consultas())

                    if opcion < 1 or opcion > 4:
                        print("Error: Ingrese un numero válido.")
                        continue
                    
                    if opcion == 1:
                        #Ventas por destino
                        print("No disponible")

                    elif opcion == 2:
                        #Ventas por fecha
                        print("No disponible")

                    elif opcion == 3:
                        #Ventas por usuario
                        print("No disponible")

                    else:
                        break

            elif opcion == 3: #MENU VIAJES
                
                while True:
                    opcion = int(menu_viajes())

                    if opcion < 1 or opcion > 4:
                        print("Error: Ingrese un numero válido.")
                        continue

                    if opcion == 1:
                        #Consultar disponibilidad
                        print("No disponible")

                    elif opcion == 2:
                        RegistrarViaje()  

                    elif opcion == 3:
                        VerViajes()

                    else:
                        break

            elif opcion == 4: #MENU MICROS

                while True:
                    opcion = int(menu_micros())

                    if opcion < 1 or opcion > 4:
                        print("Error: Ingrese un numero válido.")
                        continue

                    if opcion == 1:
                        #Ver micros
                        VerMicros()

                    elif opcion == 2:
                        #Registrar micros
                        RegistrarMicro()

                    elif opcion == 3:
                        #Dar de baja
                        DarBajaMicro()

                    else:
                        break

            elif opcion == 5: #MENU DESTINOS
                    while True:
                        opcion = int(menu_destinos())
    
                        if opcion < 1 or opcion > 4:
                            print("Error: Ingrese un numero válido.")
                            continue
    
                        if opcion == 1:
                            #Ver destinos
                            VerDestinos()
    
                        elif opcion == 2:
                            #Agregar destinos
                            AgregarDestino()
    
                        elif opcion == 3:
                            #Eliminar destinos
                            print("No disponible")    

                        else:
                            break

            else:
                print("Saliendo...")
                break

        except ValueError:
            print("Error: Ingrese un número válido.")


CargarDatos()
main()