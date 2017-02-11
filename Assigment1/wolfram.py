#!/usr/etc/python3.4
import wolframalpha
import sys
from sockcomm import SockServer


#Establish connection 
app_id=('LE4G2J-TTLEL59TJ2')
client=wolframalpha.Client(app_id) # Establishes connection with WolframAlpha API
if client:
    print("Established connection with Wolfram API")

addr = "0.0.0.0"
port = 51000

server = SockServer(addr=addr, port=port)
print("Listening on {}:{}".format(addr, port))

while 1;
    question = server.recv()[1]
    #query = ' '.join(sys.argv[1:]) # Captures cmd line arguements as query
    if query: #Wait for Question
        print("Query sent to Wolfram Alpha API:", query)
        res = client.query(query) # Submits question to WolframAlpha and stores the response
        if res; # Wait for response 
            print("Response:", next(res.results).text)
            returnText = next(res.results).text
    else:
        print("Waiting for question")
    
