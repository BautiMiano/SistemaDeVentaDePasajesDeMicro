import Utils

def ConvertirOpcion(opcion):
    try:
        numero = int(opcion)
    except ValueError:
        numero = 0

    return numero

def main():
    while True:
        opcion = ConvertirOpcion(Utils.MostrarMenuPrincipal())

        if opcion < 1 or opcion > 6:
            print("Error: ingrese un número válido.")
            continue

        if opcion == 1:
            while True:
                opcion_ventas = ConvertirOpcion(Utils.MostrarMenuVentas())

                if opcion_ventas < 1 or opcion_ventas > 4:
                    print("Error: ingrese un número válido.")
                    continue

                if opcion_ventas == 1:
                    Utils.RegistrarVenta()

                elif opcion_ventas == 2:
                    Utils.VerVentas()

                elif opcion_ventas == 3:
                    while True:
                        opcion_busqueda = ConvertirOpcion(Utils.MostrarMenuBuscarVenta())

                        if opcion_busqueda < 1 or opcion_busqueda > 4:
                            print("Error: ingrese un número válido.")
                            continue

                        if opcion_busqueda == 1:
                            venta = Utils.SeleccionarVentaPorAsiento()
                        elif opcion_busqueda == 2:
                            venta = Utils.SeleccionarVentaPorDni()
                        elif opcion_busqueda == 3:
                            venta = Utils.SeleccionarVentaPorNombre()
                        else:
                            break

                        if venta != None:
                            Utils.GestionarVenta(venta)

                else:
                    break

        elif opcion == 2:
            while True:
                opcion_informes = ConvertirOpcion(Utils.MostrarMenuInformes())

                if opcion_informes < 1 or opcion_informes > 4:
                    print("Error: ingrese un número válido.")
                    continue

                if opcion_informes == 1:
                    Utils.MostrarInformePorDestino()

                elif opcion_informes == 2:
                    Utils.MostrarInformePorMes()

                elif opcion_informes == 3:
                    Utils.MostrarRecaudacionTotal()

                else:
                    break

        elif opcion == 3:
            while True:
                opcion_viajes = ConvertirOpcion(Utils.MostrarMenuViajes())

                if opcion_viajes < 1 or opcion_viajes > 4:
                    print("Error: ingrese un número válido.")
                    continue

                if opcion_viajes == 1:
                    Utils.ConsultarDisponibilidad()

                elif opcion_viajes == 2:
                    Utils.RegistrarViaje()

                elif opcion_viajes == 3:
                    Utils.VerViajes()

                else:
                    break

        elif opcion == 4:
            while True:
                opcion_micros = ConvertirOpcion(Utils.MostrarMenuMicros())

                if opcion_micros < 1 or opcion_micros > 4:
                    print("Error: ingrese un número válido.")
                    continue

                if opcion_micros == 1:
                    Utils.VerMicros()

                elif opcion_micros == 2:
                    Utils.RegistrarMicro()

                elif opcion_micros == 3:
                    Utils.DarBajaMicro()

                else:
                    break

        elif opcion == 5:
            while True:
                opcion_terminales = ConvertirOpcion(Utils.MostrarMenuTerminales())

                if opcion_terminales < 1 or opcion_terminales > 4:
                    print("Error: ingrese un número válido.")
                    continue

                if opcion_terminales == 1:
                    Utils.VerTerminales()

                elif opcion_terminales == 2:
                    Utils.AgregarTerminal()

                elif opcion_terminales == 3:
                    Utils.EliminarTerminal()

                else:
                    break

        else:
            print("Saliendo...")
            break

# Programa principal
Utils.CargarDatos()

try:
    main()
except KeyboardInterrupt:
    print("\nPrograma cerrado. Los datos ya están guardados en datos.json.")