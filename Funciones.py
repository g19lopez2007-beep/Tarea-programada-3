#Creado por: Gustavo López Alvarado y Mel Acuña
#Version de python: 3.14
#Fecha de creacion 9/6/2026
#Fecha de creacion 11/6/2026

from FuncionesAux import *
import pickle
from tkinter import *

#Funcion principal temporal para las opciones del sistema
def ejecutarFuncionPendiente(pNombreFuncion):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el nombre de la función que luego se debe programar
    -Salida:
        Se muestra un mensaje indicando dónde debe ir esa función
    '''
    mostrarPendienteAux(pNombreFuncion)

class Vehiculo:
    '''
    Funcionamiento:
    -Entrada:
        Se reciben los datos del vehículo
    -Salida:
        Se crea un objeto vehículo para guardar en el estacionamiento
    '''
    def __init__(self,pPlaca,pMarca,pColor,pTipo,pUbicacion,pFechaEntrada,pFechaSalida,pMontoHora,pTipoPago):
        self.placa=pPlaca
        self.marca=pMarca
        self.color=pColor
        self.tipo=pTipo
        self.ubicacion=pUbicacion
        self.fechaEntrada=pFechaEntrada
        self.fechaSalida=pFechaSalida
        self.montoHora=pMontoHora
        self.tipoPago=pTipoPago

#Funcion principal temporal para las opciones del sistema
def ejecutarFuncionPendiente(pNombreFuncion):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el nombre de la función pendiente
    -Salida:
        Se muestra un mensaje indicando dónde debe ir esa función
    '''
    mostrarPendienteAux(pNombreFuncion)

#Funcion principal de carga inicial del menu
def cargarEstacionamiento():
    '''
    Funcionamiento:
    -Entrada:
        No recibe datos
    -Salida:
        Se carga la lista del estacionamiento desde memoria secundaria
    '''
    try:
        archivo=open("estacionamiento.dat","rb")
        estacionamiento=pickle.load(archivo)
        archivo.close()
        return estacionamiento
    except:
        return []

#Funcion principal para guardar datos del sistema
def guardarEstacionamiento(pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista del estacionamiento
    -Salida:
        Se guarda la lista del estacionamiento en memoria secundaria
    '''
    archivo=open("estacionamiento.dat","wb")
    pickle.dump(pEstacionamiento,archivo)
    archivo.close()

#Funcion principal de la opcion 1 del menu
def abrirObtenerVehiculos(pVentana,pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la lista del estacionamiento
    -Salida:
        Se muestra la ventana para obtener vehículos
    '''
    pVentana.withdraw()
    ventanaObtener=Toplevel()
    ventanaObtener.title("Obtener vehículos")
    ventanaObtener.geometry("600x450")
    Label(ventanaObtener,text="OBTENER VEHÍCULOS",font=("Century Gothic",14,"bold")).pack(pady=15)
    frame=Frame(ventanaObtener)
    frame.pack()
    Label(frame,text="Tamaño del estacionamiento:",font=("Century Gothic",12)).grid(row=0,column=0,pady=5,sticky="w")
    tamanno=Entry(frame,font=("Century Gothic",12))
    tamanno.grid(row=0,column=1,pady=5)
    Label(frame,text="Espacio para carro eléctrico:",font=("Century Gothic",12)).grid(row=1,column=0,pady=5,sticky="w")
    electrico=StringVar()
    electrico.set("No")
    OptionMenu(frame,electrico,"Sí","No").grid(row=1,column=1,pady=5,sticky="w")
    Label(frame,text="Monto por hora:",font=("Century Gothic",12)).grid(row=2,column=0,pady=5,sticky="w")
    monto=Entry(frame,font=("Century Gothic",12))
    monto.grid(row=2,column=1,pady=5)
    Label(frame,text="URL de la API:",font=("Century Gothic",12)).grid(row=3,column=0,pady=5,sticky="w")
    api=Entry(frame,font=("Century Gothic",12),width=35)
    api.grid(row=3,column=1,pady=5)
    Button(ventanaObtener,text="Obtener vehículos",font=("Century Gothic",12,"bold"),width=35,command=lambda:obtenerVehiculosTk(pVentana,ventanaObtener,pEstacionamiento,tamanno,electrico,monto,api)).pack(pady=10)
    Button(ventanaObtener,text="Regresar",font=("Century Gothic",12,"bold"),width=35,command=lambda:regresarMenuPrincipal(pVentana,ventanaObtener)).pack(pady=5)

#Funcion principal de la opcion 1 del menu
def obtenerVehiculosTk(pVentanaPrincipal,pVentana,pEstacionamiento,pTamanno,pElectrico,pMonto,pApi):
    '''
    Funcionamiento:
    -Entrada:
        Se reciben los datos escritos en la ventana para obtener vehículos
    -Salida:
        Se obtienen vehículos, se guardan como objetos, se generan los vouchers y se vuelve al menú
    '''
    validar=validarDatosObtenerVehiculosAux(pTamanno.get(),pMonto.get(),pApi.get())
    if validar!=True:
        messagebox.showinfo("Sistema de Parqueo",validar)
        return
    tamanno=int(pTamanno.get())
    monto=round(float(pMonto.get()),2)
    if pElectrico.get()=="Sí":
        electrico=1
    else:
        electrico=0
    cantidad=calcularTopeMasivoAux(tamanno,electrico)
    datos=obtenerJsonApiAux(pApi.get(),cantidad)
    if type(datos)==str:
        messagebox.showinfo("Sistema de Parqueo",datos)
        return
    diccionario=crearDiccionarioVehiculosAux(datos,cantidad,monto)
    objetos=crearObjetosVehiculos(diccionario)
    pEstacionamiento.clear()
    for objeto in objetos:
        pEstacionamiento.append(objeto)
    guardarEstacionamiento(pEstacionamiento)
    crearVouchersVehiculosAux(pEstacionamiento)
    messagebox.showinfo("Sistema de Parqueo","Se cargaron "+str(len(pEstacionamiento))+" vehículos correctamente.")
    regresarMenuPrincipal(pVentanaPrincipal,pVentana)

#Funcion principal de la opcion 1 del menu
def crearObjetosVehiculos(pDiccionario):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el diccionario de vehículos
    -Salida:
        Se devuelve una lista de objetos vehículo
    '''
    lista=[]
    for placa in pDiccionario:
        datos=pDiccionario[placa]
        lista.append(Vehiculo(placa,datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7]))
    return lista