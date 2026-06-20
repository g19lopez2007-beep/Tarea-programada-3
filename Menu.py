#Creado por: Gustavo López Alvarado y Mel Acuña
#Version de python: 3.14
#Fecha de creacion 9/6/2026
#Ultima fecha de modificacion: 18/6/2026

from Funciones import *
from tkinter import *

def abrirSubmenuVerEstacionamiento(pVentana,pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la lista del estacionamiento
    -Salida:
        Se muestra el submenú de ver estacionamiento
    '''
    pVentana.withdraw()
    ventana=Toplevel()
    ventana.title("Ver estacionamiento")
    ventana.geometry("500x350")
    Label(ventana,text="VER ESTACIONAMIENTO",font=("Century Gothic",14,"bold")).pack(pady=15)
    Button(ventana,text="1.Observar espacio",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirObservarEspacio(ventana,pEstacionamiento)).pack(pady=5)
    Button(ventana,text="2.Estacionar un vehículo",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirEstacionarVehiculo(ventana,pEstacionamiento)).pack(pady=5)
    Button(ventana,text="3.Regresar",font=("Century Gothic",12,"bold"),width=35,command=lambda:regresarMenuPrincipal(pVentana,ventana)).pack(pady=5)

def abrirSubmenuReportes(pVentana,pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la lista del estacionamiento
    -Salida:
        Se muestra el submenú de reportes
    '''
    pVentana.withdraw()
    ventana=Toplevel()
    ventana.title("Reportes")
    ventana.geometry("500x400")
    Label(ventana,text="REPORTES",font=("Century Gothic",14,"bold")).pack(pady=15)
    Button(ventana,text="1.Cierre diario",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirCierreDiario(ventana,pEstacionamiento)).pack(pady=5)
    Button(ventana,text="2.Cierre por tipo de pago",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirCierreTipoPago(ventana,pEstacionamiento)).pack(pady=5)
    Button(ventana,text="3.Exportar cierre diario a CSV",font=("Century Gothic",12,"bold"),width=35,command=lambda:ejecutarFuncionPendiente("exportarCierreDiarioCsv")).pack(pady=5)
    Button(ventana,text="4.Regresar",font=("Century Gothic",12,"bold"),width=35,command=lambda:regresarMenuPrincipal(pVentana,ventana)).pack(pady=5)

def abrirSubmenuConfiguracion(pVentana,pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ventana principal y la lista del estacionamiento
    -Salida:
        Se muestra el submenú de configuración
    '''
    pVentana.withdraw()
    ventana=Toplevel()
    ventana.title("Configuración")
    ventana.geometry("500x400")
    Label(ventana,text="CONFIGURACIÓN",font=("Century Gothic",14,"bold")).pack(pady=15)
    Button(ventana,text="1.Tamaño del estacionamiento",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirTamannoEstacionamiento(ventana,pEstacionamiento)).pack(pady=5)
    Button(ventana,text="2.Modificar monto por hora",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirModificarMontoHora(ventana)).pack(pady=5)
    Button(ventana,text="3.Tiempo de gracia en minutos",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirTiempoGracia(ventana,pEstacionamiento)).pack(pady=5)
    Button(ventana,text="4.Regresar",font=("Century Gothic",12,"bold"),width=35,command=lambda:regresarMenuPrincipal(pVentana,ventana)).pack(pady=5)

def menuPrincipal(pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista del estacionamiento
    -Salida:
        Se muestra el menú principal usando tkinter
    '''
    ventana=Tk()
    ventana.title("Sistema de Parqueo")
    ventana.geometry("500x450")
    Label(ventana,text="SISTEMA DE PARQUEO",font=("Century Gothic",14,"bold")).pack(pady=15)
    Button(ventana,text="1.Obtener vehículos",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirObtenerVehiculos(ventana,pEstacionamiento)).pack(pady=5)
    Button(ventana,text="2.Ver estacionamiento",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirSubmenuVerEstacionamiento(ventana,pEstacionamiento)).pack(pady=5)
    Button(ventana,text="3.Configuración",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirSubmenuConfiguracion(ventana,pEstacionamiento)).pack(pady=5)
    Button(ventana,text="4.Reportes",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirSubmenuReportes(ventana,pEstacionamiento)).pack(pady=5)
    Button(ventana,text="5.Acerca de",font=("Century Gothic",12,"bold"),width=35,command=lambda:abrirAcercaDe(ventana)).pack(pady=5)
    Button(ventana,text="6.Salir",font=("Century Gothic",12,"bold"),width=35,command=ventana.destroy).pack(pady=5)
    ventana.mainloop()
estacionamiento=cargarEstacionamiento()
menuPrincipal(estacionamiento)