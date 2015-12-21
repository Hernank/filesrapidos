from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore

PORT = 8000
NAME = '127.0.0.1'

class ChatSession(async_chat):
	def __init__(self,server,sock):
		print "Init chat sesion"
		async_chat.__init__(self, sock)
		self.server = server
		self.set_terminator("\r\n")
		self.data = []
		##import pdb; pdb.set_trace()
		self.ipremote=sock.getpeername()[0]
		self.portremote=sock.getpeername()[1]
		print self.ipremote+"-"+str(self.portremote)
		self.nombre="xxx"
		

	def collect_incoming_data(self, data):
		print "collect ." +data

		self.data.append(data)
		##import pdb; pdb.set_trace()
		self.nombre=data.split(',')[0]
		print "El valor es === "+data
		if "getdata" in data :
			print "x getdata"
			self.found_terminator_except_i()
		if "setdata" in data :
			print "x setdata"

			self.found_terminator_except_i()
		if "success" in data :
			print "x success"

			self.found_terminator_except_i()
		if "error" in data :
			print "x error"

			self.found_terminator_except_i()



	def found_terminator(self):
		print "found_terminator"
		line = ''.join(self.data)
		self.data = []
		self.server.broadcast(line)

	def found_terminator_except_i(self):
		print "found_terminator"
		line = ''.join(self.data)
		self.data = []
		self.server.broadcast_except_i(self,line)


	def handle_close(self):
		print "3.hanclose"
		async_chat.handle_close(self)

		self.server.disconnect(self)

class ChatServer(dispatcher):
	def __init__(self, port, name):
		print "inti chat server"
		dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		print name 
		print port
		self.bind((name,port))
		self.listen(5)
		self.name = name
		self.sessions = []

	def disconnect(self, sessions):
		print "disclnect server"+sessions.nombre
		self.sessions.remove(sessions)

	def broadcast(self, line):
		print "send broad"
		for session in self.sessions:
			session.push(line)
	def broadcast_except_i(self,misession_i ,line):
		print "send broad except"
		for session in self.sessions:
			##import pdb; pdb.set_trace()
			if not(session.ipremote == misession_i.ipremote and  session.portremote == misession_i.portremote):
				print "enviando broad a "+misession_i.ipremote+" - "+str(misession_i.portremote)
				session.push(line )

				



	def handle_accept(self):
		print "1handle accept"
		conn, addr = self.accept()
		self.sessions.append(ChatSession(self, conn))
		self.listarnodos()
		#self.broadcast("Bienvenido")
		#
	def listarnodos(self):
		print"   =====" 
		for sesion in self.sessions:
			print sesion.ipremote+" - "+str(sesion.portremote)+"-"+sesion.nombre
		print "=========="

if __name__ == "__main__":
	print "iniciadndo"
	s = ChatServer(PORT, NAME)
	try:asyncore.loop()
	except KeyboardInterrupt:print "-.-"

