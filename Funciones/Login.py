from Datos.Usuarios import usuarios, contrasenas
from Funciones.Registro import registro

def login():

    if len(usuarios) == 0:
        print("=" * 45)
        print("INICIO DE SESIÓN".center(45))
        print("=" * 45)
        print("")
        print("No hay usuarios registrados.".center(45))
        print("Debe registrarse antes de iniciar sesión.".center(45))
        print("")

        registro()

    else:
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
                    return True
                else:
                    print("Contraseña incorrecta!".center(45))
                    print("")
                    return False
        print("Usuario no Encontrado".center(45))
        
    print("")
    return False            