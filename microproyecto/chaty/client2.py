import socket
import sys

HOST, PORT = "127.0.0.1", 8000
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def enviarmensaje(sock,mensaje):
	sock.connect((HOST, PORT))
	#sock.sendall("socket_abierto" + "\n")
	sock.sendall(mensaje)
	return sock

while True:	    
	try:
		midata=raw_input("Ingrese mensaje")
		# Connect to server and send data
		enviarmensaje(sock, midata)
		print "me conecte"
		# Receive data from the server and shut down
		received = sock.recv(1024)
		print received

		if received=="cambio_nuevo":
			sock.close
			print "consultar a la pagina principal http"
			print "ejecuto nueva orden"
			sucess=True 
			if sucess:
				enviarmensaje(sock, "sucess !! id= 123")
			else:
				enviarmensaje(sock, "error !! id=123")
	except Exception as ex:
		sock.close()
		print "me desconecte(error no controlado)"+ex.message
	else:
		pass
	finally:
		sock.close()
		print "me desconecte"
	print "Sent:     {}".format(data)
	print "Received: {}".format(received)