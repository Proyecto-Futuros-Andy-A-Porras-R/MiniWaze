import tkinter

# funcion que valida si el usuario y la contraseña son correctos
def validarUsuario(usuario, contrasena):
    usuarios = retonarUsuarios()
    for nombre in usuarios:
        if nombre[0] == usuario:
            if nombre[1] == contrasena:
                return True
    return False

"""
funcion que retorna una lista de usuarios
"""
def retonarUsuarios():
    usuarios = []
    for linea in open("usuarios.txt"):
        nombre = ""
        contrasena = ""
        for caracter in linea:
            if caracter == ";":
                continue
            nombre += caracter
        for caracter in linea:
            if caracter == "/n":
                continue
            contrasena += caracter

        usuarios += [nombre, contrasena]
    return usuarios


"""
funcion que retorna la cantidad de letras de un texto
"""
def contarLetras(texto):
    contador = 0
    for letra in texto:
        contador += 1
    return contador

"""
lectura de archivo csv
"""
def leerArchivo():
    archivo = open("mapa.csv")
    mapa = []
    i = 0
    fila = []
    for linea in archivo:
        if linea == "\n":
            mapa += [fila]
        elif linea[i] == ";":
            continue 
        else:
            fila += [linea[i]]
    return mapa





