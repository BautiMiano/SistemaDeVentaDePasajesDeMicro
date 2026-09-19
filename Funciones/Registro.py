from Datos.Usuarios import usuarios, contrasenas

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