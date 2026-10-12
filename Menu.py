def menu_principal():
    print("=" * 45)
    print("SISTEMA DE GESTIÓN".center(45))
    print("=" * 45)
    print("")
    print("1 - Registrar venta de pasaje")
    print("2 - Ver ventas")
    print("3 - Buscar venta")
    print("4 - Modificar venta")
    print("5 - Cancelar venta")
    print("6 - Consultar disponibilidad")
    print("7 - Consultas")
    print("8 - Salir ")

    print("")
    print("-" * 45)
    opcion = input("Seleccione una opcion: ")
    print("")
    return opcion

def consultas():
    print("="*45)
    print("CONSULTAS".center(45))
    print("="*45)
    print("")
    print("1 - Consultar ventas por destino")
    print("2 - Consultar ventas por fecha")
    print("3 - Consultar ventas por usuario")
    print("4 - Volver al menú principal")
    print("")
    print("="*45)
    opcion = input("Seleccione una opción: ")
    print("")
    return opcion