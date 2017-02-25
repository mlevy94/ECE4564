#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
mess = sys.argv[1]

while mess != "quit":
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=mess)
    print(" [x] Sent", mess)
    mess = raw_input('Message to send: ')
    
connection.close()
