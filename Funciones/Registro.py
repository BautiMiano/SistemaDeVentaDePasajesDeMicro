from Datos import usuarios, contrasenas

def registro():
    print("=" * 45)
    print("REGISTRO DE USUARIO".center(45))
    print("=" * 45)
    print("")

    usuario = input("Ingrese un Nombre de Usuario: ").strip()

    while usuario == "" or usuario in usuarios:
        if usuario == "":
            usuario = input("El usuario no puede estar vacío. Ingrese uno nuevo: ").strip()
        else:
            usuario = input("Ya existe el usuario, ingrese uno nuevo: ").strip()

    usuarios.append(usuario)

    contrasena = input("Ingrese una Contraseña: ")

    while contrasena.strip() == "":
        contrasena = input("La contraseña no puede estar vacía. Ingrese una nueva: ")

    contrasenas.append(contrasena)

    print("")
    print("Usuario registrado correctamente.".center(45))
    print("-" * 45)
    print("")
    
    return

def login():


    print("=" * 45)
    print("INICIO DE SESIÓN".center(45))
    print("=" * 45)
    print("")

    usuario = input("Ingrese su nombre de usuario: ").strip()
    contrasena = input("Ingrese su contraseña: ").strip()

    print("")
    
    for i in range(len(usuarios)):
        if usuario == usuarios[i]:
            if contrasena == contrasenas[i]:
                print("Usted a ingresado correctamente!".center(45))
                print("")
                return usuario
            else:
                print("Contraseña incorrecta!".center(45))
                print("")
                return False
    print("Usuario no Encontrado".center(45))
        
    print("")
    return False            