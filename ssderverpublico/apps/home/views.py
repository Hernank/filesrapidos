
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# 
import socket
import sys


import urllib2


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