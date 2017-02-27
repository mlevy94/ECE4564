#!/usr/bin/env python3
import argparse
import time
import json
import pika
from pika import exceptions
from collections import OrderedDict


# Used for grabbing the system stats off the RPi. WARNING: only works in Linux.
class SysStats:
  
  # Get initial readings for baseline.
  def __init__(self):
    # Initialize cpu reading
    self._getCPUTimes()
    # Initialize network utilization
    self._getNetStats()
    
  # Helper function to read and update CPU values.
  def _getCPUTimes(self):
    with open('/proc/stat') as f:
      fields = [float(column) for column in f.readline().strip().split()[1:]]
    self.idle, self.total = fields[3], sum(fields)
    
  # Gets CPU values and returns system load.
  def getCPU(self):
    # below formula taken from notes.
    last_idle = self.idle
    last_total = self.total
    self._getCPUTimes()
    idle_delta, total_delta = self.idle - last_idle, self.total - last_total
    return 1.0 - idle_delta / total_delta
  
  # Helper function to read network statistics
  def _getNetStats(self):
    interfaces = OrderedDict()
    with open('/proc/net/dev') as f:
      f.readline() # useless. Ignore
      f.readline() # useless. Ignore
      # 1 Interface per line. Grab all of them.
      for lineStr in f.readlines():
        line = lineStr.split()
        interfaces[line[0].replace(":", "")] = {
          # Just grabbing the bytes fields
          "rx":int(line[1]),
          "tx":int(line[9]),
        }
    self.netStats = interfaces
    self.checkTime = time.time() # storing time for rate calculations
    
  # Grabs net stats and outputs rates for tx/rx for each interface.
  def getNetStats(self):
    last_netStats = self.netStats
    last_checkTime = self.checkTime
    self._getNetStats()
    delta_time = self.checkTime - last_checkTime
    netstats = OrderedDict()
    # Calculate rates for tx/rx of each interface.
    for interface, value in self.netStats.items():
      last_value = last_netStats[interface]
      netstats[interface] = {
        "rx": int((value["rx"] - last_value["rx"]) / delta_time),
        "tx": int((value["tx"] - last_value["tx"]) / delta_time),
      }
    return netstats
  
  # Groups cpu and net stats into a single dict and outputs them.
  def getStats(self):
    return OrderedDict((
      ("cpu", self.getCPU()),
      ("net", self.getNetStats()),
    ))
    

if __name__ == "__main__":
  # Command Line Arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("-b", action="store", default="localhost")
  parser.add_argument("-p", action="store", default="/")
  parser.add_argument("-c", action="store", default=None)
  parser.add_argument("-k", action="store", required=True)
  fields = parser.parse_args()
  
  try:
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
  
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange='pi_utilization',
                            type='direct')
    stats = SysStats()
    while True:
      time.sleep(1) # Keep first to avoid divide by 0 error
      # Grab stats
      message = stats.getStats()
      print(message)
      # send stats
      channel.basic_publish(exchange='pi_utilization',
                        routing_key=fields.k,
                        body=json.dumps(message))
      
  except KeyboardInterrupt:
    pass
  except exceptions.ConnectionClosed:
    print("Connection closed by server.")
  finally:
    print("Shutting Down.")
