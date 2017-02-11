#!/usr/etc/python3.4
import wolframalpha
import sys

app_id=('LE4G2J-TTLEL59TJ2')
client=wolframalpha.Client(app_id) # Establishes connection with WolframAlpha API
query = ' '.join(sys.argv[1:]) # Captures cmd line arguements as query
print("Query sent to Wolfram Alpha API:", query)
res = client.query(query) # Submits question to WolframAlpha and stores the response
print("Response:", next(res.results).text)

    
