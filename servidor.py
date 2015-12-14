# -*- coding: utf-8 -*-
from socket import socket, error
from threading import Thread

hilos = []

# Hilo para escucha activa/continua de cada socket
class Listening(Thread):
    def __init__(self,conexion):
        Thread.__init__(self)
        self.conexion = conexion
        self.estado = True        

    def run(self):
        while True:
            l = list(filter(lambda x: x.cliente == self.conexion,hilos)) # Selecciona el socket correcto que corresponda con el socket actual, de la lista de sockets
            input_data = l[0].cliente.recv(1024)
            if not input_data:
                print("[%s] Error de lectura." % self.name)
                return
            else:
                texto = input_data.decode("utf-8") if isinstance(input_data, bytes) else input_data
                if texto[texto.find(":") + 2:] == "s": # Determinar si el caracter enviado fue una "s"
                    if input("El usuario \"{0}\" desea salir (Y/N): ".format(texto[texto.find("->")+2:texto.find(":")])) == "Y":
                        self.estado = False
                        l[0].cliente.send("0xFFFF000OK".encode("utf-8")) # Codigo inventado para el envio de señal de cierre de conexión
                    else:
                        l[0].cliente.send("No se ha permitido el cierre de conexion".encode("utf-8"))
                else:
                    print(texto)
                    # print(hilos) # Muestra los hilos con sockets que existen actualmente

                # Previene errores en iteracion con sockets cerrados, se salta el envio a los demas sockets :(
                try:
                    for cliente in hilos:
                        cliente.cliente.send(input_data)
                except:
                    pass

# Hilo para envio continuo de cada socket
class Client(Thread):
    def __init__(self, cliente, direccion):
        # Inicializar clase padre.
        Thread.__init__(self)
        self.cliente = cliente
        self.direccion = direccion

    def run(self):
        listening = Listening(self.cliente)
        listening.start()
        while True:                
            # Previene I/O Error causado por socket cerrados
            # Recibir datos del cliente.
            if(listening.estado == False):
            	listening.join()
            	return
            else:
                output_data = input("")
                if output_data:
                    try:
                        for cliente in hilos:
                            cliente.cliente.send(output_data.encode("utf-8"))
                    except TypeError:
                        for cliente in hilos:
                            cliente.cliente.send(bytes(output_data,"utf-8"))
                    
def main():
    enchufe = socket()
    # Escuchar peticiones en el puerto 6030.
    enchufe.bind(("45.55.156.19", 8000))
    enchufe.listen(6)

    while True:
        cliente, direccion = enchufe.accept()
        c = Client(cliente, direccion)
        hilos.append(c)
        c.start()

        print("!!! %s:%d se ha conectado." % (direccion))

    for t in hilos:
        t.join()

if __name__ == "__main__":
    main()