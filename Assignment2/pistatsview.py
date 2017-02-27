#!/usr/bin/env python3
import argparse
import json
import sys
import MongoDB
import pika
from ledcontroller import LEDController
from collections import OrderedDict




if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-b", action="store", default="localhost")
  parser.add_argument("-p", action="store", default="/")
  parser.add_argument("-c", action="store", default=None)
  parser.add_argument("-k", action="store", required=True)
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


  def consumeData(ch, method, properties, body):
    message = json.loads(body.decode(), object_pairs_hook=OrderedDict)
    mongoClient.mongo_insert(method.routing_key, message)
    # if led.host_select() ^ (method.routing_key == host1):
    led.queue.put(message["cpu"])
      
  channel1 = connection.channel()
  channel1.exchange_declare(exchange='pi_utilization',
                           type='direct')
  result1 = channel1.queue_declare(exclusive=True)
  queue_name1 = result1.method.queue
  channel1.queue_bind(exchange='pi_utilization',
                      queue=queue_name1,
                      routing_key=fields.k)
  channel1.basic_consume(consumeData,
                    queue=queue_name1,
                    no_ack=True)
  try:
    channel1.start_consuming()
  except KeyboardInterrupt:
    pass
  finally:
    print("Shutting Down")
    led.cleanup()
