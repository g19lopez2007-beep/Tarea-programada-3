#Creado por: Gustavo López Alvarado y Mel Acuña
#Version de python: 3.14
#Fecha de creacion 9/6/2026
#Fecha de creacion 10/6/2026

from tkinter import messagebox

#Funcion Aux para regresar al menu principal
def regresarMenuPrincipal(pVentanaPrincipal,pVentanaActual):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la ventana actual
    -Salida:
        Se cierra la ventana actual y se muestra la ventana principal
    '''
    pVentanaActual.destroy()
    pVentanaPrincipal.deiconify()

#Funcion Aux para mostrar funciones pendientes
def mostrarPendienteAux(pNombreFuncion):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el nombre de la función pendiente
    -Salida:
        Se muestra un mensaje indicando dónde debe ir la función
    '''
    messagebox.showinfo("Sistema de Parqueo","Aquí tiene que ir la función "+pNombreFuncion)