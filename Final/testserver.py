from sockcomm import SockClient, SockServer
from time import sleep
server = SockServer('0.0.0.0')

sock, inMessage = server.recv()
print("Server recieved message: ", inMessage)
