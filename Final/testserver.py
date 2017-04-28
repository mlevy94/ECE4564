from sockcomm import SockClient, SockServer
from time import sleep
server = SockServer()

sock, inMessage = server.recv()
print("Server recieved message: ", inMessage)
