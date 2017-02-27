#!/usr/bin/env python3
import argparse
import json
import sys
import MongoDB
import pika
from ledcontroller import LEDController




if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-b", action="store", default="localhost")
  parser.add_argument("-p", action="store", default="/")
  parser.add_argument("-c", action="store", default=None)
  parser.add_argument("-k", action="store", nargs=2, default=["pi1", "pi2"])
  fields = parser.parse_args(sys.argv[1:])
  
  led = LEDController()
  mongoClient = MongoDB.Client()
  mongoClient.create_client()

  if fields.c is not None:
    login, password = fields.c.split(":")
    credentials = pika.PlainCredentials(login, password)
    parameters = pika.ConnectionParameters(fields.b,
                                       5672,
                                       fields.p,
                                       credentials)
  else:                 #attempt to login as guest
    parameters = pika.ConnectionParameters('localhost')
  
  connection = pika.BlockingConnection(parameters)  #need error handling
  
  try:
    host1 = fields.k[0]
  except IndexError:
    host1 = None
    
  try:
    host2 = fields.k[1]
  except IndexError:
    host2 = None


  def consumeData(ch, method, properties, body):
    message = json.loads(body).decode()
    mongoClient.mongo_insert(method.routing_key, message)
    if led.host_select() ^ (method.routing_key == host1):
      led.queue.put(message["cpu"])
      
  if host1 is not None:
    channel1 = connection.channel()
    channel1.exchange_declare(exchange='pi_utilization',
                             type='direct')
    result1 = channel1.queue_declare(exclusive=True)
    queue_name1 = result1.method.queue
    channel1.queue_bind(exchange='pi_utilization',
                        queue=queue_name1,
                        routing_key=host1)
    channel1.basic_consume(consumeData,
                      queue=queue_name1,
                      no_ack=True)
    channel1.start_consuming()
  
  if host2 is not None:
    channel2 = connection.channel()
    channel2.exchange_declare(exchange='pi_utilization',
                              type='direct')
    result2 = channel2.queue_declare(exclusive=True)
    queue_name2 = result2.method.queue
    channel2.queue_bind(exchange='pi_utilization',
                        queue=queue_name2,
                        routing_key=host2)
    channel2.basic_consume(consumeData,
                          queue=queue_name2,
                          no_ack=True)
    channel2.start_consuming()

  input("Press any key to end")
    
  
