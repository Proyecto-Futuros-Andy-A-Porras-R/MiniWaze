import tkinter as tk
import miniWaze
from tkinter import messagebox as mb
import csv
filaActual = None
columnaActual = None
#--------------------------------------------------------------
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
#--------------------------------------------------------------
def registrarse(labelNoCuenta, botonIngresar, botonRegistrarse, entryUsuario, entryContrasena):
    # limpia los entrys
    entryUsuario.delete(0, tk.END)
    entryContrasena.delete(0, tk.END)
    botonIngresar.pack_forget()
    # cambia el texto del label
    labelNoCuenta.config(text="Ingresa tus datos y registrate")
    # cambia la funcion del boton de registrarse
    botonRegistrarse.config(text="Registrarse", command=lambda: registrarUsuarioInterfaz(entryUsuario.get(), entryContrasena.get()))
#--------------------------------------------------------------
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
#--------------------------------------------------------------
def validarUsuarioInterfaz(usuario, contrasena):
    if miniWaze.validarUsuario(usuario, contrasena):
        ventanaAutenticacion.destroy()
        ventanaPrincipal()
        return 0
    else:
        # mensaje de error
        mb.showerror("Error", "Usuario o contraseña incorrectos")
        return 0
#--------------------------------------------------------------
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
    botonCargarMapa = tk.Button(ventanaPrincipal, text="Cargar mapa", command=lambda: cargarMapaInterfaz())
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
#--------------------------------------------------------------
# ventana para cargar el mapa
def cargarMapaInterfaz():
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
    botonCargar = tk.Button(ventanaCargarMapa, text="Cargar", command=lambda: cargarMapaInterfaz2(entryNombreMapa.get()))
    botonCargar.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
    # el boton de salir vuelve a la ventana principal
    botonSalir = tk.Button(ventanaCargarMapa, text="Salir", command=lambda: cargarVentanaAnterior(ventanaPrincipal, ventanaCargarMapa))
    botonSalir.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)

    ventanaCargarMapa.mainloop()
#--------------------------------------------------------------
# cargar ventana anterior
def cargarVentanaAnterior(ventanaAnterior, ventanaActual):
    if ventanaAnterior == ventanaPrincipal:
        ventanaActual.destroy()
        ventanaPrincipal.deiconify()
"""
b.  Crear y Cargar mapa 
Este deberá ser cargado desde un archivo de texto en formato csv, en donde por medio de 
una  representación  de  una  matriz  por  defecto  y  mínimo  (10x10),  pero  podrá  ser 
personalizada,  una  vez  definido  este  podrá  crear  las  avenidas,  cruces,  calles,  cuadras.  La 
calles  y  avenidas  tendrán  una  dirección  definida,  en  la  tabla  siguiente  se  muestra  los 
símbolos a utilizar para definir el mapa base
"""
"""
funcion que carga el mapa en la interfaz
el mapa se carga usando usando el metodo cargarMapa de la clase MiniWaze,
esa funcion retorna una matriz con el mapa, esa matriz se recorre y se van
creando los labels que representan cada posicion del mapa
"""
#--------------------------------------------------------------
def cargarMapaInterfaz2(nombreMapa):
    global ventanaMapa
    ventanaMapa = tk.Tk()
    ventanaMapa.title(nombreMapa)
    ventanaMapa.geometry("600x600")
    ventanaMapa.configure(background="white")
    global mapa 
    mapa = miniWaze.cargarMapa()
    global inicioSeleccionado
    inicioSeleccionado = [-1,-1]
    global destinoSeleccionado
    destinoSeleccionado = [-1,-1]
    copiaMapa = mapa
    filaTotal = contarFilas(copiaMapa)
    columnaTotal = totalColumnas(copiaMapa)
    mostrarMapaInterfaz(filaTotal, columnaTotal)    
    
    ventanaMapa.mainloop()

def mostrarMapaInterfaz(filaTotal, columnaTotal):
    for fila in range(filaTotal):
        for columna in range(columnaTotal):
            if mapa[fila][columna] == '0':
                label = tk.Label(ventanaMapa, text="L",font=("Arial", 12), width=1, height=1, bg="black", fg="black")
                label.grid(row=fila, column=columna)
            else:
                symbol = mapa[fila][columna]
                print(f"fila: {fila} columna: {columna}, ubicacion inicio: {inicioSeleccionado}, ubicacion destino: {destinoSeleccionado}")
                if fila == inicioSeleccionado[0] and columna == inicioSeleccionado[1]:
                    label = tk.Label(ventanaMapa, text=symbol, font=("Arial", 12), width=1, height=1, bg="green", fg="green")
                    label.grid(row=fila, column=columna)
                    continue
                elif fila == destinoSeleccionado[0] and columna == destinoSeleccionado[1]:
                    label = tk.Label(ventanaMapa, text=symbol, font=("Arial", 12), width=1, height=1, bg="red", fg="red")
                    label.grid(row=fila, column=columna)
                    continue
                label = tk.Label(ventanaMapa, text=symbol, font=("Arial", 12), width=1, height=1, bg="white", fg="black")
                label.grid(row=fila, column=columna)
                columnaActual = columna
        filaActual = fila

    botonSeleccionarInicio = tk.Button(ventanaMapa, text="Seleccionar punto de inicio", command=seleccionarInicio,font=("Arial", 7), height=1, bg="white", fg="black")
    botonSeleccionarInicio.grid(row=5, column=columnaActual+3)

    botonSeleccionarDestino = tk.Button(ventanaMapa, text="Seleccionar punto de destino", command=seleccionarDestino, font=("Arial", 7), height=1, bg="white", fg="black")
    botonSeleccionarDestino.grid(row=6, column=columnaActual+3)

    botonCalcularRuta = tk.Button(ventanaMapa, text="Calcular ruta", command=calcularRuta, font=("Arial", 7), height=1, bg="white", fg="black")
    botonCalcularRuta.grid(row=7, column=columnaActual+3)

    botonSalir = tk.Button(ventanaMapa, text="Salir", command=ventanaMapa.destroy, font=("Arial", 7), height=1, bg="white", fg="black")
    botonSalir.grid(row=8, column=columnaActual+3)

def borrarMapaInterfaz():
    for widget in ventanaMapa.winfo_children():
        widget.destroy()

#--------------------------------------------------------------
def seleccionarInicio():
    ventanaMapa.bind("<Button-1>", setInicio)
   
    

def modificarMapa(posicion,valor):
    print("posicion:",posicion, "valor:", valor, "mapa:", mapa)
    if posicion[0] < 0 or posicion[1] < 0:
        return
    if posicion[0] > contarFilas(mapa) or posicion[1] > totalColumnas(mapa):
        return
    mapa[posicion[0]][posicion[1]] = valor


#--------------------------------------------------------------
def seleccionarDestino():
    ventanaMapa.bind("<Button-1>", setDestino)

#--------------------------------------------------------------
def setInicio(event):
    x = ventanaMapa.winfo_pointerx() - ventanaMapa.winfo_rootx()
    y = ventanaMapa.winfo_pointery() - ventanaMapa.winfo_rooty()
    inicioSeleccionado1 = [y // 25, x // 15]
    print("Punto de inicio:", inicioSeleccionado1)
    # modificarMapa(inicioSeleccionado,'1')
    borrarMapaInterfaz()
    filaTotal, columnaTotal = contarFilas(mapa), totalColumnas(mapa)
    # pasar el valor de inicioSeleccionado1 a la variable global inicioSeleccionado
    inicioSeleccionado[0] = inicioSeleccionado1[0]
    inicioSeleccionado[1] = inicioSeleccionado1[1]
    mostrarMapaInterfaz(filaTotal, columnaTotal)
    ventanaMapa.unbind("<Button-1>")
    # cargarMapaInterfaz("Mapa de la Ciudad")
#--------------------------------------------------------------
def setDestino(event):
    x = ventanaMapa.winfo_pointerx() - ventanaMapa.winfo_rootx()
    y = ventanaMapa.winfo_pointery() - ventanaMapa.winfo_rooty()
    destinoSeleccionado1 = [y // 25, x // 15]
    print("Punto de destino:", destinoSeleccionado1)
    # modificarMapa(destinoSeleccionado,'2')
    borrarMapaInterfaz()
    filaTotal, columnaTotal = contarFilas(mapa), totalColumnas(mapa)
    # pasar el valor de destinoSeleccionado1 a la variable global destinoSeleccionado
    destinoSeleccionado[0] = destinoSeleccionado1[0]
    destinoSeleccionado[1] = destinoSeleccionado1[1]
    mostrarMapaInterfaz(filaTotal, columnaTotal)
    ventanaMapa.unbind("<Button-1>")
    # cargarMapaInterfaz("Mapa de la Ciudad")
#--------------------------------------------------------------
def calcularRuta():
    if inicioSeleccionado is not None and destinoSeleccionado is not None:
        # Realizar el cálculo de la ruta utilizando las coordenadas de inicio y destino seleccionadas
        # ...
        print("Punto de inicio:", inicioSeleccionado)
        print("Punto de destino:", destinoSeleccionado)
    else:
        print("Debe seleccionar un punto de inicio y un punto de destino")
#--------------------------------------------------------------
"""
c.  Seleccionar destino 
Una vez cargado el mapa, debe permitir al usuario ubicar su punto inicial y su destino en el 
mapa,  para  ello  depende  de  la  creatividad  del  programador  el  cómo  representarlo,  se  le 
recomienda el uso del mouse. 
 
La  aplicación  debe  permitir  al  usuario  insertar  una  hora,  esto  es  para  poder  calcular  la 
trayectoria ya sean en “horas pico” o fuera de ella 
 
Con los puntos de inicio y fin definido, el usuario podrá indicar al sistema que calcule la ruta 
o rutas, una vez realizado esto la aplicación le muestra la ruta de menor costo como primera 
opción, de lo contrario, el usuario puede visualizar cada una de las rutas y seleccionar el que 
más le convenga.  
"""
#--------------------------------------------------------------
def contarFilas(mapa):
    filaTotal = 0
    for fila in mapa:
        filaTotal += 1
    return filaTotal
#--------------------------------------------------------------
def totalColumnas(mapa):
    columnaTotal = 0
    for fila in mapa:
        for columna in fila:
            columnaTotal += 1
        return columnaTotal
#--------------------------------------------------------------
# ejecucion de la ventana de autenticacion
ventanaAutenticacion()