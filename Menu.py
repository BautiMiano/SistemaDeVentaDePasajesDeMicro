def menu_principal():
    print("=" * 45)
    print("SISTEMA DE GESTIÓN".center(45))
    print("=" * 45)
    print("")
    print("1 - Ventas")
    print("2 - Consultas")
    print("3 - Viajes")
    print("4 - Salir")

    print("")
    print("-" * 45)
    opcion = input("Seleccione una opcion: ")
    print("")
    return opcion

def menu_ventas():
    print("=" * 45)
    print("VENTAS".center(45))
    print("=" * 45)
    print("")
    print("1 - Registrar venta de pasaje")
    print("2 - Ver ventas")
    print("3 - Buscar venta")
    print("4 - Modificar venta")
    print("5 - Cancelar venta")
    print("6 - volver atras")
    print("")

    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion

def menu_consultas():
    print("="*45)
    print("CONSULTAS".center(45))
    print("="*45)
    print("")
    print("1 - Consultar ventas por destino")
    print("2 - Consultar ventas por fecha")
    print("3 - Consultar ventas por usuario")
    print("4 - volver atras")
    print("")

    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion

def menu_viajes():
    print("="*45)
    print("Viajes".center(45))
    print("="*45)
    print("")
    print("1 - Consultar disponibilidad")
    print("2 - Agregar destinos")
    print("3 - Eliminar destinos")
    print("4 - volver atras")
    print("")
    
    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion