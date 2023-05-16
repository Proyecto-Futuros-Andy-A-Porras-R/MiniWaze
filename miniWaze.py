import tkinter

# funcion que valida si el usuario y la contraseña son correctos
def validarUsuario(usuario, contrasena):
    usuarios = retonarUsuarios()
    print("usuarios")
    print(usuarios)
    for nombre in usuarios:
        print(nombre[0][0], usuario, contrasena)
        if nombre[0][0] == usuario:
            if nombre[1][0] == contrasena:
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
        i = 0
        for letra in linea:
            if letra == ";" or letra == "\n":
                i += 1
                continue
            if i == 0:
                nombre += letra
            elif i == 1:
                contrasena += letra

        usuarios += [[[nombre],[contrasena]]]
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
def cargarMapa():
    archivo = open("mapa.csv")
    datos = archivo.readlines()
    mapa = []
    i = 0
    fila = []
    for linea in datos:
        for letra in linea:
            if letra == ";":
                continue
            if letra == "\n":
                mapa += [fila]
                fila = []
                continue
            else:
                fila += [letra]


    return mapa

"""
funcion que retorna la cantidad de filas de un mapa
"""
def contarFilas(mapa):
    contador = 0
    for fila in mapa:
        contador += 1
    return contador


# print(cargarMapa())

