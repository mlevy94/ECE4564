#!/usr/bin/env python3
import argparse
import json
import pymongo
import pika
import time
import queue
import threading
from pika import exceptions
from collections import OrderedDict
from pymongo import MongoClient
from pymongo import errors
from RPi import GPIO


# Basic Class for controlling the LED
class LEDController:
  # Min, max, 25%, and 75% points
  maxVal = 1.0
  minVal = 0.0
  divPoint1 = (maxVal - minVal) / 4 + minVal
  divPoint2 = (maxVal - minVal) * 3 / 4 + minVal
  
  # Pinout
  RED = 4
  GREEN = 17
  BLUE = 27
  SPECIAL_SWITCH = 16
  SPECIAL_SWITCH_ON = 20
  HOST_SWITCH = 23
  HOST_SWITCH_ON = 24
  
  # setup the pins and led change thread
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((self.BLUE, self.RED, self.GREEN, self.SPECIAL_SWITCH_ON, self.HOST_SWITCH_ON), GPIO.OUT)
    GPIO.output((self.BLUE, self.RED, self.GREEN), False)
    GPIO.setup((self.SPECIAL_SWITCH, self.HOST_SWITCH), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # pwm for finer controls over the led output
    self.greenPWM = GPIO.PWM(self.GREEN, 120)
    self.redPWM = GPIO.PWM(self.RED, 120)
    self.queue = queue.Queue()
    self.ledThread = threading.Thread(target=self.modLED, daemon=True)
    self.ledThread.start()
  
  # see the position of the host select switch.
  def host_select(self):
    return GPIO.input(self.HOST_SWITCH)
  
  # change the led based on input value between min and max. Two different modes.
  def modLED(self):
    # start PWM and turn on switches.
    self.greenPWM.start(0)
    self.redPWM.start(0)
    GPIO.output(self.SPECIAL_SWITCH_ON, True)
    GPIO.output(self.HOST_SWITCH_ON, True)
    try:
      while True:
        val = self.queue.get()
        if GPIO.input(self.SPECIAL_SWITCH):  # Complex output
          # Green ranges in value from 100 at min to 0 at divPoint2.
          if self.minVal <= val < self.divPoint2:
            greenVal = 100 - ((val - self.minVal) / (self.divPoint2 - self.minVal) * 100.0)
          else:
            greenVal = 0.0
          # Red ranges in value from 0 at divPoint1 to 100 at max.
          if self.divPoint1 < val <= self.maxVal:
            redVal = (val - self.divPoint1) / (self.maxVal - self.divPoint1) * 100.0
          else:
            redVal = 0.0
        else:  # Simple output
          greenVal = 0.0
          redVal = 0.0
          if val <= self.divPoint2:
            greenVal = 100.0
          if val >= self.divPoint1:
            redVal = 100.0
        # print("Red: {} Green: {}".format(redVal, greenVal))
        self.redPWM.ChangeDutyCycle(redVal)
        self.greenPWM.ChangeDutyCycle(greenVal)
    finally:
      self.redPWM.stop()
      self.greenPWM.stop()
  
  # Cleans up the GPIO when done.
  def cleanup(self):
    GPIO.cleanup()

class Client:
  def __init__(self):
    self.client = None
    while self.client is None:
      try:
        self.client = MongoClient('localhost', 27017)
      except errors.ConnectionFailure:
        print("Failed to connect to MongoDB. Retrying in 1 second...")
        time.sleep(1)
    self.db = self.client.A2_database
    self.pi = self.db.pi_collection
  
  def mongo_insert(self, routing, js):
    pi_id = self.pi.insert_one({"Pi": routing, "info": js}).inserted_id
    
    print("\n{}:".format(routing))
    print("cpu: {} [Hi: {}, Lo: {}]".format(
      js["cpu"],
      next(self.pi.find({}).sort('info.cpu', pymongo.DESCENDING).limit(1))['info']['cpu'],
      next(self.pi.find({}).sort('info.cpu', pymongo.ASCENDING).limit(1))['info']['cpu'],
    ))
    
    for interface, rates in js["net"].items():
      rateStrings = []
      for rate in rates:
        rateStrings.append("{}={} B/s [Hi: {} B/s, Lo: {} B/s]".format(rate, js["net"][interface][rate],
                                                                       next(self.pi.find({"Pi": routing}).sort(
                                                                         "info.net.{}.{}".format(interface, rate),
                                                                         pymongo.ASCENDING).limit(1))["info"]["net"][
                                                                         interface][rate],
                                                                       next(self.pi.find({"Pi": routing}).sort(
                                                                         "info.net.{}.{}".format(interface, rate),
                                                                         pymongo.DESCENDING).limit(1))["info"]["net"][
                                                                         interface][rate],
                                                                       ))
      print("{}: {}".format(interface, ", ".join(rateStrings)))


if __name__ == "__main__":
  # Command Line Arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("-b", action="store", default="localhost")
  parser.add_argument("-p", action="store", default="/")
  parser.add_argument("-c", action="store", default=None)
  parser.add_argument("-k", action="store", required=True)
  fields = parser.parse_args()
  
  led = LEDController()
  mongoClient = Client()

  try:
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
    channel1.start_consuming()
  except KeyboardInterrupt:
    pass
  except exceptions.ConnectionClosed:
    print("Connection closed by server.")
  finally:
    print("Shutting Down.")
    led.cleanup()
