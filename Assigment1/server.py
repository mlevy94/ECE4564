#!/usr/etc/python3.4
import wolframalpha
from sockcomm import SockServer
from md5auth import createMD5, authMD5
import socket


#Establish connection 
app_id=('LE4G2J-TTLEL59TJ2')
waClient=wolframalpha.Client(app_id) # Establishes connection with WolframAlpha API
if waClient:
    print("Established connection with Wolfram API")

addr = "0.0.0.0"
port = 51000

server = SockServer(addr=addr, port=port)
print("Listening on {}:{}".format(socket.gethostbyname(socket.gethostname()), port))

while 1:
    client, (recvMD5, query) = server.recv()
    if not authMD5(recvMD5, query):
        raise Exception("Bad MD5")
    #query = ' '.join(sys.argv[1:]) # Captures cmd line arguements as query
    print("Query sent to Wolfram Alpha API:", query)
    res = waClient.query(query[0]) # Submits question to WolframAlpha and stores the response
    if res["@error"]: # Wait for response
        print("Response:", next(res.results).text)
        returnText = next(res.results).text
        ret = returnText.split('\n')
        md5 = createMD5(ret)
        server.send((md5, ret), client)

    
