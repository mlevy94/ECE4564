#!/usr/bin/env python
import pika
import argparse
import time
import sys
import json

parser = argparse.ArgumentParser()
parser.add_argument("-b", action="store", default="localhost")
parser.add_argument("-p", action="store", default="/")
parser.add_argument("-c", action="store", default=None)
parser.add_argument("-k", action="store", required=True)
fields = parser.parse_args(sys.argv[1:])
  
if fields.c is not None:
  i = 0
  while fields.c[i] != ':':  #parse login credentials
    i+=1
  login = fields.c[:i]
  password = fields.c[i+1:]
  credentials = pika.PlainCredentials(login, password)
  parameters = pika.ConnectionParameters(fields.b,
                                       5672,
                                       fields.p,
                                       credentials)

else:                 #attempt to login as guest
  parameters = pika.ConnectionParameters('localhost')
  
connection = pika.BlockingConnection(parameters)  #need error handling

channel = connection.channel()
channel.exchange_declare(exchange='pi_utilization',
                         type='direct')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='pi_utilization',
                   queue=queue_name,
                   routing_key=fields.k)

def callback(ch, method, properties, body):
    #import pdb; pdb.set_trace()
    print(" [x] Received ", json.loads(body.decode()))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
