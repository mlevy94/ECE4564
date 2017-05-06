from RPi import GPIO
from sockcomm import SockServer
from time import sleep
import pyserial
import queue
import threading


class Desk:
  
  # control pins
  controlPIN = 19
  directionPIN = 26
  
  # desk values
  minHeight = 20
  maxHeight = 70
  
  # serial device
  serDev = '/dev/tty/ACM0'
  
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
      return self.currHeight
  
  def setHeight(self, height):
    with self.lock:
      self.currHeight = height
      
  def _setHeights(self):
    while True:
      height = self.queue.get()
      if height < self.minHeight:
        height = self.minHeight
      elif height > self.maxHeight:
        height = self.maxHeight
      GPIO.output(self.directionPIN, height > self.getHeight())
      if height > self.getHeight():
        heightCheck = lambda self: height <= self.getHeight()
      else:
        heightCheck = lambda self: height >= self.getHeight()
      GPIO.output(self.controlPIN, True)
      while heightCheck():
        sleep(0.25)
      GPIO.output(self.controlPIN, False)
      self.queue.task_done()
      
  def _getHeight(self):
    serial = pyserial.Serial(self.serDev, 9600)
    while True:
      height = serial.readline()
      self.setHeight(height)
      
    
    

if __name__ == "__main__":
  desk = Desk()
  server = SockServer(addr="0.0.0.0")
  desk.queue.put(server.recv()[1])
