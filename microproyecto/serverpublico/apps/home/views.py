
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# 
import socket
import sys


import urllib2
import json 

def enviarmensaje(mensaje):
	HOST, PORT = "127.0.0.1", 8000
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))
	sock.sendall(mensaje)
	
	print "enviando mensaje"
	
	return sock

def setsocket(request,variable):
	
	
	midata="localserver,"+variable
		# Connect to server and send data
	
	sock=enviarmensaje( midata)
	received = sock.recv(1024)
	sock.close()

	return HttpResponse("jajaj "+received)

def dashboard(request):

	template='home/index.html'
	valores,sensores=getvalores()

	ctx={'hola':"hola",'valores':valores,'sensores':sensores}
	return render(request,template,ctx)
def setvalor(request):
	#import pdb; pdb.set_trace()
	nombre =str(request.GET['nombre'])
	if str(request.GET['valor'])=='false':
		valor=False
	else:
		valor=True
	midata="hostpublic,setdata,"+nombre+","+str(valor)
		# Connect to server and send data
	received		=""
	datosrecibidos	=""
	sock=""
	try:
		sock=enviarmensaje( midata)
		received = sock.recv(1024)
		datosrecibidos=received.split(',')[-1]
	except Exception as ex :
		mensaje="Ha ocurrido un error de conexion al server socket"
		payload = {'error':mensaje}
		#sock.close()

		return HttpResponse(json.dumps(payload), content_type='application/json'	)
	else:
		pass
	finally:
		#sock.close()	
		pass
	mensaje="Muy bien muchachito"
	payload = {'mensaje':mensaje}


	return HttpResponse(json.dumps(payload), content_type='application/json')




def getvalores():

	data=[]
	midata="hostpublic,getdata,"
		# Connect to server and send data
	#import pdb; pdb.set_trace()
	valores={'Alarma':False,'Ventilador 1':False,'Ventilador 2':False,'Radio 1':False,'Foco':False,
		'Arbol':False,'Servos':False,}
	received=''
	datosrecibidos=""
	sock=""
	try:
		sock=enviarmensaje( midata)
		received = sock.recv(1024)
		datosrecibidos=received.split(',')[-1]
		sock.close()
		
	except Exception as  ex:
		#sock.close()
		print "Ha ocurrido un error de conexion al server sock "+str(ex.args[0])+":"+ex.args[1]
		sensores={'temperatura':0,'alarma':0,"mensajeerror":"Ha ocurrido un error de conexion al server sock ",}
		return valores,sensores
		
	else:
		pass
	finally:
		pass
		#sock.close()
	

	
	#import pdb; pdb.set_trace()
	miboleano={'0':False,'1':True}
	
	
	valores['Alarma']=miboleano[datosrecibidos[0]]
	valores['Ventilador 1']=miboleano[datosrecibidos[1]]
	valores['Ventilador 2']=miboleano[datosrecibidos[2]]
	valores['Radio 1']=miboleano[datosrecibidos[3]]
	valores['Foco']=miboleano[datosrecibidos[4]]
	valores['Arbol']=miboleano[datosrecibidos[5]]
	valores['Servos']=miboleano[datosrecibidos[6]]
	
	valortemperatura=datosrecibidos.split('-')[-2]
	valorsensor=datosrecibidos.split('-')[-1]
	if valorsensor=='1':
		valorsensor=True 
	elif valorsensor=='0':
		valorsensor=False

	
	sensores={'temperatura':valortemperatura,'alarma':valorsensor}
	return valores,sensores
	