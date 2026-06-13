#Creado por: Gustavo López Alvarado y Mel Acuña
#Version de python: 3.14
#Fecha de creacion 9/6/2026
#Ultima fecha de modificacion: 12/6/2026
from tkinter import messagebox
import pickle
import time
import random
import json
import urllib.request
import qrcode
from PIL import Image,ImageDraw

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

#Funcion Aux de la opcion 1 del menu
def validarDatosObtenerVehiculosAux(pTamanno,pMonto,pApi):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el tamaño, monto por hora y URL de la API
    -Salida:
        Se devuelve True si los datos son válidos o un mensaje indicando el formato correcto
    '''
    if pTamanno.strip()=="":
        return "Debe ingresar el tamaño del estacionamiento.\nFormato correcto: número entero positivo, por ejemplo: 20"
    try:
        tamanno=int(pTamanno)
    except:
        return "El tamaño del estacionamiento debe escribirse con números enteros.\nFormato correcto: 20"
    if tamanno<3:
        return "El tamaño del estacionamiento no es válido.\nFormato correcto: debe ser un número mayor o igual a 3"
    if pMonto.strip()=="":
        return "Debe ingresar el monto por hora.\nFormato correcto: número positivo, por ejemplo: 1000 o 1000.50"
    try:
        monto=round(float(pMonto),2)
    except:
        return "El monto por hora debe escribirse con números.\nFormato correcto: 1000 o 1000.50"
    if monto<=0:
        return "El monto por hora no es válido.\nFormato correcto: debe ser mayor a 0"
    if pApi.strip()=="":
        return "Debe ingresar la URL de la API.\nFormato correcto: https://myfakeapi.com/api/cars/"
    if not(pApi.startswith("http://") or pApi.startswith("https://")):
        return "La URL de la API no tiene el formato correcto.\nFormato correcto: debe iniciar con http:// o https://"
    return True

#Funcion Aux de la opcion 1 del menu
def calcularEspaciosEspecialesAux(pTamanno):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el tamaño del estacionamiento
    -Salida:
        Se devuelve la cantidad de espacios especiales
    '''
    especiales=pTamanno*5/100
    if especiales>int(especiales):
        especiales=int(especiales)+1
    else:
        especiales=int(especiales)
    if pTamanno<=20 and especiales<2:
        especiales=2
    return especiales

#Funcion Aux de la opcion 1 del menu
def calcularTopeMasivoAux(pTamanno,pElectrico):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el tamaño del estacionamiento y si posee espacio eléctrico
    -Salida:
        Se devuelve la cantidad de vehículos que se pueden cargar masivamente
    '''
    especiales=calcularEspaciosEspecialesAux(pTamanno)
    disponibles=pTamanno-especiales-pElectrico
    reserva=disponibles*5/100
    if reserva>int(reserva):
        reserva=int(reserva)+1
    else:
        reserva=int(reserva)
    return disponibles-reserva

#Funcion Aux de la opcion 1 del menu
def obtenerJsonApiAux(pUrl,pCantidad):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la URL de la API y la cantidad de vehículos
    -Salida:
        Se devuelve la información JSON obtenida desde la API
    '''
    try:
        respuesta=urllib.request.urlopen(pUrl)
        contenido=respuesta.read().decode("utf-8")
        datos=json.loads(contenido)
        if type(datos)==dict:
            if "cars" in datos:
                return datos["cars"][:pCantidad]
            return [datos]
        return datos[:pCantidad]
    except:
        return "No se pudo obtener la información de la API.\nFormato correcto: https://myfakeapi.com/api/cars/\nVerifique que tenga conexión a internet"

#Funcion Aux de la opcion 1 del menu
def crearDiccionarioVehiculosAux(pDatos,pCantidad,pMonto):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la información obtenida, la cantidad y el monto por hora
    -Salida:
        Se devuelve un diccionario con los vehículos cargados
    '''
    diccionario={}
    contador=0
    for dato in pDatos:
        if contador==pCantidad:
            break
        placa=obtenerDatoJsonAux(dato,("placa","license_plate","plate","car_plate","id","vin"))
        marca=obtenerDatoJsonAux(dato,("marca","make","brand","car_make","modelo","model","make_and_model","car"))
        color=obtenerDatoJsonAux(dato,("color","car_color"))
        tipo=obtenerDatoJsonAux(dato,("tipo","car_type","vehicle_type","type","car_model"))
        if placa=="Sin dato":
            placa="TMP"+str(contador+1).zfill(4)
        ubicacion="G"+str(contador+1)
        fechaEntrada=generarFechaHoraEntradaAux()
        fechaSalida=""
        tipoPago=0
        diccionario[placa]=[marca,color,tipo,ubicacion,fechaEntrada,fechaSalida,pMonto,tipoPago]
        contador+=1
    return diccionario

#Funcion Aux de la opcion 1 del menu
def obtenerDatoJsonAux(pDato,pLlaves):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe un dato del JSON y las posibles llaves
    -Salida:
        Se devuelve el dato encontrado o un texto temporal
    '''
    for llave in pLlaves:
        if llave in pDato:
            return str(pDato[llave])
    return "Sin dato"

#Funcion Aux de la opcion 1 del menu
def generarFechaHoraEntradaAux():
    '''
    Funcionamiento:
    -Entrada:
        No recibe datos
    -Salida:
        Se devuelve una fecha y hora de entrada entre las 7:00 y la hora actual
    '''
    actual=time.localtime()
    horaActual=actual.tm_hour
    minutoActual=actual.tm_min
    if horaActual<7:
        hora=7
        minuto=0
    else:
        hora=random.randint(7,horaActual)
        if hora==horaActual:
            minuto=random.randint(0,minutoActual)
        else:
            minuto=random.randint(0,59)
    return time.strftime("%d/%m/%Y",actual)+" "+str(hora).zfill(2)+":"+str(minuto).zfill(2)

#Funcion Aux de la opcion 1 del menu
def crearVouchersVehiculosAux(pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista de vehículos del estacionamiento
    -Salida:
        Se crean vouchers en PDF con código QR
    '''
    for vehiculo in pEstacionamiento:
        texto="Placa: "+vehiculo.placa+"\nMarca: "+vehiculo.marca+"\nColor: "+vehiculo.color+"\nTipo: "+vehiculo.tipo+"\nUbicación: "+vehiculo.ubicacion+"\nEntrada: "+vehiculo.fechaEntrada
        qr=qrcode.make(texto)
        imagen=Image.new("RGB",(600,800),"white")
        dibujo=ImageDraw.Draw(imagen)
        dibujo.text((30,30),"VOUCHER DE ESTACIONAMIENTO",fill="black")
        dibujo.text((30,80),"Placa: "+vehiculo.placa,fill="black")
        dibujo.text((30,120),"Marca: "+vehiculo.marca,fill="black")
        dibujo.text((30,160),"Color: "+vehiculo.color,fill="black")
        dibujo.text((30,200),"Tipo: "+vehiculo.tipo,fill="black")
        dibujo.text((30,240),"Ubicación: "+vehiculo.ubicacion,fill="black")
        dibujo.text((30,280),"Entrada: "+vehiculo.fechaEntrada,fill="black")
        qr=qr.resize((250,250))
        imagen.paste(qr,(170,360))
        nombre="voucher_"+limpiarNombreArchivoAux(vehiculo.placa)+"_"+obtenerFechaArchivoAux()+".pdf"
        imagen.save(nombre,"PDF")

#Funcion Aux de la opcion 1 del menu
def limpiarNombreArchivoAux(pTexto):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe un texto que se usará como nombre de archivo
    -Salida:
        Se devuelve el texto sin caracteres problemáticos
    '''
    nuevo=""
    for caracter in pTexto:
        if caracter.isalnum():
            nuevo+=caracter
    return nuevo

#Funcion Aux de la opcion 1 del menu
def obtenerFechaArchivoAux():
    '''
    Funcionamiento:
    -Entrada:
        No recibe datos
    -Salida:
        Se devuelve la fecha y hora actual para usar en nombres de archivo
    '''
    return time.strftime("%d-%m-%Y_%H-%M")

#Funcion Aux de la opcion 2 del menu
def buscarVehiculoUbicacionAux(pEstacionamiento,pUbicacion):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista del estacionamiento y la ubicacion a buscar
    -Salida:
        Se devuelve el vehiculo encontrado o False si no existe
    '''
    for vehiculo in pEstacionamiento:
        if vehiculo.ubicacion==pUbicacion:
            return vehiculo
    return False

#Funcion Aux de la opcion 2 del menu
def validarDatosEstacionarAux(pPlaca,pMarca,pColor,pTipo,pUbicacion):
    '''
    Funcionamiento:
    -Entrada:
        Se reciben los datos del vehiculo
    -Salida:
        Se devuelve True si los datos son validos o un mensaje de error
    '''
    if pPlaca.strip()=="":
        return "Debe ingresar la placa del vehículo."
    if pMarca.strip()=="":
        return "Debe ingresar la marca del vehículo."
    if pColor.strip()=="":
        return "Debe ingresar el color del vehículo."
    if pTipo.strip()=="":
        return "Debe ingresar el tipo del vehículo."
    if pUbicacion.strip()=="":
        return "Debe ingresar la ubicación del vehículo.\nEjemplo: G1"
    return True

#Funcion Aux de la opcion 2 del menu
def buscarVehiculoPlacaAux(pEstacionamiento,pPlaca):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista del estacionamiento y la placa a buscar
    -Salida:
        Se devuelve True si la placa ya existe o False si no existe
    '''
    for vehiculo in pEstacionamiento:
        if vehiculo.placa==pPlaca:
            return True
    return False

#Funcion Aux de la opcion 2 del menu
def validarObservarEspacioAux(pUbicacion):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la ubicacion digitada
    -Salida:
        Se devuelve True si es valida o un mensaje de error
    '''
    if pUbicacion.strip()=="":
        return "Debe ingresar una ubicación.\nFormato correcto: G1, G2, G3"
    return True

#Funcion Aux de la opcion 4a del menu
def validarTamannoEstacionamientoAux(pTamanno):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el texto del campo de tamaño
    -Salida:
        Se devuelve True si el dato es válido o un mensaje indicando el formato correcto
    '''
    if pTamanno.strip()=="":
        return "Debe ingresar el tamaño del estacionamiento.\nFormato correcto: número entero positivo, por ejemplo: 20"
    try:
        tamanno=int(pTamanno)
    except:
        return "El tamaño del estacionamiento debe escribirse con números enteros.\nFormato correcto: 20"
    if tamanno<3:
        return "El tamaño del estacionamiento no es válido.\nFormato correcto: debe ser un número mayor o igual a 3"
    return True

#Funcion Aux de la opcion 4a del menu
def guardarConfiguracionAux(pTamanno):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el tamaño del estacionamiento a guardar
    -Salida:
        Se guarda la configuración en memoria secundaria
    '''
    configuracion=cargarConfiguracionAux()
    if configuracion==False:
        configuracion=[0,0,0.0]
    configuracion[0]=pTamanno
    archivo=open("configuracion.dat","wb")
    pickle.dump(configuracion,archivo)
    archivo.close()

#Funcion Aux de la opcion 4a del menu
def cargarConfiguracionAux():
    '''
    Funcionamiento:
    -Entrada:
        No recibe datos
    -Salida:
        Se devuelve la lista de configuración [tamanno,tiempoGracia,montoHora] o False si no existe
    '''
    try:
        archivo=open("configuracion.dat","rb")
        configuracion=pickle.load(archivo)
        archivo.close()
        return configuracion
    except:
        return False