from Menu.Sesion import login, register, usuarios, contrasenas

def Menu_Inicio_Sesion():
    print("Bienvenido al Sistema de Venta de Pasajes de Micro")
    print("1 - Iniciar Sesión")
    print("2 - Registrarse")
    print("3 - Salir")
    opcion = int(input("Eliga una opcion: "))
    if len(usuarios) == 0 and len(contrasenas) == 0:
        register()
    else:    
        if opcion == 1:
            login()
        elif opcion == 2:
            register()
        elif opcion == 3:
            print("Saliendo")
        else:
            print("Opcion Invalida")

def Menu_Sesion_Iniciada():
    print("MENU - Venta de pasajes de micro")
    print("1 - Venta pasajes")
    print("2 - Ver reserva")
    print("3 - Cancelar reserva")
    print("4 - Cerrar sesión")
    opcion = input("Eliga una opcion: ")
    return opcion