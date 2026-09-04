def register():
    print("")
    print("Registrar Nuevo Usuario")
    usuario = input("Ingrese un nombre de usuario: ")
    usuarios.append(usuario)
    print("")
    contrasena = input("Ingrese una contraseña: ")
    contrasenas.append(contrasena)
    print("Usuario registrado correctamente!")
    print("")
    login()
    return

def login():
    print("Iniciar sesión")
    print("")
    usuario = input("Ingrese su usuario: ")
    print("")
    contrasena = input("Ingresar su contraseña: ")
    for i in range(len(usuarios)):
        if usuario == usuarios[i]:
            if contrasena == contrasenas[i]:
                print("Sesion Iniciada")
                return True
            else:
                print("Contraseña Invalida!")
                return False
        else:
            print("Usuario no encontrado!")
            return False

usuarios= []
contrasenas = []