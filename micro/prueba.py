import SocketServer
server="ola"
class MyTCPHandler():
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """


    def handle(self):
        # self.request is the TCP socket connected to the client
        global server        
        server="bueo ya lo modifique"


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    print "<>"+server
    server="cambio1"
    print server
    j=MyTCPHandler()
    j.handle()
    print server





