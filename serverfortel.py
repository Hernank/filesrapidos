from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore

PORT = 8000
NAME = '127.0.0.1'

class ChatSession(async_chat):
	def __init__(self,server,sock):
		print "init chat sesion"
		async_chat.__init__(self, sock)
		self.server = server
		self.set_terminator("\r\n")
		self.data = []

	def collect_incoming_data(self, data):
		print "collect"
		self.data.append(data)

	def found_terminator(self):
		print "found_terminator"
		line = ''.join(self.data)
		self.data = []
		self.server.broadcast(line)

	def handle_close(self):
		print "hanclose"
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
		print "disclnect server"
		self.sessions.remove(sessions)

	def broadcast(self, line):
		print "send broad"
		for session in self.sessions:
			session.push('>>' + line +"\r\n" )

	def handle_accept(self):
		print "handle close"
		conn, addr = self.accept()
		self.sessions.append(ChatSession(self, conn))

if __name__ == "__main__":
	print "iniciadndo"
	s = ChatServer(PORT, NAME)
	try:asyncore.loop()
	except KeyboardInterrupt:print "-.-"

