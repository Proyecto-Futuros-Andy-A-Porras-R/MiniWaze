import tkinter as tk
from tkinter import messagebox as mb, filedialog as fd
import csv
    
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
    menuArchivo.add_separator()
    menuArchivo.add_command(label="Salir", command=lambda: ventanaPrincipal.destroy())
    barraMenu.add_cascade(label="Archivo", menu=menuArchivo)
    #opcion ayuda
    menuAyuda = tk.Menu(barraMenu, tearoff=0)
    menuAyuda.add_command(label="Acerca de", command=lambda: mb.showinfo("Acerca de", "proyecto en construccion"))
    menuAyuda.add_command(label="Ayuda", command=lambda: mb.showinfo("Ayuda", "Para cargar un mapa, seleccione la opción de cargar archivo del menú Archivo\n\nPara cerrar sesión, seleccione la opción de cerrar sesión del menú Archivo\n\nPara salir de la aplicación, seleccione la opción de salir del menú Archivo"))
    barraMenu.add_cascade(label="Ayuda", menu=menuAyuda)
    #configuracion de la barra de menu
    ventanaPrincipal.config(menu=barraMenu)

    #creacion de los botones de opciones del menu
    #seleccionar destino, planificar destino, guardar destino, borrar destino y modificar mapa
    #todos van en el frame izquierdo, que mide la mitad del ancho de la ventana
    global frameIzquierdo
    frameIzquierdo = tk.Frame(ventanaPrincipal, width=400, height=ventanaPrincipal.winfo_height(), bg="white")
    #colocar el frame a la izquierda
    frameIzquierdo.pack(side="left", fill="both", expand=True)
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
    botonGuardarDestino = tk.Button(frameIzquierdo, text="Guardar destino", font=("Helvetica", 10, "bold"))#, command=lambda: cargarVentanaAnterior(ventanaPrincipal, ventanaGuardarDestino))
    botonGuardarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonGuardarDestino.config(cursor="hand2", bg="#008CBA", fg="white", activebackground="#00BFFF", relief=tk.FLAT)
    botonesPrincipales.append(botonGuardarDestino)
    #borrar destino
    botonBorrarDestino = tk.Button(frameIzquierdo, text="Borrar destino", font=("Helvetica", 10, "bold"))#, command=lambda: cargarVentanaAnterior(ventanaPrincipal, ventanaBorrarDestino))
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
    
    #frame derecho para el mapa
    global frameDerecho
    frameDerecho = tk.Frame(ventanaPrincipal, width=400, height=ventanaPrincipal.winfo_height(), bg="white")
    frameDerecho.pack(side="right", fill="both", expand=True)
    imagenFondo = tk.PhotoImage(file="mapa.png")
    labelFondo = tk.Label(frameDerecho, image=imagenFondo)
    labelFondo.place(x=0, y=0, relwidth=1, relheight=1)
    
    bloquearBotones()
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
# bloquea los botones de opciones del menu
def bloquearBotones():
    for boton in botonesPrincipales:
        boton.config(state=tk.DISABLED)

def habilitarBotones():
    for boton in botonesPrincipales:
        boton.config(state=tk.NORMAL)

def habilitarMapa():
    for fila in botones:
        for boton in fila:
            boton.config(state=tk.NORMAL)

def bloquearMapa():
    for fila in botones:
        for boton in fila:
            boton.config(state=tk.DISABLED)

#-----------------FUNCIONES PARA MAPA-----------------
def cargarMapaInterfaz(archivo):
    global mapa 
    mapa = cargarMapa(archivo)
    global inicioSeleccionado
    inicioSeleccionado = [-1,-1]
    global destinoSeleccionado
    destinoSeleccionado = [-1,-1]
    copiaMapa = mapa
    filaTotal = contarFilas(copiaMapa)
    columnaTotal = totalColumnas(copiaMapa)
    habilitarBotones()
    #limpiar frame derecho
    for widget in frameDerecho.winfo_children():
        widget.destroy()

    for widget in frameIzquierdo.winfo_children():
        if widget.cget("text") == "Seleccionar punto de inicio" or widget.cget("text") == "Seleccionar punto de destino" or widget.cget("text") == "Calcular ruta" or widget.cget("text") == "Confirmar ruta":
            widget.destroy()

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

# reinicia los colores de los botones al color original (blanco)
# E: colores= entero positivo donde False es decolorar solo el inicio y True es ambos (inicio y destino)
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
    bloquearBotones()
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
    #desaparece los botontes de seleccionar ruta
    for widget in frameIzquierdo.winfo_children():
        if widget.cget("text") == "Seleccionar punto de inicio" or widget.cget("text") == "Seleccionar punto de destino" or widget.cget("text") == "Calcular ruta" or widget.cget("text") == "Confirmar ruta":
            widget.destroy()
    habilitarBotones()
    bloquearMapa()
    decolorar(2)

# funcion a la que responden los botones que conforman el mapa
# E: a= fila del boton, b= columna del boton
# S: cambia el color del boton seleccionado
# R: el boton no debe ser de otro color que no sea blanco
def seleccionarBoton(a,b):
    boton1 = botones[a][b]
    if(boton1.cget("bg") == "black" or boton1.cget("bg") == "red" or boton1.cget("bg") == "green"):
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

#--------------FUNCIONES DE SELECCION DE RUTA------------------
def seleccionarInicio():
    inicioSeleccionado[0] = -1
    inicioSeleccionado[1] = -1
    decolorar(0)
    mb.showinfo("Información", "Seleccione el punto de inicio\n cuando se seleccione, se tornará verde")
    habilitarMapa()

def seleccionarDestino():
    if inicioSeleccionado[0] == -1 and inicioSeleccionado[1] == -1:
        mb.showerror("Error", "Seleccione el punto de inicio")
        return 0
    
    destinoSeleccionado[0] = -1
    destinoSeleccionado[1] = -1
    decolorar(1)
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
    filaActual = inicioSeleccionado[0]
    columnaActual = inicioSeleccionado[1]
    while filaActual != destinoSeleccionado[0] or columnaActual != destinoSeleccionado[1]:
        if filaActual == destinoSeleccionado[0] and columnaActual == destinoSeleccionado[1]:
            break
        if mapa[filaActual][columnaActual] == 'L':
            columnaActual -= 1
            horasTotales += 2
        elif mapa[filaActual][columnaActual] == 'N':
            filaActual -= 1
            horasTotales += 4
        elif mapa[filaActual][columnaActual] == 'C':
            accionElegida = seleccionarCamino(filaActual, columnaActual)
            if accionElegida == 1:
                columnaActual -= 1
                horasTotales += 2
            elif accionElegida == 2:
                filaActual -= 1
                horasTotales += 2
            elif accionElegida == 3:
                columnaActual += 1
                horasTotales += 2
            elif accionElegida == 4:
                filaActual += 1
                horasTotales += 2
        elif mapa[filaActual][columnaActual] == 'R':
            columnaActual += 1
            horasTotales += 2
        elif mapa[filaActual][columnaActual] == 'S':
            filaActual += 1
            horasTotales += 4
        elif mapa[filaActual][columnaActual] == 'ND':
            accionElegida = seleccionarCamino(filaActual, columnaActual)
            if accionElegida == 1:
                columnaActual -= 1
                horasTotales += 2
            elif accionElegida == 2:
                filaActual -= 1
                horasTotales += 2
            elif accionElegida == 3:
                columnaActual += 1
                horasTotales += 2
            elif accionElegida == 4:
                filaActual += 1
                horasTotales += 2
    print("El tiempo total de su trayecto es de:", horasTotales, "horas")
    return horasTotales
# selecciona si debe ir por la derecha o izquierda, arriva o abajo
def seleccionarCamino(filaActual, columnaActual):
    # se usa la variable global mapa
    # se usa la variable global destinoSeleccionado
    # para saber si el destino esta a la derecha o izquierda
    if destinoSeleccionado[1] > columnaActual:
        # si el destino esta a la derecha
        # se debe ir por la derecha
        # se valida que no se salga del mapa y que no se choque con un edificio
        if columnaActual + 1 < totalColumnas(mapa) and mapa[filaActual][columnaActual + 1] != '0':
            return 1
        # si no se puede ir por la derecha se va por la izquierda
        elif columnaActual - 1 >= 0 and mapa[filaActual][columnaActual - 1] != '0':
            return 3
        # si no se puede ir por la derecha ni por la izquierda se va por arriba
        elif filaActual - 1 >= 0 and mapa[filaActual - 1][columnaActual] != '0':
            return 2
        # si no se puede ir por la derecha ni por la izquierda ni por arriba se va por abajo
        elif filaActual + 1 < contarFilas(mapa) and mapa[filaActual + 1][columnaActual] != '0':
            return 4
    elif destinoSeleccionado[1] < columnaActual:
        if columnaActual - 1 >= 0 and mapa[filaActual][columnaActual - 1] != '0':
            return 3
        elif columnaActual + 1 < totalColumnas(mapa) and mapa[filaActual][columnaActual + 1] != '0':
            return 1
        elif filaActual - 1 >= 0 and mapa[filaActual - 1][columnaActual] != '0':
            return 2
        elif filaActual + 1 < contarFilas(mapa) and mapa[filaActual + 1][columnaActual] != '0':
            return 4
    # para saber si el destino esta arriba o abajo
    elif destinoSeleccionado[0] > filaActual:
        # si el destino esta abajo
        # se debe ir por abajo
        # se valida que no se salga del mapa y que no se choque con un edificio
        if filaActual + 1 < contarFilas(mapa) and mapa[filaActual + 1][columnaActual] != '0':
            return 4
        # si no se puede ir por abajo se va por arriba
        elif filaActual - 1 >= 0 and mapa[filaActual - 1][columnaActual] != '0':
            return 2
        # si no se puede ir por abajo ni por arriba se va por la derecha
        elif columnaActual + 1 < totalColumnas(mapa) and mapa[filaActual][columnaActual + 1] != '0':
            return 1
        # si no se puede ir por abajo ni por arriba ni por la derecha se va por la izquierda
        elif columnaActual - 1 >= 0 and mapa[filaActual][columnaActual - 1] != '0':
            return 3
    elif destinoSeleccionado[0] < filaActual:
        if filaActual - 1 >= 0 and mapa[filaActual - 1][columnaActual] != '0':
            return 2
        elif filaActual + 1 < contarFilas(mapa) and mapa[filaActual + 1][columnaActual] != '0':
            return 4
        elif columnaActual + 1 < totalColumnas(mapa) and mapa[filaActual][columnaActual + 1] != '0':
            return 1
        elif columnaActual - 1 >= 0 and mapa[filaActual][columnaActual - 1] != '0':
            return 3
##############################################################################################################

#--------------------FUNCIONES AUXILIARES----------------------
def contarFilas(mapa):
    filaTotal = 0
    for fila in mapa:
        filaTotal += 1
    return filaTotal

def totalColumnas(mapa):
    columnaTotal = 0
    for fila in mapa:
        for columna in fila:
            columnaTotal += 1
        return columnaTotal
#--------------------------------------------------------------

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
#----------------------FIN DE LA SECCION DE LOGICA DEL PROGRAMA----------------------

#inicio del programa
ventanaAutenticacion()