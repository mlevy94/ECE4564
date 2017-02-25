import argparse
import time
import sys

class SysStats:
  
  def __init__(self):
    # Initialize cpu reading
    self._getCPUTimes()
    # Initialize network utilization
    
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
    interfaces = {}
    with open('/proc/net/dev') as f:
      f.readline() # useless. Ignore
      f.readline() # useless. Ignore
      for lineStr in f.readlines():
        line = lineStr.split()
        interfaces[line[0]] = {
          "rx":line[1],
          "tx":line[9]
        }
    self.netStats = interfaces
    self.checkTime = time.time()
    
  def getNetStats(self):
    last_netStats = self.netStats
    last_checkTime = self.checkTime
    self._getNetStats()
    delta_time = self.checkTime - last_checkTime
    netstats = {}
    for interface, value in self.netStats:
      last_value = last_netStats[interface]
      netstats[interface] = {
        "rx": int((value["rx"] - last_value["rx"]) / delta_time),
        "tx": int((value["tx"] - last_value["tx"]) / delta_time),
      }
    return netstats
  
  
  def getStats(self):
    return {
      "net": self.getNetStats(),
      "cpu": self.getCPU(),
    }
    

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-b", action="store", default="localhost")
  parser.add_argument("-p", action="store", default="/")
  parser.add_argument("-c", action="store", default=None)
  parser.add_argument("-k", action="store", required=True)
  fields = parser.parse_args(sys.argv)
  import pdb; pdb.set_trace()
