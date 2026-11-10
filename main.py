import Utils

# Qué hace: convierte a número la opción que se escribió en un menú.
# Recibe: opcion, el texto que devolvió la función del menú.
# Devuelve: la opción como número entero, o 0 si lo escrito no era un número. El 0 queda
#   fuera de rango en todos los menús, así que main() lo toma como opción inválida.
# Cómo funciona: intenta convertir con int() dentro de un try; si da ValueError, usa 0. Se
#   hizo como función porque se usa en los 6 menús y evita repetir el mismo try/except.
# Estructuras y temas: excepciones (ValueError).
def ConvertirOpcion(opcion):
    try:
        numero = int(opcion)
    except ValueError:
        numero = 0

    return numero

# Qué hace: maneja toda la navegación entre los menús del sistema.
# Recibe: nada.
# Devuelve: nada.
# Cómo funciona: un while True muestra el menú principal y controla que la opción esté
#   entre 1 y 6. Cada opción del 1 al 5 entra a su submenú, que tiene su propio while True
#   y llama a las funciones de Utils según lo que se elija. La opción "Volver atrás" de cada
#   submenú hace break y vuelve al menú principal. En Ventas hay un tercer nivel, el menú
#   de búsqueda: si la búsqueda encuentra una venta, se llama a GestionarVenta(). La opción
#   6 del menú principal termina el programa. Cada submenú guarda su respuesta en su propia
#   variable (opcion_ventas, opcion_informes, etc.) para no pisar la del menú principal.
# Estructuras y temas: ciclos while, if/elif/else y funciones de un módulo propio (Utils).
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
# Primero se cargan los datos guardados con CargarDatos() y después se ejecuta main().
# El try/except KeyboardInterrupt hace que, si el usuario cierra el programa con Ctrl+C,
# se muestre un mensaje en lugar de un error. Los datos no se pierden porque cada
# operación ya se guardó en datos.json al terminar.
Utils.CargarDatos()

try:
    main()
except KeyboardInterrupt:
    print("\nPrograma cerrado. Los datos ya están guardados en datos.json.")
