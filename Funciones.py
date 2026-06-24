#Creado por: Gustavo López Alvarado y Mel Acuña
#Version de python: 3.14
#Fecha de creacion 9/6/2026
#Ultima fecha de modificacion: 18/6/2026

from FuncionesAux import *
from tkinter import *
import pickle

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
    ventanaObtener.geometry("700x500")
    Label(ventanaObtener,text="OBTENER VEHÍCULOS",font=("Century Gothic",14,"bold")).pack(pady=15)
    frame=Frame(ventanaObtener)
    frame.pack()
    configuracion=cargarConfiguracionAux()
    Label(frame,text="Tamaño del estacionamiento:",font=("Century Gothic",12)).grid(row=0,column=0,pady=5,sticky="w")
    tamanno=Entry(frame,font=("Century Gothic",12))
    if configuracion!=False and configuracion[0]>0:
        tamanno.config(state="disabled")
        Label(frame,text="Máximo configurado: "+str(configuracion[0]),font=("Century Gothic",10)).grid(row=0,column=2,padx=10,pady=5,sticky="w")
    tamanno.grid(row=0,column=1,pady=5)
    Label(frame,text="Monto por hora:",font=("Century Gothic",12)).grid(row=1,column=0,pady=5,sticky="w")
    monto=Entry(frame,font=("Century Gothic",12))
    if configuracion!=False and configuracion[2]>0:
        monto.config(state="disabled")
        Label(frame,text="Monto configurado: ₡"+str(configuracion[2]),font=("Century Gothic",10)).grid(row=1,column=2,padx=10,pady=5,sticky="w")
    monto.grid(row=1,column=1,pady=5)
    Label(frame,text="Espacio para carro eléctrico:",font=("Century Gothic",12)).grid(row=2,column=0,pady=5,sticky="w")
    electrico=StringVar()
    electrico.set("No")
    OptionMenu(frame,electrico,"Sí","No").grid(row=2,column=1,pady=5,sticky="w")
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
    configuracion=cargarConfiguracionAux()
    guardarTamanno=False
    guardarMonto=False
    if configuracion!=False and configuracion[0]>0:
        tamanno=configuracion[0]
    else:
        validarTamanno=validarTamannoEstacionamientoAux(pTamanno.get())
        if validarTamanno!=True:
            messagebox.showinfo("Sistema de Parqueo",validarTamanno)
            return
        tamanno=int(pTamanno.get())
        guardarTamanno=True
    if configuracion!=False and configuracion[2]>0:
        monto=configuracion[2]
    else:
        validarMonto=validarMontoHoraAux(pMonto.get())
        if validarMonto!=True:
            messagebox.showinfo("Sistema de Parqueo",validarMonto)
            return
        monto=round(float(pMonto.get()),2)
        guardarMonto=True
    validarApi=validarApiAux(pApi.get())
    if validarApi!=True:
        messagebox.showinfo("Sistema de Parqueo",validarApi)
        return
    if pElectrico.get()=="Sí":
        electrico=1
    else:
        electrico=0
    cantidad=calcularTopeMasivoAux(tamanno,electrico)
    if cantidad<=0:
        messagebox.showinfo("Sistema de Parqueo","No hay espacios disponibles para realizar la carga masiva.")
        return
    datos=obtenerJsonApiAux(pApi.get(),cantidad)
    if type(datos)==str:
        messagebox.showinfo("Sistema de Parqueo",datos)
        return
    diccionario=crearDiccionarioVehiculosAux(datos,cantidad,monto)
    objetos=crearObjetosVehiculos(diccionario)
    pEstacionamiento.clear()
    for objeto in objetos:
        pEstacionamiento.append(objeto)
    if guardarTamanno==True:
        guardarConfiguracionAux(tamanno)
    if guardarMonto==True:
        guardarMontoHoraAux(monto)
    guardarEstacionamiento(pEstacionamiento)
    crearVouchersVehiculosAux(pEstacionamiento)
    messagebox.showinfo("Sistema de Parqueo","Se cargaron "+str(len(pEstacionamiento))+" vehículos correctamente.\nMáximo permitido por el estacionamiento: "+str(cantidad))
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

#Funcion principal de la opcion 2 del menu
def abrirObservarEspacio(pVentana,pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la lista del estacionamiento
    -Salida:
        Se muestra la ventana para observar un espacio
    '''
    pVentana.withdraw()
    ventana=Toplevel()
    ventana.title("Observar espacio")
    ventana.geometry("500x350")
    Label(ventana,text="OBSERVAR ESPACIO",font=("Century Gothic",14,"bold")).pack(pady=15)
    frame=Frame(ventana)
    frame.pack()
    Label(frame,text="Ubicación:",font=("Century Gothic",12)).grid(row=0,column=0,pady=5,sticky="w")
    ubicacion=Entry(frame,font=("Century Gothic",12))
    ubicacion.grid(row=0,column=1,pady=5)
    resultado=Label(ventana,text="",font=("Century Gothic",11),justify="left")
    resultado.pack(pady=15)
    Button(ventana,text="Buscar espacio",font=("Century Gothic",12,"bold"),width=30,command=lambda:observarEspacioTk(pEstacionamiento,ubicacion,resultado)).pack(pady=5)
    Button(ventana,text="Regresar",font=("Century Gothic",12,"bold"),width=30,command=lambda:regresarMenuPrincipal(pVentana,ventana)).pack(pady=5)

#Funcion principal de la opcion 2 del menu
def observarEspacioTk(pEstacionamiento,pUbicacion,pResultado):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista del estacionamiento, la ubicacion y el label de resultado
    -Salida:
        Se muestra la informacion del espacio consultado
    '''
    validar=validarObservarEspacioAux(pUbicacion.get())
    if validar!=True:
        messagebox.showinfo("Sistema de Parqueo",validar)
        return
    ubicacion=pUbicacion.get().strip()
    vehiculo=buscarVehiculoUbicacionAux(pEstacionamiento,ubicacion)
    if vehiculo==False:
        pResultado.config(text="Ubicación: "+ubicacion+"\nEstado: Libre")
    else:
        texto=""
        texto+="Ubicación: "+vehiculo.ubicacion+"\n"
        texto+="Estado: Ocupado\n"
        texto+="Placa: "+vehiculo.placa+"\n"
        texto+="Marca: "+vehiculo.marca+"\n"
        texto+="Color: "+vehiculo.color+"\n"
        texto+="Tipo: "+vehiculo.tipo+"\n"
        texto+="Entrada: "+vehiculo.fechaEntrada
        pResultado.config(text=texto)

#Funcion principal de la opcion 2 del menu
def abrirEstacionarVehiculo(pVentana,pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la lista del estacionamiento
    -Salida:
        Se muestra la ventana para estacionar un vehiculo manualmente
    '''
    pVentana.withdraw()
    ventana=Toplevel()
    ventana.title("Estacionar vehículo")
    ventana.geometry("600x450")
    Label(ventana,text="ESTACIONAR VEHÍCULO",font=("Century Gothic",14,"bold")).pack(pady=15)
    frame=Frame(ventana)
    frame.pack()
    Label(frame,text="Placa:",font=("Century Gothic",12)).grid(row=0,column=0,pady=5,sticky="w")
    placa=Entry(frame,font=("Century Gothic",12))
    placa.grid(row=0,column=1,pady=5)
    Label(frame,text="Marca:",font=("Century Gothic",12)).grid(row=1,column=0,pady=5,sticky="w")
    marca=Entry(frame,font=("Century Gothic",12))
    marca.grid(row=1,column=1,pady=5)
    Label(frame,text="Color:",font=("Century Gothic",12)).grid(row=2,column=0,pady=5,sticky="w")
    color=Entry(frame,font=("Century Gothic",12))
    color.grid(row=2,column=1,pady=5)
    Label(frame,text="Tipo:",font=("Century Gothic",12)).grid(row=3,column=0,pady=5,sticky="w")
    tipo=Entry(frame,font=("Century Gothic",12))
    tipo.grid(row=3,column=1,pady=5)
    Label(frame,text="Ubicación:",font=("Century Gothic",12)).grid(row=4,column=0,pady=5,sticky="w")
    ubicacion=Entry(frame,font=("Century Gothic",12))
    ubicacion.grid(row=4,column=1,pady=5)
    Label(frame,text="Monto por hora:",font=("Century Gothic",12)).grid(row=5,column=0,pady=5,sticky="w")
    monto=Entry(frame,font=("Century Gothic",12))
    monto.grid(row=5,column=1,pady=5)
    Button(ventana,text="Estacionar vehículo",font=("Century Gothic",12,"bold"),width=35,command=lambda:estacionarVehiculoTk(pVentana,ventana,pEstacionamiento,placa,marca,color,tipo,ubicacion,monto)).pack(pady=10)
    Button(ventana,text="Regresar",font=("Century Gothic",12,"bold"),width=35,command=lambda:regresarMenuPrincipal(pVentana,ventana)).pack(pady=5)

#Funcion principal de la opcion 2 del menu
def estacionarVehiculoTk(pVentanaPrincipal,pVentana,pEstacionamiento,pPlaca,pMarca,pColor,pTipo,pUbicacion,pMonto):
    '''
    Funcionamiento:
    -Entrada:
        Se reciben los datos del vehiculo digitados en la ventana
    -Salida:
        Se guarda el vehiculo en el estacionamiento
    '''
    validar=validarDatosEstacionarAux(pPlaca.get(),pMarca.get(),pColor.get(),pTipo.get(),pUbicacion.get())
    if validar!=True:
        messagebox.showinfo("Sistema de Parqueo",validar)
        return
    try:
        monto=round(float(pMonto.get()),2)
    except:
        messagebox.showinfo("Sistema de Parqueo","El monto por hora debe ser numérico.\nEjemplo: 1000 o 1000.50")
        return
    if monto<=0:
        messagebox.showinfo("Sistema de Parqueo","El monto por hora debe ser mayor a 0.")
        return
    placa=pPlaca.get().strip().upper()
    marca=pMarca.get().strip()
    color=pColor.get().strip()
    tipo=pTipo.get().strip()
    ubicacion=pUbicacion.get().strip().upper()
    existePlaca=buscarVehiculoPlacaAux(pEstacionamiento,placa)
    if existePlaca==True:
        messagebox.showinfo("Sistema de Parqueo","Ya existe un vehículo con esa placa.")
        return
    existeUbicacion=buscarVehiculoUbicacionAux(pEstacionamiento,ubicacion)
    if existeUbicacion!=False:
        messagebox.showinfo("Sistema de Parqueo","La ubicación ya está ocupada.")
        return
    fechaEntrada=generarFechaHoraEntradaAux()
    fechaSalida=""
    tipoPago=0
    vehiculo=Vehiculo(placa,marca,color,tipo,ubicacion,fechaEntrada,fechaSalida,monto,tipoPago)
    pEstacionamiento.append(vehiculo)
    guardarEstacionamiento(pEstacionamiento)
    crearVouchersVehiculosAux([vehiculo])
    messagebox.showinfo("Sistema de Parqueo","Vehículo estacionado correctamente.")
    regresarMenuPrincipal(pVentanaPrincipal,pVentana)

#Funcion principal de la opcion 3a del menu
def abrirTamannoEstacionamiento(pVentana,pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la lista del estacionamiento
    -Salida:
        Se muestra la ventana para configurar el tamaño del estacionamiento
    '''
    pVentana.withdraw()
    ventana=Toplevel()
    ventana.title("Tamaño del estacionamiento")
    ventana.geometry("500x300")
    Label(ventana,text="TAMAÑO DEL ESTACIONAMIENTO",font=("Century Gothic",14,"bold")).pack(pady=15)
    frame=Frame(ventana)
    frame.pack()
    Label(frame,text="Nuevo tamaño:",font=("Century Gothic",12)).grid(row=0,column=0,pady=5,sticky="w")
    tamanno=Entry(frame,font=("Century Gothic",12))
    tamanno.grid(row=0,column=1,pady=5)
    Button(ventana,text="Guardar",font=("Century Gothic",12,"bold"),width=35,command=lambda:guardarTamannoEstacionamientoTk(pVentana,ventana,pEstacionamiento,tamanno)).pack(pady=10)
    Button(ventana,text="Regresar",font=("Century Gothic",12,"bold"),width=35,command=lambda:regresarMenuPrincipal(pVentana,ventana)).pack(pady=5)

#Funcion principal de la opcion 3a del menu
def guardarTamannoEstacionamientoTk(pVentanaPrincipal,pVentana,pEstacionamiento,pTamanno):
    '''
    Funcionamiento:
    -Entrada:
        Se reciben la ventana principal, la ventana actual, el estacionamiento y el campo de tamaño
    -Salida:
        Se guarda el nuevo tamaño del estacionamiento en configuración
    '''
    validar=validarTamannoEstacionamientoAux(pTamanno.get())
    if validar!=True:
        messagebox.showinfo("Sistema de Parqueo",validar)
        return
    tamanno=int(pTamanno.get())
    configuracion=cargarConfiguracionAux()
    if configuracion!=False and configuracion[0]>0:
        confirmar=messagebox.askyesno("Sistema de Parqueo","Ya existe un tamaño de estacionamiento guardado.\nSi continúa, puede perder datos.\n¿Está seguro que desea continuar?")
        if confirmar==False:
            return
    if tamanno<len(pEstacionamiento):
        messagebox.showinfo("Sistema de Parqueo","El tamaño del estacionamiento no puede ser menor que la cantidad de vehículos cargados.")
        return
    guardarConfiguracionAux(tamanno)
    messagebox.showinfo("Sistema de Parqueo","Tamaño del estacionamiento guardado correctamente.")
    regresarMenuPrincipal(pVentanaPrincipal,pVentana)

#Funcion principal de la opcion 3b del menu
def abrirModificarMontoHora(pVentana):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal
    -Salida:
        Se muestra la ventana para modificar el monto por hora
    '''
    pVentana.withdraw()
    ventana=Toplevel()
    ventana.title("Modificar monto por hora")
    ventana.geometry("500x300")
    Label(ventana,text="MODIFICAR MONTO POR HORA",font=("Century Gothic",14,"bold")).pack(pady=15)
    frame=Frame(ventana)
    frame.pack()
    Label(frame,text="Nuevo monto:",font=("Century Gothic",12)).grid(row=0,column=0,pady=5,sticky="w")
    monto=Entry(frame,font=("Century Gothic",12))
    monto.grid(row=0,column=1,pady=5)
    Button(ventana,text="Guardar",font=("Century Gothic",12,"bold"),width=35,command=lambda:guardarMontoHoraTk(pVentana,ventana,monto)).pack(pady=10)
    Button(ventana,text="Regresar",font=("Century Gothic",12,"bold"),width=35,command=lambda:regresarMenuPrincipal(pVentana,ventana)).pack(pady=5)

#Funcion principal de la opcion 3b del menu
def guardarMontoHoraTk(pVentanaPrincipal,pVentana,pMonto):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal, la ventana actual y el monto por hora
    -Salida:
        Se valida y guarda el monto por hora en configuración
    '''
    validar=validarMontoHoraAux(pMonto.get())
    if validar!=True:
        messagebox.showinfo("Sistema de Parqueo",validar)
        return
    resultado=guardarMontoHoraAux(pMonto.get())
    if resultado!=True:
        messagebox.showinfo("Sistema de Parqueo",resultado)
        return
    messagebox.showinfo("Sistema de Parqueo","Monto por hora guardado correctamente.")
    regresarMenuPrincipal(pVentanaPrincipal,pVentana)

#Funcion principal de la opcion 3c del menu
def abrirTiempoGracia(pVentana,pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la lista del estacionamiento
    -Salida:
        Se muestra la ventana para configurar el tiempo de gracia
    '''
    pVentana.withdraw()
    ventana=Toplevel()
    ventana.title("Tiempo de gracia")
    ventana.geometry("500x300")
    Label(ventana,text="TIEMPO DE GRACIA",font=("Century Gothic",14,"bold")).pack(pady=15)
    configuracion=cargarConfiguracionAux()
    if configuracion!=False:
        textoActual="Tiempo actual: "+str(configuracion[1])+" minutos"
    else:
        textoActual="Tiempo actual: 0 minutos"
    Label(ventana,text=textoActual,font=("Century Gothic",12)).pack(pady=5)
    frame=Frame(ventana)
    frame.pack()
    Label(frame,text="Nuevo tiempo:",font=("Century Gothic",12)).grid(row=0,column=0,pady=5,sticky="w")
    tiempo=Entry(frame,font=("Century Gothic",12))
    tiempo.grid(row=0,column=1,pady=5)
    Button(ventana,text="Guardar",font=("Century Gothic",12,"bold"),width=35,command=lambda:guardarTiempoGraciaTk(pVentana,ventana,pEstacionamiento,tiempo)).pack(pady=10)
    Button(ventana,text="Regresar",font=("Century Gothic",12,"bold"),width=35,command=lambda:regresarMenuPrincipal(pVentana,ventana)).pack(pady=5)

#Funcion principal de la opcion 3c del menu
def guardarTiempoGraciaTk(pVentanaPrincipal,pVentana,pEstacionamiento,pTiempo):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal, la ventana actual, el estacionamiento y el campo de tiempo
    -Salida:
        Se guarda el tiempo de gracia en la configuracion
    '''
    validar=validarTiempoGraciaAux(pTiempo.get())
    if validar!=True:
        messagebox.showinfo("Sistema de Parqueo",validar)
        return
    tiempo=int(pTiempo.get())
    guardarTiempoGraciaAux(tiempo)
    messagebox.showinfo("Sistema de Parqueo","Tiempo de gracia guardado correctamente.")
    regresarMenuPrincipal(pVentanaPrincipal,pVentana)

#Funcion principal de la opcion 4a del menu
def abrirCierreDiario(pVentana,pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la lista del estacionamiento
    -Salida:
        Se muestra el reporte de cierre diario
    '''
    pVentana.withdraw()
    ventana=Toplevel()
    ventana.title("Cierre diario")
    ventana.geometry("550x400")
    Label(ventana,text="CIERRE DIARIO",font=("Century Gothic",14,"bold")).pack(pady=15)
    datos=calcularCierreDiarioAux(pEstacionamiento)
    guardarCierreDiarioDatAux(datos)
    texto=""
    texto+="Cantidad de vehículos registrados: "+str(datos[0])+"\n"
    texto+="Vehículos activos en el parqueo: "+str(datos[2])+"\n"
    texto+="Vehículos retirados: "+str(datos[0]-datos[2])+"\n"
    texto+="Ingreso total del día: ₡"+str(round(datos[1],2))+"\n"
    Label(ventana,text=texto,font=("Century Gothic",12),justify="left").pack(pady=20)
    Button(ventana,text="Regresar",font=("Century Gothic",12,"bold"),width=35,command=lambda:regresarMenuPrincipal(pVentana,ventana)).pack(pady=10)

#Funcion principal de la opcion 4b del menu
def abrirCierreTipoPago(pVentana,pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la lista del estacionamiento
    -Salida:
        Se muestra el cierre por tipo de pago
    '''
    validar=validarDatosReporteAux(pEstacionamiento,cargarConfiguracionAux())
    if validar!=True:
        messagebox.showinfo("Sistema de Parqueo",validar)
        return
    pVentana.withdraw()
    ventana=Toplevel()
    ventana.title("Cierre por tipo de pago")
    ventana.geometry("600x450")
    Label(ventana,text="CIERRE POR TIPO DE PAGO",font=("Century Gothic",14,"bold")).pack(pady=15)
    datos=calcularCierreTipoPagoAux(pEstacionamiento)
    texto=""
    texto+="EFECTIVO\n"
    texto+="Cantidad: "+str(datos[0])+"\n"
    texto+="Ingresos: ₡"+str(round(datos[1],2))+"\n\n"
    texto+="TARJETA\n"
    texto+="Cantidad: "+str(datos[2])+"\n"
    texto+="Ingresos: ₡"+str(round(datos[3],2))+"\n\n"
    texto+="SINPE\n"
    texto+="Cantidad: "+str(datos[4])+"\n"
    texto+="Ingresos: ₡"+str(round(datos[5],2))
    Label(ventana,text=texto,font=("Century Gothic",12),justify="left").pack(pady=20)
    Button(ventana,text="Regresar",font=("Century Gothic",12,"bold"),width=35,command=lambda:regresarMenuPrincipal(pVentana,ventana)).pack(pady=10)

#Funcion principal de la opcion 4c del menu
def abrirExportarCierreDiarioCsv(pVentana,pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la lista del estacionamiento
    -Salida:
        Se exporta el cierre diario a un archivo CSV
    '''
    validar=validarExportarCierreDiarioCsvAux()
    if validar!=True:
        messagebox.showinfo("Sistema de Parqueo",validar)
        return
    nombre=exportarCierreDiarioCsvAux()
    messagebox.showinfo("Sistema de Parqueo","El cierre diario se exportó correctamente.\nArchivo generado: "+nombre)
    
#Funcion principal de la opcion 5 del menu
def abrirAcercaDe(pVentana):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal
    -Salida:
        Se muestra la ventana acerca de con la información de los creadores
    '''
    pVentana.withdraw()
    ventana=Toplevel()
    ventana.title("Acerca de")
    ventana.geometry("600x450")
    Label(ventana,text="ACERCA DE",font=("Century Gothic",14,"bold")).pack(pady=15)
    texto="\nCreadores:\nGustavo López Alvarado\nMel Acuña\n\nCurso:\nTaller de Programación\n\nInstitución:\nInstituto Tecnológico de Costa Rica."
    Label(ventana,text=texto,font=("Century Gothic",12),justify="center").pack(pady=20)
    Button(ventana,text="Regresar",font=("Century Gothic",12,"bold"),width=35,command=lambda:regresarMenuPrincipal(pVentana,ventana)).pack(pady=10)