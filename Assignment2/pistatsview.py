#!/usr/bin/env python
import argparse
import json
import sys
import threading
from ledcontroller import LEDController



def consumeData(routingKey, controller, switchPosition=True):
  while True:
    # recv message as message
    # convert to json
    # add to database
    if controller.host_select == switchPosition:
      controller.queue.put(message["cpu"])







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
    recvThread1 = threading.Thread(target=consumeData, args=[host1, led, True], daemon=True)
    recvThread1.start()
  except IndexError:
    host1 = None
    recvThread1 = None
    
  try:
    host2 = fields.k[1]
    recvThread2 = threading.Thread(target=consumeData, args=[host2, led, False], daemon=True)
  except IndexError:
    host2 = None
    recvThread2 = None
    recvThread2.start()
    
  input()
    
  
