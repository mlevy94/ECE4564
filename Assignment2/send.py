#!/usr/bin/env python
import pika
import sys


credentials = pika.PlainCredentials('ECE4564', 'team13')
parameters = pika.ConnectionParameters('jacques',5672,'/',credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')
mess = sys.argv[1]

while mess != "quit":
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=mess)
    print(" [x] Sent", mess)
    mess = input('Message to send: ')
    
connection.close()
