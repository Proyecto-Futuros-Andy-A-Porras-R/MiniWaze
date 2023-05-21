import tkinter as tk
from tkinter import messagebox as mb, filedialog as fd, ttk
import csv
global inicioSeleccionado
inicioSeleccionado = [-1,-1]
global destinoSeleccionado
destinoSeleccionado = [-1,-1]
global nuevoMapa
nuevoMapa = []
global destinos 
destinos = []
        
#--------------------VENTANA AUTENTICACION---------------------
def ventanaAutenticacion():
    global ventanaAutenticacion
    ventanaAutenticacion = tk.Tk()
    ventanaAutenticacion.title("Autenticacion")
    #centrar ventana en la pantalla
    x_ventana = ventanaAutenticacion.winfo_screenwidth() // 2 - 800 // 2
    y_ventana = ventanaAutenticacion.winfo_screenheight() // 2 - 400 // 2
    posicion = str(800) + "x" + str(400) + "+" + str(x_ventana) + "+" + str(y_ventana)
    ventanaAutenticacion.geometry(posicion)
    ventanaAutenticacion.iconbitmap("icono.ico")

    labelImagen = tk.Label(ventanaAutenticacion, bg="white")
    labelImagen.pack(side=tk.LEFT, fill=tk.Y)
    imagen = tk.PhotoImage(file="fondo.png")
    labelImagen.config(image=imagen)
    
    frameDerecha = tk.Frame(ventanaAutenticacion, width=600, height=400, bg="white")
    frameDerecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    labelBienvenida = tk.Label(frameDerecha, text="Bienvenido/a a la app", font=("Helvetica", 20, "bold"), bg="white")
    labelBienvenida.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    
    labelUsuario = tk.Label(frameDerecha, text="Usuario", font=("Helvetica", 10, "bold"), bg="white")
    labelUsuario.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    entryUsuario = tk.Entry(frameDerecha)
    entryUsuario.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    labelContrasena = tk.Label(frameDerecha, text="Contraseña", font=("Helvetica", 10, "bold"), bg="white")
    labelContrasena.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    
    entryContrasena = tk.Entry(frameDerecha, show="*")
    entryContrasena.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    
    botonIngresar = tk.Button(frameDerecha, text="Ingresar", font=("Helvetica", 10, "bold"), command=lambda: validarUsuarioInterfaz(entryUsuario.get(), entryContrasena.get()))
    botonIngresar.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonIngresar.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)

    labelNoCuenta = tk.Label(frameDerecha, text="¿Aún no tienes cuenta?", font=("Helvetica", 10, "bold"), bg="white")
    labelNoCuenta.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    
    botonRegistrarse = tk.Button(frameDerecha, text="Registrarse", font=("Helvetica", 10, "bold"), command=lambda: registrarse(labelNoCuenta, botonIngresar, botonRegistrarse, entryUsuario, entryContrasena))
    botonRegistrarse.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonRegistrarse.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)

    # boton de salir
    botonSalir = tk.Button(frameDerecha, text="Salir", font=("Helvetica", 10, "bold"), command=lambda: ventanaAutenticacion.destroy())
    botonSalir.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonSalir.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)

    ventanaAutenticacion.mainloop()

def registrarse(labelNoCuenta, botonIngresar, botonRegistrarse, entryUsuario, entryContrasena):
    # limpia los entrys
    entryUsuario.delete(0, tk.END)
    entryContrasena.delete(0, tk.END)
    botonIngresar.pack_forget()
    # cambia el texto del label
    labelNoCuenta.config(text="Ingresa tus datos y registrate")
    # cambia la funcion del boton de registrarse
    botonRegistrarse.config(text="Registrarse", command=lambda: registrarUsuarioInterfaz(entryUsuario.get(), entryContrasena.get()))

def registrarUsuarioInterfaz(usuario, contrasena):
    datos = "\n" + usuario + ";" + contrasena
    archivo = open("usuarios.txt", "r")
    usuarios = archivo.read()
    archivo.close()
    
    if datos in usuarios:
        mb.showerror("Error", "El usuario ya existe")
    else:
        archivo = open("usuarios.txt", "a")
        archivo.write(datos)
        archivo.close()
        mb.showinfo("Exito", "Usuario registrado")
        ventanaAutenticacion.destroy()
        ventanaPrincipal()

def validarUsuarioInterfaz(usuario, contrasena):
    if validarUsuario(usuario, contrasena):
        ventanaAutenticacion.destroy()
        ventanaPrincipal()
        return 0
    else:
        # mensaje de error
        mb.showerror("Error", "Usuario o contraseña incorrectos")
        return 0

#-------------------VENTANA PRINCIPAL-------------------
def ventanaPrincipal():
    global ventanaPrincipal
    ventanaPrincipal = tk.Tk()
    ventanaPrincipal.title("MiniWaze")
    ventanaPrincipal.state("zoomed")
    ventanaPrincipal.resizable(0, 0)
    ventanaPrincipal.iconbitmap("icono.ico")
    
    global botonesPrincipales
    botonesPrincipales = []
    #widget de la barra de menu
    barraMenu = tk.Menu(ventanaPrincipal)
    #opciones de la barra de menu
    #opcion cargar archivo
    menuArchivo = tk.Menu(barraMenu, tearoff=0)
    menuArchivo.add_command(label="Cargar archivo", command=lambda: cargarArchivo())
    menuArchivo.add_command(label="Crear mapa", command=lambda: crearMapa())
    menuArchivo.add_separator()
    menuArchivo.add_command(label="Salir", command=lambda: ventanaPrincipal.destroy())
    barraMenu.add_cascade(label="Archivo", menu=menuArchivo)
    #opcion ayuda
    menuAyuda = tk.Menu(barraMenu, tearoff=0)
    menuAyuda.add_command(label="Acerca de", command=lambda: mb.showinfo("Acerca de", "proyecto en construccion"))
    menuAyuda.add_command(label="Ayuda", command=lambda: mb.showinfo("Ayuda", "Para cargar un mapa, seleccione la opción de cargar archivo del menú Archivo\n\nPara salir del programa, seleccione la opción de salir del menú Archivo, o la opción salir del menú principal\n\nPara tener acceso a todas las funciones, primero debe cargar un mapa o crear uno"))
    barraMenu.add_cascade(label="Ayuda", menu=menuAyuda)
    #configuracion de la barra de menu
    ventanaPrincipal.config(menu=barraMenu)

    #creacion de los botones de opciones del menu
    #seleccionar destino, planificar destino, guardar destino, borrar destino y modificar mapa
    #todos van en el frame izquierdo, que mide la mitad del ancho de la ventana
    global frameIzquierdo
    frameIzquierdo = tk.Frame(ventanaPrincipal, width=400, height=ventanaPrincipal.winfo_height(), bg="white")
    frameIzquierdo.pack(side="left", fill="both", expand=True)
    labelInicial = tk.Label(frameIzquierdo, text="Bienvenid@ al Mini Waze", font=("Helvetica", 30, "bold"), bg="white")
    labelInicial2 = tk.Label(frameIzquierdo, text="por favor cargue un archivo o cree un mapa para continuar", font=("Helvetica", 16, "bold"), bg="white")
    labelInicial.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    labelInicial2.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)


    #frame derecho para el mapa
    global frameDerecho
    frameDerecho = tk.Frame(ventanaPrincipal, width=400, height=ventanaPrincipal.winfo_height(), bg="white")
    frameDerecho.pack(side="right", fill="both", expand=True)
    imagenFondo = tk.PhotoImage(file="mapa.png")
    labelFondo = tk.Label(frameDerecho, image=imagenFondo, bg="#008CBA")
    labelFondo.place(x=0, y=0, relwidth=1, relheight=1)
    ventanaPrincipal.mainloop()

def cargarArchivo():
    #solo acepta archivos csv
    archivo = fd.askopenfilename(
            filetypes=[("Archivos CSV", "*.csv")],
            title="Seleccionar archivo CSV"
        )
    if archivo != "":
        cargarMapaInterfaz(archivo)

#-----------------FUNCIONES PARA WIDGETS-----------------
#despliega las opciones del menu
def mostrarOpciones():
    #limpia el frame izquierdo
    for widget in frameIzquierdo.winfo_children():
        widget.destroy()    

    #seleccionar destino
    botonSeleccionarDestino = tk.Button(frameIzquierdo, text="Seleccionar destino", font=("Helvetica", 10, "bold"), command=lambda: seleccionarRuta())
    botonSeleccionarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonSeleccionarDestino.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    botonesPrincipales.append(botonSeleccionarDestino)
    #planificar destino
    botonPlanificarDestino = tk.Button(frameIzquierdo, text="Planificar destino", font=("Helvetica", 10, "bold"))#, command=lambda: cargarVentanaAnterior(ventanaPrincipal, ventanaPlanificarDestino))
    botonPlanificarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonPlanificarDestino.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    botonesPrincipales.append(botonPlanificarDestino)
    #guardar destino
    botonGuardarDestino = tk.Button(frameIzquierdo, text="Guardar destino", font=("Helvetica", 10, "bold"), command=lambda: guardarDestino())#, command=lambda: cargarVentanaAnterior(ventanaPrincipal, ventanaGuardarDestino))
    botonGuardarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonGuardarDestino.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    botonesPrincipales.append(botonGuardarDestino)
    #borrar destino
    botonBorrarDestino = tk.Button(frameIzquierdo, text="Borrar destino", font=("Helvetica", 10, "bold"))#, command=lambda: borrarDestino())#, command=lambda: cargarVentanaAnterior(ventanaPrincipal, ventanaBorrarDestino))
    botonBorrarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonBorrarDestino.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    botonesPrincipales.append(botonBorrarDestino)
    #modificar mapa
    botonModificarMapa = tk.Button(frameIzquierdo, text="Modificar mapa", font=("Helvetica", 10, "bold"))#, command=lambda: cargarVentanaAnterior(ventanaPrincipal, ventanaModificarMapa))
    botonModificarMapa.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonModificarMapa.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    botonesPrincipales.append(botonModificarMapa)
    #boton salir
    botonSalir = tk.Button(frameIzquierdo, text="Salir", font=("Helvetica", 10, "bold"), command=lambda: ventanaPrincipal.destroy())
    botonSalir.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonSalir.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)


# funcion para guardar el destino seleccionado
def guardarDestino():
    # si no se ha seleccionado un destino
    if inicioSeleccionado == [-1,-1] or destinoSeleccionado == [-1,-1]:
        mb.showerror("Error", "No se ha seleccionado un destino")
    else:
        # se agrega el destino a la lista de destinos
        global destinos
        destinos += [nombreMapaSeleccionado,destinoSeleccionado[0],destinoSeleccionado[1]]
        mb.showinfo("Información", "Destino guardado con éxito")


#quita las opciones del menu
def quitarOpciones():
    for widget in frameIzquierdo.winfo_children():
        widget.destroy()
    botonesPrincipales = []

# habilita los botones del mapa
def habilitarMapa():
    for fila in botones:
        for boton in fila:
            boton.config(state=tk.NORMAL)

# bloquea los botones del mapa
def bloquearMapa():
    for fila in botones:
        for boton in fila:
            boton.config(state=tk.DISABLED)

#---------------------FUNCIONES PARA MAPA---------------------
#muestra un mapa de botones en la parte derecha de la interfaz
#E: el nombre del archivo
def cargarMapaInterfaz(archivo):
    global mapa 
    mapa = cargarMapa(archivo)
    copiaMapa = mapa
    filaTotal = contarFilas(copiaMapa)
    columnaTotal = totalColumnas(copiaMapa)
    #limpiar frame derecho
    for widget in frameDerecho.winfo_children():
        widget.destroy()

    mostrarOpciones()
    global botones
    botones = []
    for fila in range(filaTotal):
        filaBotones = []
        for columna in range(columnaTotal):
            if mapa[fila][columna] == '0':
                boton = tk.Button(frameDerecho, text="",font=("Arial", 12), width=1, height=1, bg="black", fg="black", command=lambda fila=fila, columna=columna: seleccionarBoton(fila, columna))
                boton.grid(row=fila, column=columna)
                filaBotones.append(boton)
            else:
                symbol = mapa[fila][columna]
                if fila == inicioSeleccionado[0] and columna == inicioSeleccionado[1]:
                    boton = tk.Button(frameDerecho, text=symbol, font=("Arial", 12), width=1, height=1, bg="green", fg="green", command=lambda fila=fila, columna=columna: seleccionarBoton(fila, columna))
                    boton.grid(row=fila, column=columna)
                    filaBotones.append(boton)
                    continue
                elif fila == destinoSeleccionado[0] and columna == destinoSeleccionado[1]:
                    boton = tk.Button(frameDerecho, text=symbol, font=("Arial", 12), width=1, height=1, bg="red", fg="red", command=lambda fila=fila, columna=columna: seleccionarBoton(fila, columna))
                    boton.grid(row=fila, column=columna)
                    filaBotones.append(boton)
                    continue
                boton = tk.Button(frameDerecho, text=symbol, font=("Arial", 12), width=1, height=1, bg="white", fg="black", command=lambda fila=fila, columna=columna: seleccionarBoton(fila, columna))
                boton.grid(row=fila, column=columna)
                filaBotones.append(boton)
        botones.append(filaBotones)
    bloquearMapa()

""" 
reinicia los colores de los botones al color original (blanco)
E: colores= entero positivo donde 0=verde, 1=rojo, 2=ambos
"""
def decolorar(colores):
    for fila in botones:
        for boton in fila:
            if colores == 0:
                if boton.cget("bg") == "green":
                    boton.config(bg="white")
                    return 0
            elif colores == 1:
                if boton.cget("bg") == "red":
                    boton.config(bg="white")
                    return 0
            elif colores == 2:
                if boton.cget("bg") == "green" or boton.cget("bg") == "red":
                    boton.config(bg="white")
            
#despliega el menu para seleccionar el punto de inicio y destino, tambien para calcular la ruta
def seleccionarRuta():
    quitarOpciones()
    botonSeleccionarInicio = tk.Button(frameIzquierdo, text="Seleccionar punto de inicio", command=seleccionarInicio,font=("Arial", 7), height=1, bg="white", fg="black")
    botonSeleccionarInicio.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    botonSeleccionarDestino = tk.Button(frameIzquierdo, text="Seleccionar punto de destino", command=seleccionarDestino, font=("Arial", 7), height=1, bg="white", fg="black")
    botonSeleccionarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    botonCalcularRuta = tk.Button(frameIzquierdo, text="Calcular ruta", command=calcularRuta, font=("Arial", 7), height=1, bg="white", fg="black")
    botonCalcularRuta.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    botonConfirmarRuta = tk.Button(frameIzquierdo, text="Confirmar ruta", command=confirmarRuta, font=("Arial", 7), height=1, bg="white", fg="black")
    botonConfirmarRuta.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

#desaparece los botones de opciones de seleccionar ruta
def confirmarRuta():
    mostrarOpciones()
    bloquearMapa()
    decolorar(2)

""" 
 funcion a la que responden los botones que conforman el mapa
 E: a= fila del boton, b= columna del boton
 S: cambia el color del boton seleccionado
 R: el boton no debe ser de otro color que no sea blanco
"""
def seleccionarBoton(a,b):
    boton1 = botones[a][b]
    if(boton1.cget("bg") == "black" or boton1.cget("bg") == "red" or boton1.cget("bg") == "green"):
        mb.showerror("Error", "Seleccione otro punto\nEl seleccionado ya está ocupado o es un obstáculo")
        return 0
    elif inicioSeleccionado[0] == -1 and inicioSeleccionado[1] == -1:
        boton1.config(bg="green")
        inicioSeleccionado[0] = a
        inicioSeleccionado[1] = b
        bloquearMapa()
    elif destinoSeleccionado[0] == -1 and destinoSeleccionado[1] == -1:
        boton1.config(bg="red")
        destinoSeleccionado[0] = a
        destinoSeleccionado[1] = b
        bloquearMapa()

#---------------FUNCIONES DE CREACION DE MAPA------------------
# funcion para crear un mapa
def crearMapa():
    # limpiar frameIzquierdo
    for widget in frameIzquierdo.winfo_children():
        widget.destroy()
    # limpiar frameDerecho
    for widget in frameDerecho.winfo_children():
        widget.destroy()
    # limpiar botones  
    botones = []
    inicioSeleccionado[0] = inicioSeleccionado[1] = destinoSeleccionado[0] = destinoSeleccionado[1] = -1
    
    labelFilas = tk.Label(frameIzquierdo, text="Filas: ", font=("Arial", 12))
    labelFilas.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    comboFilas = ttk.Combobox(frameIzquierdo, state="readonly", font=("Arial", 12), width=5)
    comboFilas.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    comboFilas["values"] = [i for i in range(10, 22)]
    comboFilas.current(0)

    labelColumnas = tk.Label(frameIzquierdo, text="Columnas: ", font=("Arial", 12))
    labelColumnas.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    comboColumnas = ttk.Combobox(frameIzquierdo, state="readonly", font=("Arial", 12), width=5)
    comboColumnas.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    comboColumnas["values"] = [i for i in range(10, 35)]
    comboColumnas.current(0)

    botonCrearMapa = tk.Button(frameIzquierdo, text="Crear mapa", command=lambda: dibujarMapa(int(comboFilas.get()), int(comboColumnas.get())), font=("Arial", 12), height=1, bg="white", fg="black")
    botonCrearMapa.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonGuardarMapa = tk.Button(frameIzquierdo, text="Guardar mapa", command=guardarMapa, font=("Arial", 12), height=1, bg="white", fg="black")
    botonGuardarMapa.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

#dibuja el mapa para crear en el frameDerecho
def dibujarMapa(filas, columnas):
    # limpiar frameDerecho
    for widget in frameDerecho.winfo_children():    
        widget.destroy()
    global nuevoMapa
    nuevoMapa = []
    for fila in range(filas):
        filas = []
        for columna in range(columnas):
            boton = tk.Button(frameDerecho, text="0",font=("Arial", 12), width=1, height=1, bg="black", fg = "white", command=lambda fila=fila, columna=columna: cambiarColor(fila, columna))
            boton.grid(row=fila, column=columna)
            filas.append(boton)
        nuevoMapa.append(filas)

#funciones de los botones, cambian las letras de los botones
# E: fila: total de filas, columna: total de columnas
def cambiarColor(fila, columna):
    boton = nuevoMapa[fila][columna]
    # cada toque cambia a una letra, por defecto es un 0
    # las letras son N, S, L, R, C y ND
    if boton.cget("text") == "0":
        boton.config(text="N")
        boton.config(bg="white")
        boton.config(fg="black")
    elif boton.cget("text") == "N":
        boton.config(text="S")
    elif boton.cget("text") == "S":
        boton.config(text="L")
    elif boton.cget("text") == "L":
        boton.config(text="R")
    elif boton.cget("text") == "R":
        boton.config(text="C")
    elif boton.cget("text") == "C":
        boton.config(text="ND")
    else:
        boton.config(text="0")
        boton.config(bg="black")
        boton.config(fg="white")

#guarda el mapa en un archivo csv
#R: si no hay nada para guardar, retorna 0 y un error diciendo que no hay nada para guardar
def guardarMapa():
    # validar si hay algo para guardar
    if nuevoMapa == []:
        mb.showerror("Error", "Primero cree un mapa")
        return 0

    # guardar mapa en un string
    mapa = ""
    for fila in nuevoMapa:
        for boton in fila:
            mapa += boton.cget("text")+";"
        mapa = mapa[:-1]
        mapa += "\n"
    # quitar el ultimo salto de linea
    mapa = mapa[:-1]
    archivo = fd.asksaveasfile(title="Guardar mapa", mode="w", defaultextension=".csv", filetypes=[("Archivo CSV", "*.csv")])
    if archivo is None:
        return
    archivo.write(mapa)
    archivo.close()
    mb.showinfo("Información", "Mapa guardado con éxito")
    cargarMapaInterfaz(archivo.name)
#--------------FUNCIONES DE SELECCION DE RUTA------------------
# habilita los botones del mapa para que se seleccione el inicio
def seleccionarInicio():
    decolorar(0)
    inicioSeleccionado[0] = inicioSeleccionado[1] = -1
    mb.showinfo("Información", "Seleccione el punto de inicio\n cuando se seleccione, se tornará verde")
    habilitarMapa()

# habilita los botones del mapa para que se seleccione el destino
def seleccionarDestino():
    if inicioSeleccionado[0] == -1 and inicioSeleccionado[1] == -1:
        mb.showerror("Error", "Seleccione el punto de inicio primero")
        return 0
    
    decolorar(1)
    destinoSeleccionado[0] = destinoSeleccionado[1] = -1
    mb.showinfo("Información", "Seleccione el punto de destino\n cuando se seleccione, se tornará rojo")
    habilitarMapa()
##############################################################################################################
"""
Cuando  el  usuario  calcule  la  duración  de  su  trayecto  debe  tomar  en  cuenta  que  su  valor 
puede variar según la hora del día en que realiza esta operación. A continuación, se muestra 
los valores para cada uno de los elementos del mapa.
"""
def calcularRuta():
    # L son calles donde su direccion de navegacion es de derecha a izquierda
    # N son avenidas donde su direccion de navegacion es del sur al norte
    # C son son las intersecciones de las calles y avenidas
    # R son calles donde su direccion de navegacion es de izquierda a derecha
    # S son avenidas donde su direccion de navegacion es del norte al sur
    # ND son aquellas calles donde se puede navegar en ambas direcciones
    # L y R calles, en horas pico 2, hora normal 2
    # N y S avenidas, en horas pico 4, hora normal 1
    # C cruces, en horas pico 3, hora normal 2
    horasTotales = 0
    horasPico = 0
    filaActual = inicioSeleccionado[0]
    columnaActual = inicioSeleccionado[1]
    bucle = 0
    movimientos = buscarCaminoCorto()
    for movimiento in movimientos:
        if movimiento == 'L' or movimiento == 'R':
            horasTotales += 2
            horasPico += 2
        elif movimiento == 'N' or movimiento == 'S':
            horasTotales += 1
            horasPico += 4
        elif movimiento == 'C':
            horasTotales += 2
            horasPico += 3
        elif movimiento == 'ND':
            horasTotales += 2
            horasPico += 2
    # mensaje de la duracion aproximada del trayecto
    mb.showinfo("Información", "La duración aproximada de su trayecto es de: " + str(horasTotales) + " horas")
    return horasTotales
    """
    while filaActual != destinoSeleccionado[0] or columnaActual != destinoSeleccionado[1]:
        posicion = mapa[filaActual][columnaActual]
        if bucle == 150:
            mb.showerror("Error", "No se pudo encontrar una ruta")
            return 0
        if filaActual == destinoSeleccionado[0] and columnaActual == destinoSeleccionado[1]:
            break
        if posicion == 'L':
            columnaActual -= 1
            horasTotales += 2
            bucle += 1
        elif posicion == 'N':
            filaActual -= 1
            horasTotales += 1
            bucle += 1
        elif posicion == 'C':
            accionElegida = seleccionarCamino(filaActual, columnaActual)
            if accionElegida == 1:
                columnaActual -= 1
                horasTotales += 2
                bucle += 1
            elif accionElegida == 2:
                filaActual -= 1
                horasTotales += 2
                bucle += 1
            elif accionElegida == 3:
                columnaActual += 1
                horasTotales += 2
                bucle += 1
            elif accionElegida == 4:
                filaActual += 1
                horasTotales += 2
                bucle += 1
        elif posicion == 'R':
            columnaActual += 1
            horasTotales += 2
            bucle += 1
        elif posicion == 'S':
            filaActual += 1
            horasTotales += 1
            bucle += 1
        elif posicion == 'ND':
            accionElegida = seleccionarCamino(filaActual, columnaActual)
            if accionElegida == 1:
                columnaActual -= 1
                horasTotales += 2
                bucle += 1
            elif accionElegida == 2:
                filaActual -= 1
                horasTotales += 2
                bucle += 1
            elif accionElegida == 3:
                columnaActual += 1
                horasTotales += 2
                bucle += 1
            elif accionElegida == 4:
                filaActual += 1
                horasTotales += 2
                bucle += 1
    
    print("El tiempo total de su trayecto es de:", horasTotales, "horas")
    # mensaje de informacion con el tiempo total
    mb.showinfo("Información", "El tiempo total de su trayecto es de: " + str(horasTotales) + " horas")
    return horasTotales
    """
# buscar el camino mas corto
def buscarCaminoCorto():
    # L son calles donde su direccion de navegacion es de derecha a izquierda
    # N son avenidas donde su direccion de navegacion es del sur al norte
    # C son son las intersecciones de las calles y avenidas
    # R son calles donde su direccion de navegacion es de izquierda a derecha
    # S son avenidas donde su direccion de navegacion es del norte al sur
    # ND son aquellas calles donde se puede navegar en ambas direcciones

    filaActual = inicioSeleccionado[0]
    columnaActual = inicioSeleccionado[1]
    bucle = 0
    movimientos = []
    while filaActual != destinoSeleccionado[0] or columnaActual != destinoSeleccionado[1]:
        movimientos += [mapa[filaActual][columnaActual]]
        if bucle == 150:
            mb.showerror("Error", "No se pudo encontrar una ruta")
            return 0
        if filaActual == destinoSeleccionado[0] and columnaActual == destinoSeleccionado[1]:
            break
        if mapa[filaActual][columnaActual] == 'L':
            columnaActual -= 1
            bucle += 1
        elif mapa[filaActual][columnaActual] == 'N':
            filaActual -= 1
            bucle += 1
        elif mapa[filaActual][columnaActual] == 'C':
            accionElegida = seleccionarCamino(filaActual, columnaActual)
            if accionElegida == 1:
                columnaActual -= 1
                bucle += 1
            elif accionElegida == 2:
                filaActual -= 1
                bucle += 1
            elif accionElegida == 3:
                columnaActual += 1
                bucle += 1
            elif accionElegida == 4:
                filaActual += 1
                bucle += 1
        elif mapa[filaActual][columnaActual] == 'R':
            columnaActual += 1
            bucle += 1
        elif mapa[filaActual][columnaActual] == 'S':
            filaActual += 1
            bucle += 1
        elif mapa[filaActual][columnaActual] == 'ND':
            accionElegida = seleccionarCamino(filaActual, columnaActual)
            if accionElegida == 1:
                columnaActual -= 1
                bucle += 1
            elif accionElegida == 2:
                filaActual -= 1
                bucle += 1
            elif accionElegida == 3:
                columnaActual += 1
                bucle += 1
            elif accionElegida == 4:
                filaActual += 1
                bucle += 1
    return movimientos
    
# selecciona si debe ir por la derecha o izquierda, arriva o abajo
def seleccionarCamino(filaActual, columnaActual):
    # 1 izquierda, 2 arriba, 3 derecha, 4 abajo
    if columnaActual > destinoSeleccionado[1]:
        if filaActual > destinoSeleccionado[0]:
            return 2
        elif filaActual < destinoSeleccionado[0]:
            return 4
        else:
            return 1
    elif columnaActual < destinoSeleccionado[1]:
        if filaActual > destinoSeleccionado[0]:
            return 2
        elif filaActual < destinoSeleccionado[0]:
            return 4
        else:
            return 3
    else:
        if filaActual > destinoSeleccionado[0]:
            return 2
        elif filaActual < destinoSeleccionado[0]:
            return 4
        else:
            return 0
##############################################################################################################

#**********************SECCION DE LOGICA DEL PROGRAMA***********************
#funcion que valida si el usuario y la contraseña son correctos
def validarUsuario(usuario, contrasena):
    datos = usuario + ";" + contrasena
    archivo = open("usuarios.txt", "r")
    usuarios = archivo.read()
    archivo.close()
    if datos not in usuarios:
        return False
    else:
        return True

#funcion que retorna la cantidad de letras de un texto
def contarLetras(texto):
    contador = 0
    for letra in texto:
        contador += 1
    return contador

#lectura de archivo csv
def cargarMapa(nombreMapa):
    # guardo el nombre del mapa
    global nombreMapaSeleccionado
    nombreMapaSeleccionado = nombreMapa
    archivo = open(nombreMapa)
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

#funcion que retorna la cantidad de filas de un mapa
def contarFilas(mapa):
    contador = 0
    for fila in mapa:
        contador += 1
    return contador

#funcion que retorna la cantidad de columnas de un mapa
def totalColumnas(mapa):
    columnaTotal = 0
    for columna in mapa[0]:
        columnaTotal += 1
    return columnaTotal
#----------------------FIN DE LA SECCION DE LOGICA DEL PROGRAMA----------------------

#inicio del programa
ventanaAutenticacion()