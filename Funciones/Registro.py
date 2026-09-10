from Datos.Usuarios import usuarios, contrasenas

def registro():
    print("ΞΞΞ Registro ΞΞΞ")
    print("")
    usuario = input("Ingrese un Nombre de Usuario: ")
    while usuario in usuarios:
        usuario = input("Ya existe el usuario, Ingrese uno nuevo: ")
    usuarios.append(usuario)

    contrasena = input("Ingrese una Contraseña: ")
    contrasenas.append(contrasena)
    print("")
    return