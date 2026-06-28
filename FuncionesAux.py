#Creado por: Gustavo López Alvarado y Mel Acuña
#Version de python: 3.14
#Fecha de creacion 9/6/2026
#Ultima fecha de modificacion: 27/6/2026

from tkinter import messagebox
from PIL import Image,ImageDraw
import urllib.request
import pickle
import time
import random
import json
import qrcode

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

#Funcion Aux de configuracion
def obtenerConfiguracionAux():
    '''
    Funcionamiento:
    -Entrada:
        No recibe datos
    -Salida:
        Se devuelve la configuración actual o se crea una nueva si no existe
    '''
    configuracion=cargarConfiguracionAux()
    if configuracion==False:
        configuracion=[0,-1,0.0]
        archivo=open("configuracion.dat","wb")
        pickle.dump(configuracion,archivo)
        archivo.close()
    return configuracion

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
def validarApiAux(pApi):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la URL de la API
    -Salida:
        Se devuelve True si la URL es válida o un mensaje indicando el formato correcto
    '''
    if pApi.strip()=="":
        return "Debe ingresar la URL de la API.\nFormato correcto: https://myfakeapi.com/api/cars/"
    if not(pApi.startswith("http://") or pApi.startswith("https://")):
        return "La URL de la API no tiene el formato correcto.\nFormato correcto: debe iniciar con http:// o https://"
    return True

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

#Funcion Aux de la opcion 1 del menu
def validarDatosApiObtenidosAux(pDatos):
    '''
    Funcionamiento:
    -Entrada:
        Se reciben los datos obtenidos desde la API
    -Salida:
        Se devuelve True si los datos son validos o un mensaje de error
    '''
    if type(pDatos)!=list:
        return "La API no devolvió una lista válida de vehículos."
    if len(pDatos)==0:
        return "La API no devolvió vehículos."
    return True

#Funcion Aux de la opcion 1 del menu
def validarReinicioEstacionamientoAux(pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista del estacionamiento
    -Salida:
        Se devuelve True si se puede cargar o False si el usuario cancela
    '''
    if len(pEstacionamiento)>0:
        confirmar=messagebox.askyesno("Sistema de Parqueo","Ya existen vehículos cargados.\nSi continúa se reemplazará el estacionamiento actual.\n¿Desea continuar?")
        if confirmar==False:
            return False
    return True

#Funcion Aux de la opcion 2 del menu
def validarUbicacionDisponibleAux(pEstacionamiento,pUbicacion):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el estacionamiento y la ubicacion
    -Salida:
        Se devuelve True si la ubicacion existe y esta libre o un mensaje de error
    '''
    configuracion=cargarConfiguracionAux()
    if configuracion==False:
        return "Debe configurar primero el tamaño del estacionamiento."
    tamanno=configuracion[0]
    if tamanno<=0:
        return "Debe configurar primero el tamaño del estacionamiento."
    ubicacion=pUbicacion.strip().upper()
    try:
        numero=int(ubicacion[1:])
    except:
        return "La ubicación debe tener formato correcto.\nEjemplo: G1"
    if numero>tamanno:
        return "La ubicación no existe.\nEl estacionamiento llega hasta G"+str(tamanno)+"."
    vehiculo=buscarVehiculoUbicacionAux(pEstacionamiento,ubicacion)
    if vehiculo!=False and vehiculo.fechaSalida=="":
        return "La ubicación ya está ocupada."
    return True

#Funcion Aux de la opcion 2 del menu
def validarEstacionamientoCreadoAux():
    '''
    Funcionamiento:
    -Entrada:
        No recibe datos
    -Salida:
        Se devuelve True si el estacionamiento ya fue configurado o un mensaje indicando qué falta
    '''
    configuracion=cargarConfiguracionAux()
    if configuracion==False:
        return "Debe configurar primero el tamaño del estacionamiento."
    if configuracion[0]<=0:
        return "Debe configurar primero el tamaño del estacionamiento."
    return True

#Funcion Aux de la opcion 2 del menu
def buscarVehiculoUbicacionAux(pEstacionamiento,pUbicacion):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista del estacionamiento y la ubicacion a buscar
    -Salida:
        Se devuelve el vehiculo activo encontrado o False si no existe
    '''
    for vehiculo in pEstacionamiento:
        if vehiculo.ubicacion==pUbicacion and vehiculo.fechaSalida=="":
            return vehiculo
    return False

#Funcion Aux de la opcion 2 del menu
def validarDatosEstacionarAux(pPlaca,pMarca,pColor,pTipo,pUbicacion):
    '''
    Funcionamiento:
    -Entrada:
        Se reciben los datos del vehiculo
    -Salida:
        Se devuelve True si los datos son validos o un mensaje indicando el formato correcto
    '''
    placa=pPlaca.strip().upper()
    marca=pMarca.strip()
    color=pColor.strip()
    tipo=pTipo.strip()
    ubicacion=pUbicacion.strip().upper()
    if placa=="":
        return "Debe ingresar la placa del vehículo.\nFormato correcto: letras y números, por ejemplo: ABC123"
    if len(placa)<5 or len(placa)>8:
        return "La placa no tiene el formato correcto.\nFormato correcto: letras y números, por ejemplo: ABC123"
    if placa.isdigit() or placa.isalpha():
        return "La placa debe combinar letras y números.\nFormato correcto: ABC123"
    for caracter in placa:
        if caracter.isalnum()==False:
            return "La placa solo puede contener letras y números.\nFormato correcto: ABC123"
    if marca=="":
        return "Debe ingresar la marca del vehículo.\nFormato correcto: Toyota, Nissan, Hyundai"
    if marca.isdigit():
        return "La marca no puede ser solamente numérica.\nFormato correcto: Toyota, Nissan, Hyundai"
    for caracter in marca:
        if caracter.isalpha()==False and caracter!=" ":
            return "La marca solo puede contener letras.\nFormato correcto: Toyota, Nissan, Hyundai"
    if color=="":
        return "Debe ingresar el color del vehículo.\nFormato correcto: rojo, blanco, negro"
    if color.isdigit():
        return "El color no puede ser numérico.\nFormato correcto: rojo, blanco, negro"
    for caracter in color:
        if caracter.isalpha()==False and caracter!=" ":
            return "El color solo puede contener letras.\nFormato correcto: rojo, blanco, negro"
    if tipo=="":
        return "Debe ingresar el tipo del vehículo.\nFormato correcto: carro, moto, camion, bus, suv"
    tiposValidos=["carro","moto","camion","bus","suv","pickup","automovil","motocicleta"]
    if tipo.lower() not in tiposValidos:
        return "El tipo de vehículo no tiene el formato correcto.\nFormato correcto: carro, moto, camion, bus, suv o pickup"
    if ubicacion=="":
        return "Debe ingresar la ubicación del vehículo.\nFormato correcto: G1, G2, G3"
    if ubicacion[0]!="G":
        return "La ubicación no tiene el formato correcto.\nFormato correcto: G1, G2, G3"
    numero=ubicacion[1:]
    if numero=="":
        return "La ubicación debe incluir un número.\nFormato correcto: G1, G2, G3"
    if numero.isdigit()==False:
        return "La ubicación debe llevar la letra G seguida de un número.\nFormato correcto: G1, G2, G3"
    configuracion=cargarConfiguracionAux()
    if configuracion==False or configuracion[0]<=0:
        return "Debe configurar primero el tamaño del estacionamiento."
    if int(numero)<1 or int(numero)>configuracion[0]:
        return "La ubicación no existe dentro del estacionamiento.\nTamaño actual: "+str(configuracion[0])+"\nFormato correcto: G1 hasta G"+str(configuracion[0])
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

#Funcion Aux de la opcion 2c del menu
def validarRetirarVehiculoAux(pPlaca):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la placa del vehículo
    -Salida:
        Se devuelve True si la placa es válida o un mensaje de error
    '''
    if pPlaca.strip()=="":
        return "Debe ingresar la placa del vehículo."
    return True

#Funcion Aux de la opcion 2c del menu
def buscarVehiculoObjetoPlacaAux(pEstacionamiento,pPlaca):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista del estacionamiento y la placa a buscar
    -Salida:
        Se devuelve el vehículo encontrado o False si no existe
    '''
    for vehiculo in pEstacionamiento:
        if vehiculo.placa==pPlaca:
            return vehiculo
    return False

#Funcion Aux de la opcion 2c del menu
def obtenerFechaHoraSalidaAux():
    '''
    Funcionamiento:
    -Entrada:
        No recibe datos
    -Salida:
        Se devuelve la fecha y hora actual como salida
    '''
    actual=time.localtime()
    return time.strftime("%d/%m/%Y %H:%M",actual)

#Funcion Aux de la opcion 2c del menu
def convertirFechaMinutosAux(pFecha):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe una fecha en formato dd/mm/yyyy hh:mm
    -Salida:
        Se devuelve la fecha convertida a minutos
    '''
    dia=int(pFecha[0:2])
    mes=int(pFecha[3:5])
    anno=int(pFecha[6:10])
    hora=int(pFecha[11:13])
    minuto=int(pFecha[14:16])
    total=0
    total+=anno*525600
    total+=mes*43200
    total+=dia*1440
    total+=hora*60
    total+=minuto
    return total

#Funcion Aux de la opcion 2c del menu
def calcularTiempoPermanenciaAux(pFechaEntrada,pFechaSalida):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la fecha de entrada y la fecha de salida
    -Salida:
        Se devuelve la cantidad de minutos que estuvo el vehiculo
    '''
    entrada=convertirFechaMinutosAux(pFechaEntrada)
    salida=convertirFechaMinutosAux(pFechaSalida)
    minutos=salida-entrada
    if minutos<0:
        minutos=0
    return minutos

#Funcion Aux de la opcion 2c del menu
def calcularMontoSalidaAux(pVehiculo):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el vehiculo
    -Salida:
        Se devuelve una lista con minutos, minutos cobrados, horas cobradas y monto a pagar
    '''
    configuracion=obtenerConfiguracionAux()
    tiempoGracia=configuracion[1]
    if tiempoGracia<0:
        tiempoGracia=0
    minutos=calcularTiempoPermanenciaAux(pVehiculo.fechaEntrada,pVehiculo.fechaSalida)
    minutosCobrados=minutos-tiempoGracia
    if minutosCobrados<=0:
        horas=0
        monto=0
    else:
        horas=minutosCobrados/60
        if horas>int(horas):
            horas=int(horas)+1
        else:
            horas=int(horas)
        monto=horas*pVehiculo.montoHora
    return [minutos,minutosCobrados,horas,round(monto,2)]

#Funcion Aux de la opcion 3a del menu
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

#Funcion Aux de la opcion 3a del menu
def guardarConfiguracionAux(pTamanno):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el tamaño del estacionamiento a guardar
    -Salida:
        Se guarda la configuración en memoria secundaria
    '''
    configuracion=obtenerConfiguracionAux()
    configuracion[0]=pTamanno
    archivo=open("configuracion.dat","wb")
    pickle.dump(configuracion,archivo)
    archivo.close()

#Funcion Aux de la opcion 3a del menu
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

#Funcion Aux de la opcion 3b del menu
def validarMontoHoraAux(pMonto):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el monto por hora escrito por el usuario
    -Salida:
        Se devuelve True si el dato es válido o un mensaje indicando el formato correcto
    '''
    if pMonto.strip()=="":
        return "Debe ingresar el monto por hora.\nFormato correcto: número positivo, por ejemplo: 1000 o 1000.50"
    try:
        monto=round(float(pMonto),2)
    except:
        return "El monto por hora debe escribirse con números.\nFormato correcto: 1000 o 1000.50"
    if monto<=0:
        return "El monto por hora debe ser mayor a 0.\nFormato correcto: 1000 o 1000.50"
    return True

#Funcion Aux de la opcion 3b del menu
def guardarMontoHoraAux(pMonto):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el monto por hora
    -Salida:
        Se guarda el monto por hora en la configuración del sistema
    '''
    configuracion=obtenerConfiguracionAux()
    configuracion[2]=round(float(pMonto),2)
    archivo=open("configuracion.dat","wb")
    pickle.dump(configuracion,archivo)
    archivo.close()
    return True

#Funcion Aux de la opcion 3c del menu
def validarTiempoGraciaAux(pTiempo):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el tiempo de gracia escrito por el usuario
    -Salida:
        Se devuelve True si el dato es valido o un mensaje de error
    '''
    if pTiempo.strip()=="":
        return "Debe ingresar el tiempo de gracia.\nFormato correcto: número entero positivo, por ejemplo: 15"
    try:
        tiempo=int(pTiempo)
    except:
        return "El tiempo de gracia debe escribirse con números enteros.\nFormato correcto: 15"
    if tiempo<0:
        return "El tiempo de gracia no puede ser negativo.\nFormato correcto: 0, 5, 10, 15"
    return True

#Funcion Aux de la opcion 3c del menu
def guardarTiempoGraciaAux(pTiempo):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el tiempo de gracia en minutos
    -Salida:
        Se guarda el tiempo de gracia en la configuracion del sistema
    '''
    configuracion=obtenerConfiguracionAux()
    configuracion[1]=pTiempo
    archivo=open("configuracion.dat","wb")
    pickle.dump(configuracion,archivo)
    archivo.close()

#Funcion Aux de la opcion 4 del menu
def obtenerNombreTipoPagoAux(pTipoPago):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe el número del tipo de pago
    -Salida:
        Se devuelve el nombre del tipo de pago
    '''
    if pTipoPago==1:
        return "Efectivo"
    if pTipoPago==2:
        return "Tarjeta"
    if pTipoPago==3:
        return "SINPE"
    return "Sin pago"

#Funcion Aux de la opcion 4 del menu
def obtenerMontoPagadoAux(pVehiculo):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe un vehículo
    -Salida:
        Se devuelve el monto pagado del vehículo
    '''
    if hasattr(pVehiculo,"montoPagado") and pVehiculo.montoPagado>0:
        return pVehiculo.montoPagado
    datosPago=calcularMontoSalidaAux(pVehiculo)
    pVehiculo.montoPagado=datosPago[3]
    return pVehiculo.montoPagado

#Funcion Aux de la opcion 4a del menu
def calcularCierreDiarioAux(pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista del estacionamiento
    -Salida:
        Se devuelve la información completa del cierre diario
    '''
    registros=[]
    totalGeneral=0
    efectivoCantidad=0
    efectivoTotal=0
    tarjetaCantidad=0
    tarjetaTotal=0
    sinpeCantidad=0
    sinpeTotal=0
    for vehiculo in pEstacionamiento:
        if vehiculo.fechaSalida=="":
            vehiculo.fechaSalida=obtenerFechaHoraSalidaAux()
        if vehiculo.tipoPago==0:
            vehiculo.tipoPago=random.randint(1,3)
        monto=obtenerMontoPagadoAux(vehiculo)
        tipoPago=obtenerNombreTipoPagoAux(vehiculo.tipoPago)
        registros.append([vehiculo.ubicacion,vehiculo.placa,vehiculo.fechaEntrada,vehiculo.fechaSalida,tipoPago,monto])
        totalGeneral+=monto
        if vehiculo.tipoPago==1:
            efectivoCantidad+=1
            efectivoTotal+=monto
        elif vehiculo.tipoPago==2:
            tarjetaCantidad+=1
            tarjetaTotal+=monto
        elif vehiculo.tipoPago==3:
            sinpeCantidad+=1
            sinpeTotal+=monto
    return [registros,round(totalGeneral,2),efectivoCantidad,round(efectivoTotal,2),tarjetaCantidad,round(tarjetaTotal,2),sinpeCantidad,round(sinpeTotal,2)]

#Funcion Aux de la opcion 4b del menu
def calcularCierreTipoPagoAux(pEstacionamiento):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista del estacionamiento
    -Salida:
        Se devuelve la información separada por tipo de pago
    '''
    efectivo=[]
    tarjeta=[]
    sinpe=[]
    for vehiculo in pEstacionamiento:
        if vehiculo.fechaSalida!="":
            monto=obtenerMontoPagadoAux(vehiculo)
            registro=[vehiculo.ubicacion,vehiculo.placa,vehiculo.marca,vehiculo.color,vehiculo.tipo,vehiculo.fechaEntrada,vehiculo.fechaSalida,monto]
            if vehiculo.tipoPago==1:
                efectivo.append(registro)
            elif vehiculo.tipoPago==2:
                tarjeta.append(registro)
            elif vehiculo.tipoPago==3:
                sinpe.append(registro)
    return [efectivo,tarjeta,sinpe]

#Funcion Aux de la opcion 4b del menu
def limpiarTextoXmlAux(pTexto):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe un texto
    -Salida:
        Se devuelve el texto preparado para XML
    '''
    texto=str(pTexto)
    texto=texto.replace("&","&amp;")
    texto=texto.replace("<","&lt;")
    texto=texto.replace(">","&gt;")
    return texto

#Funcion Aux de la opcion 4b del menu
def guardarCierreTipoPagoXmlAux(pDatos):
    '''
    Funcionamiento:
    -Entrada:
        Se reciben los datos separados por tipo de pago
    -Salida:
        Se genera el archivo cierreTipoPago.xml
    '''
    archivo=open("cierreTipoPago.xml","w",encoding="utf-8")
    archivo.write("<cierreTipoPago>\n")
    nombres=["efectivo","tarjeta","sinpe"]
    contador=0
    while contador<len(pDatos):
        archivo.write("  <"+nombres[contador]+">\n")
        for vehiculo in pDatos[contador]:
            archivo.write("    <vehiculo>\n")
            archivo.write("      <ubicacion>"+limpiarTextoXmlAux(vehiculo[0])+"</ubicacion>\n")
            archivo.write("      <placa>"+limpiarTextoXmlAux(vehiculo[1])+"</placa>\n")
            archivo.write("      <marca>"+limpiarTextoXmlAux(vehiculo[2])+"</marca>\n")
            archivo.write("      <color>"+limpiarTextoXmlAux(vehiculo[3])+"</color>\n")
            archivo.write("      <tipo>"+limpiarTextoXmlAux(vehiculo[4])+"</tipo>\n")
            archivo.write("      <fechaEntrada>"+limpiarTextoXmlAux(vehiculo[5])+"</fechaEntrada>\n")
            archivo.write("      <fechaSalida>"+limpiarTextoXmlAux(vehiculo[6])+"</fechaSalida>\n")
            archivo.write("      <monto>"+limpiarTextoXmlAux(vehiculo[7])+"</monto>\n")
            archivo.write("    </vehiculo>\n")
        archivo.write("  </"+nombres[contador]+">\n")
        contador+=1
    archivo.write("</cierreTipoPago>")
    archivo.close()
    return "cierreTipoPago.xml"

#Funcion Aux de la opcion 4b del menu
def calcularTotalListaPagoAux(pLista):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe una lista de vehículos de un tipo de pago
    -Salida:
        Se devuelve el total acumulado
    '''
    total=0
    for vehiculo in pLista:
        total+=vehiculo[7]
    return round(total,2)

#Funcion Aux de la opcion 4c del menu
def guardarCierreDiarioDatAux(pDatos):
    '''
    Funcionamiento:
    -Entrada:
        Se reciben los datos del cierre diario
    -Salida:
        Se guarda el cierre diario en memoria secundaria
    '''
    archivo=open("cierreDiario.dat","wb")
    pickle.dump(pDatos,archivo)
    archivo.close()

#Funcion Aux de la opcion 4c del menu
def cargarCierreDiarioDatAux():
    '''
    Funcionamiento:
    -Entrada:
        No recibe datos
    -Salida:
        Se devuelve el cierre diario guardado o False si no existe
    '''
    try:
        archivo=open("cierreDiario.dat","rb")
        datos=pickle.load(archivo)
        archivo.close()
        return datos
    except:
        return False

#Funcion Aux de la opcion 4c del menu
def exportarCierreDiarioCsvAux():
    '''
    Funcionamiento:
    -Entrada:
        No recibe datos
    -Salida:
        Se genera un archivo CSV con el cierre diario sin encabezados
    '''
    datos=cargarCierreDiarioDatAux()
    nombre="cierreDiario_"+obtenerFechaArchivoAux()+".csv"
    archivo=open(nombre,"w",encoding="utf-8")
    for registro in datos[0]:
        archivo.write(str(registro[0])+","+str(registro[1])+","+str(registro[2])+","+str(registro[3])+","+str(registro[4])+","+str(registro[5])+"\n")
    archivo.close()
    return nombre

#Funcion Aux para validar reportes
def validarDatosReporteAux(pEstacionamiento,pConfiguracion):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la lista del estacionamiento y la configuración del sistema
    -Salida:
        Se devuelve True si se puede generar el reporte o un mensaje indicando qué falta
    '''
    if len(pEstacionamiento)==0:
        return "No se puede generar el reporte porque no hay vehículos cargados."
    if pConfiguracion==False:
        return "No se puede generar el reporte porque no existe configuración guardada."
    if pConfiguracion[0]<=0:
        return "No se puede generar el reporte porque falta configurar el tamaño del estacionamiento."
    if pConfiguracion[2]<=0:
        return "No se puede generar el reporte porque falta configurar el monto por hora."
    return True

#Funcion Aux para validar tiempo de gracia en reportes
def validarTiempoGraciaReporteAux(pConfiguracion):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la configuración del sistema
    -Salida:
        Se devuelve True si el tiempo de gracia está configurado o False si falta
    '''
    if pConfiguracion==False:
        return False
    if pConfiguracion[1]<0:
        return False
    return True

#Funcion Aux para establecer tiempo de gracia en cero
def establecerTiempoGraciaCeroAux(pConfiguracion):
    '''
    Funcionamiento:
    -Entrada:
        Se recibe la configuración actual del sistema
    -Salida:
        Se guarda el tiempo de gracia en 0 sin cambiar los demás datos
    '''
    pConfiguracion[1]=0
    archivo=open("configuracion.dat","wb")
    pickle.dump(pConfiguracion,archivo)
    archivo.close()

#Funcion Aux para validar exportacion a CSV
def validarExportarCierreDiarioCsvAux():
    '''
    Funcionamiento:
    -Entrada:
        No recibe datos
    -Salida:
        Se devuelve True si existe el cierre diario o un mensaje indicando por qué no puede continuar
    '''
    try:
        archivo=open("cierreDiario.dat","rb")
        archivo.close()
        return True
    except:
        return "No se puede exportar a CSV porque todavía no existe un cierre diario generado."