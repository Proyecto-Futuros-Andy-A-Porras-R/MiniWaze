import tkinter as tk
from tkinter import messagebox as mb, filedialog as fd, ttk
import csv
import time
    
global inicioSeleccionado
inicioSeleccionado = [-1,-1]
global destinoSeleccionado
destinoSeleccionado = [-1,-1]
global nuevoMapa
nuevoMapa = []
global rutas
rutas = []
global nombreMapaActual
nombreMapaActual = ""
#--------------------VENTANA AUTENTICACION---------------------
#ventana principal del programa
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

# seccion de registro de usuario
def registrarse(labelNoCuenta, botonIngresar, botonRegistrarse, entryUsuario, entryContrasena):
    # limpia los entrys
    entryUsuario.delete(0, tk.END)
    entryContrasena.delete(0, tk.END)
    botonIngresar.pack_forget()
    # cambia el texto del label
    labelNoCuenta.config(text="Ingresa tus datos y registrate")
    # cambia la funcion del boton de registrarse
    botonRegistrarse.config(text="Registrarse", command=lambda: registrarUsuarioInterfaz(entryUsuario.get(), entryContrasena.get()))

# funcion para registrar usuario
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

# valida que el usuario y la contraseña sean correctos
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
#despliega la ventana principal
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

#uso de filedialog para cargar el mapa
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
    global botonesPrincipales
    #limpia el frame izquierdo
    for widget in frameIzquierdo.winfo_children():
        widget.destroy()    

    #limpia el frame derecho
    for widget in frameDerecho.winfo_children():
        if widget.cget("bg") == "red" or widget.cget("bg") == "green" or widget.cget("bg") == "purple":
            widget.config(bg="white", fg="black")
            
    #seleccionar destino
    botonSeleccionarDestino = tk.Button(frameIzquierdo, text="Seleccionar destino", font=("Helvetica", 10, "bold"), command=lambda: seleccionarRuta())
    botonSeleccionarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonSeleccionarDestino.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    botonesPrincipales += [botonSeleccionarDestino]
    #planificar destino
    botonPlanificarDestino = tk.Button(frameIzquierdo, text="Planificar destino", font=("Helvetica", 10, "bold"), command=lambda: planificarDestino())
    botonPlanificarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonPlanificarDestino.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    botonesPrincipales += [botonPlanificarDestino]
    #guardar destino
    botonGuardarDestino = tk.Button(frameIzquierdo, text="Guardar destino", font=("Helvetica", 10, "bold"), command=lambda: guardarDestino())
    botonGuardarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonGuardarDestino.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    botonesPrincipales += [botonGuardarDestino]
    #borrar destino
    botonBorrarDestino = tk.Button(frameIzquierdo, text="Borrar destino", font=("Helvetica", 10, "bold"), command=lambda: borrarDestino())
    botonBorrarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonBorrarDestino.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    botonesPrincipales += [botonBorrarDestino]
    #modificar mapa
    botonModificarMapa = tk.Button(frameIzquierdo, text="Modificar mapa", font=("Helvetica", 10, "bold"), command=lambda: modificarMapa())
    botonModificarMapa.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonModificarMapa.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    botonesPrincipales += [botonModificarMapa]
    #boton salir
    botonSalir = tk.Button(frameIzquierdo, text="Salir", font=("Helvetica", 10, "bold"), command=lambda: ventanaPrincipal.destroy())
    botonSalir.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonSalir.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)

##########################################################################################
# funcion para modificar el mapa
def modificarMapa():
# validamos que se haya cargado un mapa
    if mapa == [] and nuevoMapa == []:
        mb.showerror("Error", "Primero cargue un mapa o cree uno")
        return 0
    # limpiar frameIzquierdo
    for widget in frameIzquierdo.winfo_children():
        widget.destroy()
    # limpiar frameDerecho
    for widget in frameDerecho.winfo_children():
        widget.destroy()
    # limpiar botones
    botones = []
    # limpiar variables globales
    inicioSeleccionado[0] = inicioSeleccionado[1] = destinoSeleccionado[0] = destinoSeleccionado[1] = -1
    # boton para guardar el mapa
    botonGuardarMapa = tk.Button(frameIzquierdo, text="Guardar mapa", font=("Helvetica", 10, "bold"), command=lambda: guardarMapa())
    botonGuardarMapa.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonGuardarMapa.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    # botones.append(botonGuardarMapa)
    # para salir de la modificacion del mapa
    botonSalir = tk.Button(frameIzquierdo, text="Salir", font=("Helvetica", 10, "bold"), command=lambda: mostrarOpciones())
    botonSalir.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonSalir.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    # llamamos a la funcion dibujarMapaExistente, para que dibuje el mapa que ya se cargo
    # pero con los botones habilitados para modificarlo, como si fuera un mapa nuevo
    dibujarMapaExistente()

# funcion para dibujar el mapa que ya se cargo, pero con los botones habilitados para modificarlo
def dibujarMapaExistente():
    mapaCopia = mapa
    filaTotal = contarFilas(mapaCopia)
    columnaTotal = contarFilas(mapaCopia[0])
    global nuevoMapa
    nuevoMapa = []
    for fila in range(filaTotal):
        filas = []
        for columna in range(columnaTotal):
            # saco el valor actual de la posicion actual
            valor = mapaCopia[fila][columna]
            # si es un 0 lo que hay en la posicion actual, se muestra el boton negro
            if valor == "0":
                boton = tk.Button(frameDerecho, text="0",font=("Arial",12), width=1, height=1, bg="black", fg="white", command=lambda fila=fila, columna=columna: cambiarColor(fila, columna))
                boton.grid(row=fila,column=columna)
                filas += [boton]
            # en cualquier otro caso se muestra la letra
            elif valor == "N":
                boton = tk.Button(frameDerecho, text="N",font=("Arial",12), width=1, height=1,command=lambda fila=fila, columna=columna: cambiarColor(fila, columna))
                boton.grid(row=fila,column=columna)
                filas += [boton]
            elif valor == "R":
                boton = tk.Button(frameDerecho, text="R",font=("Arial",12), width=1, height=1,command=lambda fila=fila, columna=columna: cambiarColor(fila, columna))
                boton.grid(row=fila,column=columna)
                filas += [boton]
            elif valor == "L":
                boton = tk.Button(frameDerecho, text="L",font=("Arial",12), width=1, height=1,command=lambda fila=fila, columna=columna: cambiarColor(fila, columna))
                boton.grid(row=fila,column=columna)
                filas += [boton]
            elif valor == "S":
                boton = tk.Button(frameDerecho, text="S",font=("Arial",12), width=1, height=1,command=lambda fila=fila, columna=columna: cambiarColor(fila, columna))
                boton.grid(row=fila,column=columna)
                filas += [boton]
            elif valor == "C":
                boton = tk.Button(frameDerecho, text="C",font=("Arial",12), width=1, height=1,command=lambda fila=fila, columna=columna: cambiarColor(fila, columna))
                boton.grid(row=fila,column=columna)
                filas += [boton]
            elif valor == "ND":
                boton = tk.Button(frameDerecho, text="ND",font=("Arial",12), width=1, height=1,command=lambda fila=fila, columna=columna: cambiarColor(fila, columna))
                boton.grid(row=fila,column=columna)
                filas += [boton]
        nuevoMapa += [filas]

##########################################################################################

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
    filaTotal = contarFilas(mapa)
    columnaTotal = totalColumnas(mapa)
    #limpiar frame derecho
    for widget in frameDerecho.winfo_children():
        widget.destroy()
    mostrarOpciones()

    global botones #lista de botones del mapa
    botones = []
    for fila in range(filaTotal):
        filaBotones = []
        for columna in range(columnaTotal):
            if mapa[fila][columna] == '0':
                boton = tk.Button(frameDerecho, text="",font=("Arial", 12), width=1, height=1, bg="black", fg="black", command=lambda fila=fila, columna=columna: seleccionarBoton(fila, columna))
                boton.grid(row=fila, column=columna)
                filaBotones += [boton]
            else:
                symbol = mapa[fila][columna]
                if fila == inicioSeleccionado[0] and columna == inicioSeleccionado[1]:
                    boton = tk.Button(frameDerecho, text=symbol, font=("Arial", 12), width=1, height=1, bg="green", fg="green", command=lambda fila=fila, columna=columna: seleccionarBoton(fila, columna))
                    boton.grid(row=fila, column=columna)
                    filaBotones += [boton]
                    continue
                elif fila == destinoSeleccionado[0] and columna == destinoSeleccionado[1]:
                    boton = tk.Button(frameDerecho, text=symbol, font=("Arial", 12), width=1, height=1, bg="red", fg="red", command=lambda fila=fila, columna=columna: seleccionarBoton(fila, columna))
                    boton.grid(row=fila, column=columna)
                    filaBotones += [boton]
                    continue
                boton = tk.Button(frameDerecho, text=symbol, font=("Arial", 12), width=1, height=1, bg="white", fg="black", command=lambda fila=fila, columna=columna: seleccionarBoton(fila, columna))
                boton.grid(row=fila, column=columna)
                filaBotones += [boton]
        botones += [filaBotones]
    bloquearMapa()
    #mostrar nombre del mapa en la parte inferior
    nombre = archivo[pos(archivo, '/')+1:pos(archivo, '.')]
    global nombreMapaActual
    nombreMapaActual = nombre
    labelNombreMapa = tk.Label(frameDerecho, text=nombre, font=("Arial", 12, "bold"))
    labelNombreMapa.grid(row=filaTotal+1, column=0, columnspan=columnaTotal)
    cargarDestinos(nombreMapaActual)

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
    botonVolver = tk.Button(frameIzquierdo, text="Volver", command=mostrarOpciones, font=("Arial", 7), height=1, bg="white", fg="black")
    botonVolver.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

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
            filas += [boton]
        nuevoMapa += [filas]

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

# borra uno de los destinos registrados para un mapa
def borrarDestino():
    if (contarFilas(rutas))==0:
        mb.showerror("Error", "No hay destinos registrados")
        return 0
    #obtiene el nombre del mapa
    nombre = ""
    for widget in frameDerecho.winfo_children():
        if isinstance(widget, tk.Label):
            nombre = widget.cget("text")

    #limpiar el frameIzquierdo
    for widget in frameIzquierdo.winfo_children():
        widget.destroy()

    #repintar a blanco los botones en rojo verde o morado
    for widget in frameDerecho.winfo_children():
        if widget.cget("bg") == "red" or widget.cget("bg") == "green" or widget.cget("bg") == "purple":
            widget.config(bg="white", fg="black")
    
    #sacar la informacion del archivo txt con el camino
    cargarDestinos(nombre)
    #crear un combobox con los destinos
    labelDestino = tk.Label(frameIzquierdo, text="Destino: ", font=("Arial", 12))
    labelDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    comboDestino = ttk.Combobox(frameIzquierdo, state="readonly", font=("Arial", 12), width=5)
    comboDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    lista = []
    for i in range(contarFilas(rutas)):
        lista += ["Ruta " + str(i+1)]
    comboDestino['values'] = tuple(lista)
    comboDestino.current(0)

    #boton para mostrar el recorrido
    botonMostrarRecorrido = tk.Button(frameIzquierdo, text="Mostrar recorrido", command=lambda: pintarTrayecto(rutas[comboDestino.current()]), font=("Arial", 12), height=1, bg="white", fg="black")
    botonMostrarRecorrido.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    #boton para borrar el destino
    botonBorrarDestino = tk.Button(frameIzquierdo, text="Borrar destino", command=lambda: borrarArchivo(comboDestino.current(), nombre), font=("Arial", 12), height=1, bg="white", fg="black")
    botonBorrarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    #boton para volver a la pantalla de opciones
    botonVolver = tk.Button(frameIzquierdo, text="Volver", command=mostrarOpciones, font=("Arial", 12), height=1, bg="white", fg="black")
    botonVolver.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

def borrarArchivo(destino, nombre):
    global rutas
    #borrar la ruta de la lista
    i = 0
    nuevaRuta = []
    for ruta in rutas:
        if i != destino:
            nuevaRuta += [ruta]
        i += 1
    rutas = nuevaRuta

    #borrar el archivo
    import os
    os.remove(nombre+str(destino)+".txt")
    mb.showinfo("Informacion", "Destino borrado con exito")
    mostrarOpciones()

def planificarDestino():
    cargarDestinos(nombreMapaActual)
    if (contarFilas(rutas))==0:
        mb.showerror("Error", "No hay destinos registrados")
        return 0
    #obtiene el nombre del mapa
    nombre = ""
    for widget in frameDerecho.winfo_children():
        if isinstance(widget, tk.Label):
            nombre = widget.cget("text")

    #limpiar el frameIzquierdo
    for widget in frameIzquierdo.winfo_children():
        widget.destroy()

    #repintar a blanco los botones en rojo verde o morado
    for widget in frameDerecho.winfo_children():
        if widget.cget("bg") == "red" or widget.cget("bg") == "green" or widget.cget("bg") == "purple":
            widget.config(bg="white", fg="black")
    
    #sacar la informacion del archivo txt con el camino
    # cargarDestinos(nombre)
    #crear un combobox con los destinos
    labelDestino = tk.Label(frameIzquierdo, text="Destino: ", font=("Arial", 12))
    labelDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    comboDestino = ttk.Combobox(frameIzquierdo, state="readonly", font=("Arial", 12), width=5)
    comboDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    lista = []
    for i in range(contarFilas(rutas)):
        lista += ["Ruta " + str(i+1)]
    comboDestino['values'] = tuple(lista)
    comboDestino.current(0)

    #boton para mostrar el recorrido
    botonMostrarRecorrido = tk.Button(frameIzquierdo, text="Mostrar recorrido", command=lambda: pintarTrayecto(rutas[comboDestino.current()]), font=("Arial", 12), height=1, bg="white", fg="black")
    botonMostrarRecorrido.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    # entry para la hora de salida
    labelHoraSalida = tk.Label(frameIzquierdo, text="Hora de salida: ", font=("Arial", 12))
    labelHoraSalida.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    entryHoraSalida = tk.Entry(frameIzquierdo, font=("Arial", 12))
    entryHoraSalida.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    
    #boton para calcular la hora de llegada
    botonCalcularHoraLlegada = tk.Button(frameIzquierdo, text="Calcular hora de llegada", command=lambda: calcularHoraLlegada(rutas[comboDestino.current()],entryHoraSalida.get()), font=("Arial", 12), height=1, bg="white", fg="black")
    botonCalcularHoraLlegada.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    #boton para volver a la pantalla de opciones
    botonVolver = tk.Button(frameIzquierdo, text="Volver", command=mostrarOpciones, font=("Arial", 12), height=1, bg="white", fg="black")
    botonVolver.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

# funcion que calcula la hora de llegada
# segun la ruta y la hora de salida
# retriccion: la hora de salida debe ser en formato hh:mm
# R: si la hora de salida no es valida, muestra un error diciendo que la hora de salida no es valida
def calcularHoraLlegada(ruta, horaSalida):
    # validar que la hora de salida sea valida
    if validarHora(horaSalida) == False:
        mb.showerror("Error", "La hora de salida no es valida")
        return 0
    # obtener la hora de salida
    hora = int(horaSalida[:2])
    minutos = int(horaSalida[3:])
    # obtener la duracion de la ruta
    duracion, duracionPico = calcularDuracion(ruta)
    # sumar la duracion a los minutos
    duracion = calculoHora(hora, minutos+duracion)
    duracionPico = calculoHora(hora, minutos+duracionPico)
    # mostrar la hora de llegada
    mb.showinfo("Hora de llegada", "Hora de llegada: "+duracion+"\nHora de llegada en hora pico: "+duracionPico)

# funcion para que la hora tenga el formato hh:mm
# restriccion: la hora debe ser un numero entero
# R: retorna la hora con el formato hh:mm
def calculoHora(hora, minutos):
    if minutos >= 60:
        hora += 1
        minutos -= 60
    if hora >= 24:
        hora -= 24
    if hora < 10:
        hora = "0"+str(hora)
    if minutos < 10:
        minutos = "0"+str(minutos)
    return str(hora)+":"+str(minutos)
# funcion que calcula la duracion de una ruta
# restriccion: la ruta debe ser una lista de listas
# R: retorna la duracion de la ruta
def calcularDuracion(ruta):
    tiempo = 0
    tiempoPico = 0
    for movimiento in ruta[:-2]:
        print(movimiento, mapa[movimiento[0]][movimiento[1]])
        if mapa[movimiento[0]][movimiento[1]] == "C":
            tiempo += 2
            tiempoPico += 3
        elif mapa[movimiento[0]][movimiento[1]] == "N" or mapa[movimiento[0]][movimiento[1]] == "S":
            tiempo += 1
            tiempoPico += 4
        elif mapa[movimiento[0]][movimiento[1]] == "R" or mapa[movimiento[0]][movimiento[1]] == "L":
            tiempo += 2
            tiempoPico += 2
    return tiempo, tiempoPico


# funcion que valida que la hora sea valida
# restriccion: la hora debe ser en formato hh:mm    
# R: si la hora es valida retorna True, si no retorna False
def validarHora(hora):
    # validar que la hora sea en formato hh:mm
    if contarCaracteres(hora) == 5:
        for i in range(5):
            if i == 2:
                if hora[i] != ":":
                    return False
            else:
                for j in range(10):
                    if hora[i] == str(j):
                        break
                    elif j > 2 and i == 0:
                        return False
                    elif j > 5 and i == 3:
                        return False
    else:
        return False
    return True



#**********************SECCION DE LOGICA DEL PROGRAMA***********************
#guarda el mapa creado en un archivo csv
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
    nombreMapaActual = archivo.name
    cargarMapaInterfaz(archivo.name)
    cargarDestinos(nombreMapaActual)

#funcion para guardar el trayecto de destino en un archivo txt
def guardarDestino():
    global rutas
    if rutas == []:
        mb.showerror("Error", "Primero seleccione un destino")
        return 0
    # toma las coordenadas del camino y los guarda en un archivo con el nombre del mapa
    i = 0
    for ruta in rutas:
        guardado(ruta, i)
        i += 1
    mb.showinfo("Información", "Ruta(s) guardada(s) con éxito")

# guarda las diferentes rutas en archivos txt con el nombre del mapa y un numero
# E: lista: lista de coordenadas, i: numero de ruta
def guardado(lista, i):
    nombre = ""
    for widget in frameDerecho.winfo_children():
        if isinstance(widget, tk.Label):
            nombre = widget.cget("text")
    archivo = open(nombre+str(i)+".txt", "w")
    contenido = ""
    for coordenada in lista:
        contenido += (str(coordenada[0])+","+str(coordenada[1])+"\n")
    #quitar el ultimo salto de linea
    contenido = contenido[:-1]
    archivo.write(contenido)
    archivo.close()
    
# carga todos los destinos guardados en el mapa
# E: nombre: nombre del mapa
# S: guarda los destinos en la variable global rutas
def cargarDestinos(nombre):
    i = 0
    global rutas
    rutas = []
    while True:
        archivo = None
        try:
            archivo = open(nombre+str(i)+".txt", "r")
        except:
            break
        contenido= []
        linea = archivo.readline()
        while linea:
            if(linea[-1]=="\n"):
                linea = linea[:-1]
            linea = separar(linea, ",")
            coord = [int(linea[0]), int(linea[1])]      
            contenido += [coord]
            linea = archivo.readline()
        archivo.close()
        rutas += [contenido]
        i += 1 

# muestra el recorrido en el mapa, y las horas pico
def pintarTrayecto(contenido):
    # decolorar el mapa
    for widget in frameDerecho.winfo_children():
        if isinstance(widget, tk.Button):
            if widget["bg"] == "purple" or widget["bg"] == "green" or widget["bg"] == "red":
                widget.config(bg="white", fg="black")
    contenido = contenido
    for coordenada in contenido:
        boton = botones[coordenada[0]][coordenada[1]]
        # si es el inicio, se pinta de verde
        if coordenada == contenido[0]:
            boton.config(bg="green", fg="white")
        # si es el destino, se pinta de rojo
        elif coordenada == contenido[-1]:
            boton.config(bg="red", fg="white")
        # el resto se pinta de morado
        else:
            boton.config(bg="purple", fg="white")
        frameDerecho.update()
        time.sleep(0.1)
    
    horas = contenido[-1] # las horas estan en la ultima posicion
    #mostrar en la interfaz
    labelHoras = tk.Label(frameDerecho, text="Duracion en tiempo normal: "+str(horas[0])+" minutos", font=("Arial", 12), bg="white", fg="black")
    labelHoras.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    labelHorasPico = tk.Label(frameDerecho, text="Duracion en hora pico: "+str(horas[1])+" minutos", font=("Arial", 12), bg="white", fg="black")
    labelHorasPico.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
#--------------FUNCIONES DE SELECCION DE RUTA------------------
# habilita los botones del mapa para que se seleccione el inicio
def seleccionarInicio():
    decolorar(0)
    for fila in botones:
        for boton in fila:
            if boton["bg"] == "purple":
                boton.config(bg="white", fg="black")
    inicioSeleccionado[0] = inicioSeleccionado[1] = -1
    mb.showinfo("Información", "Seleccione el punto de inicio\n cuando se seleccione, se tornará verde")
    habilitarMapa()

# habilita los botones del mapa para que se seleccione el destino
def seleccionarDestino():
    if inicioSeleccionado[0] == -1 and inicioSeleccionado[1] == -1:
        mb.showerror("Error", "Seleccione el punto de inicio primero")
        return 0
    decolorar(1)
    for fila in botones:
        for boton in fila:
            if boton["bg"] == "purple":
                boton.config(bg="white", fg="black")
    destinoSeleccionado[0] = destinoSeleccionado[1] = -1
    mb.showinfo("Información", "Seleccione el punto de destino\n cuando se seleccione, se tornará rojo")
    habilitarMapa()

#toma el mapa y lo convierte en una matriz de ceros, si hay un obstaculo, se pone una x
def matrizCeros():
    matriz = []
    for i in range(contarFilas(mapa)):
        lista = []
        for j in range(totalColumnas(mapa)):
            if mapa[i][j] == '0':
                lista += ['X']
            else:
                lista += [0]
        matriz += [lista]
    return matriz

#calcula la ruta entre un punto de inicio y un punto de destino
def calcularRuta():
    if inicioSeleccionado[0] == -1 and inicioSeleccionado[1] == -1 or destinoSeleccionado[0] == -1 and destinoSeleccionado[1] == -1:
        mb.showerror("Error", "Seleccione el punto de inicio y destino primero")
        return 0
    decolorar(2)
    for fila in botones:
        for boton in fila:
            if boton["bg"] == "purple":
                boton.config(bg="white", fg="black")
    horasTotales = 0
    horasPico = 0
    filaActual = inicioSeleccionado[0]
    columnaActual = inicioSeleccionado[1]
    bucle = 0
    camino = []
    matrizCamino = matrizCeros()
    #imprimir coordenadas de inicio y destino
    while filaActual != destinoSeleccionado[0] or columnaActual != destinoSeleccionado[1]:
        posicion=""
        #comprobar si quien le precede es una posicion en la que se puede ir (que no salga de los limites del mapa)
        try:
            posicion = mapa[filaActual][columnaActual]
            if posicion == 'N':
                arriba = matrizCamino[filaActual - 1][columnaActual]
            if posicion == 'S':
                abajo = matrizCamino[filaActual + 1][columnaActual]
            if posicion == 'L':
                izquierda = matrizCamino[filaActual][columnaActual - 1]
            if posicion == 'R':
                derecha = matrizCamino[filaActual][columnaActual + 1]
            if posicion == 'C' or posicion == 'ND':
                arriba = matrizCamino[filaActual - 1][columnaActual]
                abajo = matrizCamino[filaActual + 1][columnaActual]
                izquierda = matrizCamino[filaActual][columnaActual - 1]
                derecha = matrizCamino[filaActual][columnaActual + 1]
        except:
            bucle = contarFilas(mapa)*totalColumnas(mapa)
        #ir pintando el camino en la matriz de botones
        botones[filaActual][columnaActual].config(bg="purple", fg="white")
        frameDerecho.update()
        time.sleep(0.1)
        # si se demora mucho en encontrar una ruta, se detiene
        if bucle == contarFilas(mapa)*totalColumnas(mapa):
            mb.showerror("Error", "No se pudo encontrar una ruta")
            return 0
        # si llego al destino, se detiene
        if [filaActual, columnaActual] == destinoSeleccionado:
            camino += [[filaActual, columnaActual]]
            break
        #CONDICION IMPORTANTE: solo avanzara si el que le sigue es igual o es C o ND
        if posicion == 'L':
            if mapa[filaActual][columnaActual - 1] not in ['L', 'C', 'ND']:
                bucle = contarFilas(mapa)*totalColumnas(mapa)
            else:
                matrizCamino[filaActual][columnaActual] = 1
                camino += [[filaActual, columnaActual]]
                columnaActual -= 1
                horasTotales += 2
                horasPico += 2
                bucle += 1
        elif posicion == 'N':
            if mapa[filaActual - 1][columnaActual] not in ['N', 'C', 'ND']:
                bucle = contarFilas(mapa)*totalColumnas(mapa)
            else:
                matrizCamino[filaActual][columnaActual] = 1
                camino += [[filaActual, columnaActual]]
                filaActual -= 1
                horasTotales += 1
                horasPico += 4
                bucle += 1
        elif posicion == 'R':
            if mapa[filaActual][columnaActual + 1] not in ['R', 'C', 'ND']:
                bucle = contarFilas(mapa)*totalColumnas(mapa)
            else:
                matrizCamino[filaActual][columnaActual] = 1
                camino += [[filaActual, columnaActual]]
                columnaActual += 1
                horasTotales += 2
                horasPico += 2
                bucle += 1
        elif posicion == 'S':
            if mapa[filaActual + 1][columnaActual] not in ['S', 'C', 'ND']:
                bucle = contarFilas(mapa)*totalColumnas(mapa)
            else:
                matrizCamino[filaActual][columnaActual] = 1
                camino += [[filaActual, columnaActual]]
                filaActual += 1
                horasTotales += 1
                horasPico += 4
                bucle += 1
        elif posicion == 'C' or posicion == 'ND':
            """
            no sube si arriba es un obstaculo o S
            no baja si abajo es un obstaculo o N
            no avanza a la derecha si a la derecha es un obstaculo o L
            no avanza a la izquierda si a la izquierda es un obstaculo o R
            """
            hayPaso = [True, True, True, True] #arriba, abajo, derecha, izquierda
            if mapa[filaActual - 1][columnaActual] in ['0', 'S'] or matrizCamino[filaActual - 1][columnaActual] == 1:
                hayPaso[0] = False
            if mapa[filaActual + 1][columnaActual] in ['0', 'N'] or matrizCamino[filaActual + 1][columnaActual] == 1:
                hayPaso[1] = False
            if mapa[filaActual][columnaActual + 1] in ['0', 'L'] or matrizCamino[filaActual][columnaActual + 1] == 1:
                hayPaso[2] = False
            if mapa[filaActual][columnaActual - 1] in ['0', 'R'] or matrizCamino[filaActual][columnaActual - 1] == 1:
                hayPaso[3] = False
            
            irPor=posiblesCaminos(hayPaso, filaActual, columnaActual)
            if (irPor == 1):
                #va hacia arriba
                matrizCamino[filaActual][columnaActual] = 1
                camino += [[filaActual, columnaActual]]
                filaActual -= 1
                horasTotales += 2
                horasPico += 3
                bucle += 1
            elif (irPor == 2):    
                #va hacia abajo
                matrizCamino[filaActual][columnaActual] = 1
                camino += [[filaActual, columnaActual]]
                filaActual += 1
                horasTotales += 2
                horasPico += 3
                bucle += 1
            elif (irPor == 3):
                #va hacia la derecha
                matrizCamino[filaActual][columnaActual] = 1
                camino += [[filaActual, columnaActual]]
                columnaActual += 1
                horasTotales += 2
                horasPico += 3
                bucle += 1
            elif (irPor == 4):
                #va hacia la izquierda
                matrizCamino[filaActual][columnaActual] = 1
                camino += [[filaActual, columnaActual]]
                columnaActual -= 1
                horasTotales += 2
                horasPico += 3
                bucle += 1
            else:
                bucle = contarFilas(mapa)*totalColumnas(mapa)
    
    botones[filaActual][columnaActual].config(bg="green")
    # mensaje de informacion con el tiempo total
    mb.showinfo("Información", "El tiempo total de su trayecto es de: " + str(horasTotales) + " minutos\nEl tiempo total de su trayecto en horas pico es de: " + str(horasPico) + " minutos")
    camino += [[horasTotales, horasPico]]

    #agregar el camino a la lista de rutas
    # si el camino ya existe, no lo agrega
    global rutas
    if camino not in rutas:
        rutas += [camino]
    return 0

"""
 dirige el camino si hay mas de una opcion
 E: un arreglo con las posibilidades de caminos, la fila y columna actual
 S: un numero que indica la direccion a tomar
 1 arriba, 2 abajo, 3 derecha, 4 izquierda, 0 sin paso
"""
def posiblesCaminos(posibilidad, filaActual, columnaActual): 
    if posibilidad == [False, False, False, False]:
        return 0
    else:
        #si el objetivo esta en direccion noreste
        if filaActual > destinoSeleccionado[0] and columnaActual < destinoSeleccionado[1]: 
            if posibilidad[0]: # si hay paso arriba
                return 1
            elif posibilidad[2]: # si hay paso derecha
                return 3
            elif posibilidad[1]: # si hay paso abajo
                return 2
            else: # sino
                return 4
        #si el objetivo esta en direccion noroeste
        elif filaActual > destinoSeleccionado[0] and columnaActual > destinoSeleccionado[1]:
            if posibilidad[0]: # si hay paso arriba
                return 1
            elif posibilidad[3]: # si hay paso izquierda
                return 4
            elif posibilidad[1]: # si hay paso abajo
                return 2
            else: # sino
                return 3 
        #si el objetivo esta en direccion sureste
        elif filaActual < destinoSeleccionado[0] and columnaActual < destinoSeleccionado[1]:
            if posibilidad[1]: # si hay paso abajo
                return 2
            elif posibilidad[2]: # si hay paso derecha
                return 3
            elif posibilidad[0]: # si hay paso arriba
                return 1
            else: # sino    
                return 4
        #si el objetivo esta en direccion suroeste
        elif filaActual < destinoSeleccionado[0] and columnaActual > destinoSeleccionado[1]:
            if posibilidad[1]: # si hay paso abajo
                return 2
            elif posibilidad[3]: # si hay paso izquierda
                return 4
            elif posibilidad[0]: # si hay paso arriba
                return 1
            else: # sino
                return 3
        # si lo tiene a la derecha
        elif filaActual == destinoSeleccionado[0] and columnaActual < destinoSeleccionado[1]:
            if posibilidad[2]: # si hay paso derecha  
                return 3
            elif posibilidad[0]: # si hay paso arriba
                return 1
            elif posibilidad[1]: # si hay paso abajo
                return 2
            else:
                return 4
        # si lo tiene a la izquierda
        elif filaActual == destinoSeleccionado[0] and columnaActual > destinoSeleccionado[1]:
            if posibilidad[3]: # si hay paso izquierda
                return 4
            elif posibilidad[0]: # si hay paso arriba
                return 1
            elif posibilidad[1]: # si hay paso abajo
                return 2
            else:
                return 3
        # si lo tiene arriba
        elif filaActual > destinoSeleccionado[0] and columnaActual == destinoSeleccionado[1]:
            if posibilidad[0]: # si hay paso arriba
                return 1
            elif posibilidad[2]: # si hay paso derecha
                return 3
            elif posibilidad[3]: # si hay paso izquierda
                return 4
            else:
                return 2
        # si lo tiene abajo
        elif filaActual < destinoSeleccionado[0] and columnaActual == destinoSeleccionado[1]:
            if posibilidad[1]: # si hay paso abajo
                return 2
            elif posibilidad[2]: # si hay paso derecha
                return 3
            elif posibilidad[3]: # si hay paso izquierda
                return 4
            else:
                return 1
#---------------------FUNCIONES AUXILIARES---------------------
# retorna el largo de un string
# E: un string
# S: un numero que indica el largo del string
def largoSTR(cadena):
    longitud = 0
    for i in cadena:
        longitud += 1
    return longitud

#funcion que retorna la ultima posicion de un caracter en un string
# E: un string y un caracter a buscar
# S: un numero que indica la ultima posicion del caracter en el string
def pos(cadena, caracter):
    ultima_posicion = -1  # Valor predeterminado si no se encuentra el carácter
    i = 0
    while i < largoSTR(cadena):
        if cadena[i] == caracter:
            ultima_posicion = i
        i += 1
    return ultima_posicion

# funcion que separa un string en una lista, reemplazo de split
# E: un string y un caracter, separa el string cada vez que encuentra el caracter
# S: una lista con los strings separados
def separar(cadena, caracter):
    lista = []
    elemento = ""
    for letra in cadena:
        if letra != caracter:
            elemento += letra
        else:
            lista += [elemento]
            elemento = ""
    lista += [elemento]
    return lista

#funcion que valida si el usuario y la contraseña son correctos
# E: un usuario y una contraseña
# S: un booleano que indica si el usuario y la contraseña son correctos
def validarUsuario(usuario, contrasena):
    datos = usuario + ";" + contrasena
    archivo = open("usuarios.txt", "r")
    usuarios = archivo.read()
    archivo.close()
    if datos not in usuarios:
        return False
    else:
        return True

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
# funcion que retorna la cantidad de carateres de un string
def contarCaracteres(string):
    contador = 0
    for caracter in string:
        contador += 1
    return contador
#----------------------FIN DE LA SECCION DE LOGICA DEL PROGRAMA----------------------
#inicio del programa
ventanaAutenticacion()