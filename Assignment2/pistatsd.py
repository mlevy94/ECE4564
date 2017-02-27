#!/usr/bin/env python3
import argparse
import time
import sys
import json
import pika
from collections import OrderedDict


class SysStats:
  
  def __init__(self):
    # Initialize cpu reading
    self._getCPUTimes()
    # Initialize network utilization
    self._getNetStats()
    
  def _getCPUTimes(self):
    with open('/proc/stat') as f:
      fields = [float(column) for column in f.readline().strip().split()[1:]]
    self.idle, self.total = fields[3], sum(fields)
    
  def getCPU(self):
    last_idle = self.idle
    last_total = self.total
    self._getCPUTimes()
    idle_delta, total_delta = self.idle - last_idle, self.total - last_total
    return 1.0 - idle_delta / total_delta
  
  def _getNetStats(self):
    interfaces = OrderedDict()
    with open('/proc/net/dev') as f:
      f.readline() # useless. Ignore
      f.readline() # useless. Ignore
      for lineStr in f.readlines():
        line = lineStr.split()
        interfaces[line[0].replace(":", "")] = {
          "rx":int(line[1]),
          "tx":int(line[9]),
        }
    self.netStats = interfaces
    self.checkTime = time.time()
    
  def getNetStats(self):
    last_netStats = self.netStats
    last_checkTime = self.checkTime
    self._getNetStats()
    delta_time = self.checkTime - last_checkTime
    netstats = OrderedDict()
    for interface, value in self.netStats.items():
      last_value = last_netStats[interface]
      netstats[interface] = {
        "rx": int((value["rx"] - last_value["rx"]) / delta_time),
        "tx": int((value["tx"] - last_value["tx"]) / delta_time),
      }
    return netstats
  
  
  def getStats(self):
    return OrderedDict((
      ("cpu", self.getCPU()),
      ("net", self.getNetStats()),
    ))
    

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-b", action="store", default="localhost")
  parser.add_argument("-p", action="store", default="/")
  parser.add_argument("-c", action="store", default=None)
  parser.add_argument("-k", action="store", required=True)
  fields = parser.parse_args(sys.argv[1:])
  
  ######### rabbitMQ Init code goes here #########
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
  stats = SysStats()
  while True:
    time.sleep(1) # Keep first to avoid divide by 0 error
    message = stats.getStats()
    print(message)
    channel.basic_publish(exchange='pi_utilization',
                      routing_key=fields.k,
                      body=json.dumps(message))
