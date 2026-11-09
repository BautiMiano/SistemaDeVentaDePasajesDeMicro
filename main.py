import Utils

def ConvertirOpcion(opcion):

    try:
        numero = int(opcion)
    except ValueError:
        numero = 0
    return numero

def main():

    while True:
        opcion = ConvertirOpcion(Utils.menu_principal())

        if opcion < 1 or opcion > 6:
            print("Error: Ingrese un numero válido.")
            continue

        if opcion == 1: #MENU VENTAS

            while True:

                opcion = ConvertirOpcion(Utils.menu_ventas())

                if opcion < 1 or opcion > 4:
                    print("Error: Ingrese un numero válido.")
                    continue

                if opcion == 1:
                    Utils.RegistrarVenta()

                elif opcion == 2:
                    Utils.VerVentas()

                elif opcion == 3: #SUBMENU BUSCAR VENTA

                    while True:
                        opcion = ConvertirOpcion(Utils.menu_buscar_venta())

                        if opcion < 1 or opcion > 4:
                            print("Error: Ingrese un numero válido.")
                            continue

                        if opcion == 1:
                            venta = Utils.SeleccionarVentaPorAsiento()
                        elif opcion == 2:
                            venta = Utils.SeleccionarVentaPorDni()
                        elif opcion == 3:
                            venta = Utils.SeleccionarVentaPorNombre()
                        else:
                            break

                        if venta != None:
                            Utils.GestionarVenta(venta)

                else:
                    break

        elif opcion == 2: #MENU INFORMES

            while True:
                opcion = ConvertirOpcion(Utils.menu_informes())

                if opcion < 1 or opcion > 4:
                    print("Error: Ingrese un numero válido.")
                    continue

                if opcion == 1:
                    Utils.InformeVentasPorDestino()

                elif opcion == 2:
                    Utils.InformeVentasPorMes()

                elif opcion == 3:
                    Utils.InformeRecaudacionTotal()

                else:
                    break

        elif opcion == 3: #MENU VIAJES

            while True:
                opcion = ConvertirOpcion(Utils.menu_viajes())

                if opcion < 1 or opcion > 4:
                    print("Error: Ingrese un numero válido.")
                    continue

                if opcion == 1:
                    Utils.Disponibilidad()

                elif opcion == 2:
                    Utils.RegistrarViaje()

                elif opcion == 3:
                    Utils.VerViajes()

                else:
                    break

        elif opcion == 4: #MENU MICROS

            while True:
                opcion = ConvertirOpcion(Utils.menu_micros())

                if opcion < 1 or opcion > 4:
                    print("Error: Ingrese un numero válido.")
                    continue

                if opcion == 1:
                    Utils.VerMicros()

                elif opcion == 2:
                    Utils.RegistrarMicro()

                elif opcion == 3:
                    Utils.DarBajaMicro()

                else:
                    break

        elif opcion == 5: #MENU DESTINOS

            while True:
                opcion = ConvertirOpcion(Utils.menu_destinos())

                if opcion < 1 or opcion > 4:
                    print("Error: Ingrese un numero válido.")
                    continue

                if opcion == 1:
                    Utils.VerDestinos()

                elif opcion == 2:
                    Utils.AgregarDestino()

                elif opcion == 3:
                    Utils.EliminarDestino()

                else:
                    break

        else:
            print("Saliendo...")
            break

Utils.CargarDatos()

try:
    main()
except KeyboardInterrupt:
    print("\nPrograma cerrado. Los datos ya están guardados en datos.json.")
