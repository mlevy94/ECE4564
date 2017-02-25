#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('ECE4564', 'team13')
parameters = pika.ConnectionParameters('jacques',5672,'/',credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
