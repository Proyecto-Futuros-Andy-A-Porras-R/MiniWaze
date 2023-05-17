import tkinter

# funcion que valida si el usuario y la contraseña son correctos
def validarUsuario(usuario, contrasena):
    datos = usuario + ";" + contrasena
    archivo = open("usuarios.txt", "r")
    usuarios = archivo.read()
    archivo.close()
    if datos not in usuarios:
        return False
    else:
        return True

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


# print(())

