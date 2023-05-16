# importar el archivo miniWaze.py
import miniWaze
import tkinter as tk

# creacion de la ventana de autenticacion
def ventanaAutenticacion():
    global ventanaAutenticacion
    ventanaAutenticacion = tk.Tk()
    ventanaAutenticacion.title("Autenticacion")
    ventanaAutenticacion.geometry("350x350")
    ventanaAutenticacion.configure(background="black")

    # creacion de los labels
    labelUsuario = tk.Label(ventanaAutenticacion, text="Usuario", bg="black", fg="white")
    labelUsuario.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    labelContrasena = tk.Label(ventanaAutenticacion, text="Contraseña", bg="black", fg="white")
    labelContrasena.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    # creacion de los entrys
    entryUsuario = tk.Entry(ventanaAutenticacion)
    entryUsuario.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    entryContrasena = tk.Entry(ventanaAutenticacion)
    entryContrasena.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    # creacion de los botones
    botonIngresar = tk.Button(ventanaAutenticacion, text="Ingresar", command=lambda: validarUsuarioInterfaz(entryUsuario.get(), entryContrasena.get()))
    botonIngresar.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonSalir = tk.Button(ventanaAutenticacion, text="Salir", command=lambda: ventanaAutenticacion.destroy())
    botonSalir.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    ventanaAutenticacion.mainloop()

# funcion que valida si el usuario y la contraseña son correctos
def validarUsuarioInterfaz(usuario, contrasena):
    if miniWaze.validarUsuario(usuario, contrasena):
        ventanaAutenticacion.destroy()
        ventanaPrincipal()
    else:
        # mensaje de error
        labelError = tk.Label(ventanaAutenticacion, text="Usuario o contraseña incorrectos", bg="black", fg="white")
        labelError.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

# creacion de la ventana principal
def ventanaPrincipal():
    global ventanaPrincipal
    ventanaPrincipal = tk.Tk()
    ventanaPrincipal.title("MiniWaze")
    ventanaPrincipal.geometry("400x400")
    ventanaPrincipal.configure(background="black")

    # creacion de los botones
    # opciones del menu principal
    # cargar mapa, seleccionar destino, planificar destino,
    # guardar destino, borrar destino, modificar mapa, salir
    botonCargarMapa = tk.Button(ventanaPrincipal, text="Cargar mapa", command=lambda: cargarMapa())
    botonCargarMapa.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonSeleccionarDestino = tk.Button(ventanaPrincipal, text="Seleccionar destino", command=lambda: seleccionarDestino())
    botonSeleccionarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonPlanificarDestino = tk.Button(ventanaPrincipal, text="Planificar destino", command=lambda: planificarDestino())
    botonPlanificarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonGuardarDestino = tk.Button(ventanaPrincipal, text="Guardar destino", command=lambda: guardarDestino())
    botonGuardarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonBorrarDestino = tk.Button(ventanaPrincipal, text="Borrar destino", command=lambda: borrarDestino())
    botonBorrarDestino.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonModificarMapa = tk.Button(ventanaPrincipal, text="Modificar mapa", command=lambda: modificarMapa())
    botonModificarMapa.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    botonSalir = tk.Button(ventanaPrincipal, text="Salir", command=lambda: ventanaPrincipal.destroy())
    botonSalir.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    ventanaPrincipal.mainloop()

# ventana para cargar el mapa
def cargarMapa():
    # se oculta la ventana principal
    ventanaPrincipal.withdraw()
    global ventanaCargarMapa
    ventanaCargarMapa = tk.Tk()
    ventanaCargarMapa.title("Cargar mapa")
    ventanaCargarMapa.geometry("600x600")
    ventanaCargarMapa.configure(background="black")

    # creacion de los labels
    labelNombreMapa = tk.Label(ventanaCargarMapa, text="Nombre del mapa", bg="black", fg="white")
    labelNombreMapa.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    # labelNombreArchivo = tk.Label(ventanaCargarMapa, text="Nombre del archivo", bg="black", fg="white")
    # labelNombreArchivo.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    # creacion de los entrys
    entryNombreMapa = tk.Entry(ventanaCargarMapa)
    entryNombreMapa.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    # entryNombreArchivo = tk.Entry(ventanaCargarMapa)
    # entryNombreArchivo.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    # creacion de los botones
    botonCargar = tk.Button(ventanaCargarMapa, text="Cargar", command=lambda: cargarMapaInterfaz(entryNombreMapa.get()))
    botonCargar.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    # el boton de salir vuelve a la ventana principal
    botonSalir = tk.Button(ventanaCargarMapa, text="Salir", command=lambda: cargarVentanaAnterior(ventanaPrincipal, ventanaCargarMapa))
    botonSalir.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    ventanaCargarMapa.mainloop()

# cargar ventana anterior
def cargarVentanaAnterior(ventanaAnterior, ventanaActual):
    if ventanaAnterior == ventanaPrincipal:
        ventanaActual.destroy()
        ventanaPrincipal.deiconify()
"""
funcion que carga el mapa en la interfaz
el mapa se carga usando usando el metodo cargarMapa de la clase MiniWaze,
esa funcion retorna una matriz con el mapa, esa matriz se recorre y se van
creando los labels que representan cada posicion del mapa
"""
def cargarMapaInterfaz(nombreMapa):
    # ventanaCargarMapa.destroy()
    global ventanaMapa # ventana que muestra el mapa
    ventanaMapa = tk.Tk()
    ventanaMapa.title(nombreMapa)
    ventanaMapa.geometry("600x600")
    ventanaMapa.configure(background="black")
    mapa = miniWaze.cargarMapa()
    filaTotal = contarFilas(mapa)
    columnaTotal = totalColumnas(mapa)
    filaActual = 0
    columnaActual = 0
    for fila in range(filaTotal):
        for columna in range(columnaTotal):
            # si es 0 es un espacio vacio
            if mapa[fila][columna] == '0':
                label = tk.Label(ventanaMapa, text=" ", bg="black", fg="white")
                label.grid(row=fila, column=columna)
            # cualquier otro caso se muestra el numero o letra
            else:
                label = tk.Label(ventanaMapa, text=mapa[fila][columna], bg="black", fg="white")
                label.grid(row=fila, column=columna)
                columnaActual = columna
        filaActual = fila
    # creacion de los botones
    botonSalir = tk.Button(ventanaMapa, text="Salir", command=lambda: ventanaMapa.destroy())
    botonSalir.grid(row=filaActual+1, column=columnaActual+1)


    ventanaMapa.mainloop()


# ventana para seleccionar el destino

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





# ejecucion de la ventana de autenticacion
ventanaAutenticacion()