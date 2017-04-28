from sockcomm import SockClient, SockServer
from time import sleep

host = input("host ip: ")
client = SockClient()
outMessage = input("message to send: ")
client.send(outMessage)

servsock, finalMessage = client.recv()
