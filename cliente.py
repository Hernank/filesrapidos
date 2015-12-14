# -*- coding: utf-8 -*-
from socket import socket
from threading import Thread

estado = True

class Response(Thread):
    global estado
    def __init__(self, conexion):
        Thread.__init__(self)
        self.conexion = conexion

    def run(self):
        while True:
            input_data = self.conexion.recv(1024)
            if input_data.decode("utf-8") == "0xFFFF000OK": # Codigo que significa el termino de una conexion
                global estado
                print("saliendo.. [ENTER]")
                estado = False
                return
            print(input_data.decode("utf-8") if
                  isinstance(input_data, bytes) else input_data)

def main():
    global estado
    enchufe = socket()
    enchufe.connect(("45.55.156.19", 8000))
    nombre = input(":::> Escriba su nombre de usuario: ")
    enchufe.send(("!!! \"{0}\" se ha conectado".format(nombre)).encode("utf-8"))
    listen = Response(enchufe)
    listen.start()
    while True:
        if estado == False:
            exit()
        output_data = "-> {0}: {1}".format(nombre,input(""))
        if output_data:
            # Enviar entrada. Comptabilidad con Python 3.
            try:
                enchufe.send(output_data.encode("utf-8"))
            except TypeError:
                enchufe.send(bytes(output_data, "utf-8"))
                
if __name__ == "__main__":
    main()
