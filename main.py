from Utils import (RegistrarViaje, VerViajes, RegistrarMicro, DarBajaMicro, 
                   VerMicros, VerDestinos, menu_informes, menu_principal,  
                   menu_ventas, menu_viajes, menu_micros, RegistrarVenta, 
                   AgregarDestino, CargarDatos,menu_destinos, Disponibilidad, EliminarDestino,InformeVentasPorDestino, 
                   InformeVentasPorFecha, InformeRecaudacionTotal, VerVentas, BuscarVenta, CancelarVenta, ModificarVenta)



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
                            VerVentas()
                            input("\nPresione Enter para volver al menú...")


                        elif opcion == 3:
                            #Buscar ventas
                            BuscarVenta()
                            input("\nPresione Enter para volver al menú...")
                            

                        elif opcion == 4:
                            #Modificar ventas
                            ModificarVenta()
                            input("\nPresione Enter para volver al menú...")

                        elif opcion == 5:
                            #Cancelar ventas
                            CancelarVenta()
                            input("\nPresione Enter para volver al menú...")

                        else:
                            break

                elif opcion == 2: #MENU Informes

                    while True:
                        opcion = int(menu_informes())

                        if opcion < 1 or opcion > 4:
                            print("Error: Ingrese un numero válido.")
                            continue
                        
                        if opcion == 1:
                            #Ventas por destino
                            InformeVentasPorDestino()
                            input("\nPresione Enter para volver al menú...")

                        elif opcion == 2:
                            #Ventas por fecha
                            InformeVentasPorFecha()
                            input("\nPresione Enter para volver al menú...")

                        elif opcion == 3:
                            InformeRecaudacionTotal()
                            input("\nPresione Enter para volver al menú...")


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
                            Disponibilidad()
                            input("\nPresione Enter para volver al menú...")


                        elif opcion == 2:
                            RegistrarViaje() 
                            input("\nPresione Enter para volver al menú...")
                        elif opcion == 3:
                            VerViajes()
                            input("\nPresione Enter para volver al menú...")


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
                            ("\nPresione Enter para volver al menú...")


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
                                input("\nPresione Enter para volver al menú...")

        
                            elif opcion == 2:
                                #Agregar destinos
                                AgregarDestino()
        
                            elif opcion == 3:
                                #Eliminar destinos
                                EliminarDestino()
                              

                            else:
                                break

                else:
                    print("Saliendo...")
                    break

            except ValueError as e:
                print("Error: ",e)
                continue

try:
        CargarDatos()
        main()
except KeyboardInterrupt:
    print("\nPrograma interrumpido por el usuario.")