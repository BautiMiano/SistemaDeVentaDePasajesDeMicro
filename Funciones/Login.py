from Datos.Usuarios import usuarios, contrasenas
from Funciones.Registro import registro

def login():

    if len(usuarios) == 0:
        print("No hay usuarios registrados")
        print("Se debe registrar")
        print("")
        registro()
    else:
        print("ΞΞΞ Login ΞΞΞ")
        print("")
        usuario = input("Ingrese su nombre de usuario: ")
        contrasena = input("Ingrese su contraseña: ")
        print("")
        
        for i in range(len(usuarios)):
            if usuario == usuarios[i]:
                if contrasena == contrasenas[i]:
                    print("Usted a ingresado correctamente!")
                    return True
                else:
                    print("Contraseña incorrecta!")
                    return False
        print("Usuario no Encontrado")
    print("")
    return False            