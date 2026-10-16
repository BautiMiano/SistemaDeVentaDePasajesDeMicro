from Funciones.VentaPasaje import VentaPasajes
from Menu import menu_inicio, menu_principal
from Funciones.ReservaPasaje import VerReserva, CancelarReserva
from Funciones.Registro import registro, login


def main():

    while True:
        try:
            opcion = int(menu_principal())

            if opcion == 1:
                opcion = int(menu_ventas())

                if opcion == 1:
                    #Registrar venta de pasaje

                if opcion == 2:
                    #Ver ventas

                if opcion == 3:
                    #Buscar ventas

                if opcion == 4:
                    #Modificar ventas

                if opcion == 5:
                    #Cancelar ventas
                else:
                    print("Saliendo...")
                    break

            elif opcion == 2:
                opcion = int(menu_consultas())

                if opcion == 1:
                    #Ventas por destino

                if opcion == 2:
                    #Ventas por fecha

                if opcion == 3:
                    #Ventas por usuario
                else:
                    print("Saliendo...")
                    break

            elif opcion == 3:
                opcion = int(menu_viajes())

                if opcion == 1:
                    #Consultar disponibilidad

                if opcion == 2:
                    #Agregar destinos

                if opcion == 3:
                    #Eliminar destinos

                else:
                    print("Saliendo...")
                    break
            else:
                print("Saliendo...")

        except ValueError:
            print("Error: Ingrese un número válido.")
