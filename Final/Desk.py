from RPi import GPIO
from sockcomm import SockServer
from time import sleep
import serial
import queue
import threading
import json


class Desk:
  
  # control pins
  controlPIN = 19
  directionPIN = 26
  
  # desk values
  minHeight = 29
  maxHeight = 48
  
  minHeightVal = 555
  maxHeightVal = 917
  
  # serial device
  serDev = '/dev/ttyACM0'
  
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((self.controlPIN, self.directionPIN), GPIO.OUT)
    self.queue = queue.Queue()
    self.heightThread = threading.Thread(target=self._getHeight, daemon=True)
    self.adjustThread = threading.Thread(target=self._setHeights, daemon=True)
    self.heightThread.start()
    self.adjustThread.start()
    self.lock = threading.Lock()
    self.currHeight = self.minHeight
    
  def __del__(self):
    GPIO.cleanup()
    
  def getHeight(self):
    with self.lock:
      return ((self.currHeight - self.minHeightVal) / (self.maxHeightVal - self.minHeightVal)) * \
             (self.maxHeight - self.minHeight) + self.minHeight
  
  def setHeight(self, height):
    with self.lock:
      self.currHeight = height
      
  def _setHeights(self):
    while True:
      height = self.queue.get()
      print("Received height: {}".format(height))
      if not isinstance(height, int):
        height = int(height)
      if height < self.minHeight:
        height = self.minHeight
      elif height > self.maxHeight:
        height = self.maxHeight
      GPIO.output(self.directionPIN, height > self.getHeight())
      print("Direction Pin {}!".format("On" if height > self.getHeight() else "Off"))
      if height < self.getHeight():
        heightCheck = lambda: height <= self.getHeight()
      else:
        heightCheck = lambda: height >= self.getHeight()
      GPIO.output(self.controlPIN, True)
      while heightCheck():
        print("Current Height: {}".format(self.getHeight()))
        sleep(0.25)
      print("Height Reached!")
      GPIO.output(self.controlPIN, False)
      self.queue.task_done()
      
  def _getHeight(self):
    ser = serial.Serial(self.serDev, 9600)
    while True:
      try:
        height = int(ser.readline())
        self.setHeight(height)
      except ValueError:
        pass
    
    
if __name__ == "__main__":
  try:
    desk = Desk()
    server = SockServer(addr="0.0.0.0")
    print("Waiting for clients to connect.")
    while True:
      msg = server.recv()[1]
      desk.queue.put(json.loads(msg)["height"])
  finally:
    GPIO.cleanup()

