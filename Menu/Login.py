from Menu.Menu import Menu 

usuarios=[]

def register():
    print("Iniciar sesión")
    usuario = input("Ingrese su usuario: ")
    contrasena = input("Ingresar su contraseña: ")
    guardarUsuario(usuario, contrasena)
    return usuario, contrasena

def guardarUsuario(usuario, contrasena):
    usuarios.append(usuario,contrasena)
    print("Usuario guardado correctamente.")

def verificarUsuario(usuario, contrasena):
    for u in usuarios:
        if u[0] == usuario and u[1] == contrasena:
            loginExitoso(usuario)

def loginExitoso(usuario):
    print("Bienvenido, ", usuario)
    Menu()
