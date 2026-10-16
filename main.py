from Menu import  menu_principal, menu_consultas, menu_ventas, menu_viajes
from Pasajes import AgregarReserva, VerVentas, BuscarVenta, ModificarVenta, CancelarVenta, VentasPorDestino, VentasPorFecha,VentasPorUsuario
from Funciones.Asientos import ImprimirMatriz, matriz, ElegirAsiento, CancelarAsiento,ModificarAsiento


# def main():

#     while True:
#         try:
#             opcion = int(menu_principal())
#             if opcion == 1:
#                 AgregarReserva()
#             if opcion == 2:
#                 VerVentas()
#             if opcion == 3:
#                 BuscarVenta()
#             if opcion == 4:
#                 ModificarVenta()
#             if opcion == 5:
#                 CancelarVenta()
#             if opcion == 6:
#                 ImprimirMatriz(matriz)
#             if opcion == 7:
#                 while True:
#                     opcion_consulta = int(consultas())
#                     if opcion_consulta == 1:
#                         VentasPorDestino()
#                     if opcion_consulta == 2:
#                         VentasPorFecha()
#                     if opcion_consulta == 3:
#                         VentasPorUsuario()
#                     if opcion_consulta == 4:
#                         break
#             if opcion == 8:
#                 print("Saliendo del sistema...")
#                 break
            

#         except ValueError:
#             print("Error: Ingrese un número válido.")

# main()

def main():

    while True:
        try:
            opcion = int(menu_principal())

            if opcion == 1:
                opcion = int(menu_ventas())

                if opcion == 1:
                    
                if opcion == 2:

                if opcion == 3:

                if opcion == 4:

                if opcion == 5:

                else:
                    print("Saliendo...")
                    break

            elif opcion == 2:
                opcion = int(menu_consultas())

                if opcion == 1:

                if opcion == 2:

                if opcion == 3:

                else:

            elif opcion == 3:
                opcion = int(menu_viajes())

                if opcion == 1:

                if opcion == 2:

                if opcion == 3:

                else:

            else:
                print("Saliendo...")

        except ValueError:
            print("Error: Ingrese un número válido.")
