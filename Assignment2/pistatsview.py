#!/usr/bin/env python
import argparse
import json
import sys
import threading
from ledcontroller import LEDController








if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-b", action="store", default="localhost")
  parser.add_argument("-p", action="store", default="/")
  parser.add_argument("-c", action="store", default=None)
  parser.add_argument("-k", action="store", nargs=2, const=["pi1, pi2"], default=["pi1", "pi2"])
  fields = parser.parse_args(sys.argv[1:])
  
  led = LEDController()

  ######### rabbitMQ Init code goes here #########
  
  try:
    host1 = fields.k[0]
  except IndexError:
    host1 = None
    
  try:
    host2 = fields.k[1]
  except IndexError:
    host2 = None


  def consumeData(ch, method, properties, body):
    message = json.loads(body)
    # add to database
    if led.host_select() ^ (method.routing_key == host1):
      led.queue.put(message["cpu"])
      
  if host1 is not None:
    # channel declaration 1
  
  if host2 is not None:
    # channel declaration 2


  input()
    
  
