from Datos.Usuarios import usuarios, contrasenas

def registro():
    print("=" * 45)
    print("REGISTRO DE USUARIO".center(45))
    print("=" * 45)
    print("")

    usuario = input("Ingrese un Nombre de Usuario: ").strip()

    while usuario in usuarios:
        usuario = input("Ya existe el usuario, Ingrese uno nuevo: ").strip()

    usuarios.append(usuario)

    contrasena = input("Ingrese una Contraseña: ")
    contrasenas.append(contrasena)

    print("")
    print("Usuario registrado correctamente.".center(45))
    print("-" * 45)
    print("")
    
    return