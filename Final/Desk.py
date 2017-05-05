from RPi import GPIO
from sockcomm import SockServer
import queue
import threading


class Desk:
  
  # control pins
  controlPIN = 19
  directionPIN = 26
  heightPIN = 3
  sensePIN = 2
  
  # desk values
  minHeight = 20
  maxHeight = 70
  
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((self.controlPIN, self.directionPIN, self.heightPIN), GPIO.OUT)
    GPIO.setup(self.sensePIN, GPIO.IN)
    self.heightPWM = GPIO.PWM(self.heightPIN, 1000)
    self.heightPWM.start(0)
    self.queue = queue.Queue()
    self.heightThread = threading.Thread(target=self._setHeights, daemon=True)
    self.heightThread.start()
    
  def __del__(self):
    self.heightPWM.stop()
    GPIO.cleanup()
    
  def setTargetHeight(self, height):
    if self.minHeight < height < self.maxHeight:
      self.heightPWM.ChangeDutyCycle((height - self.minHeight)/(self.maxHeight - self.minHeight))
      return True
    return False
      
  def _setHeights(self):
    while True:
      height = self.queue.get()
      if self.setTargetHeight(height):
        GPIO.output(self.directionPIN, GPIO.input(self.sensePIN))
        GPIO.output(self.controlPIN, True)
        GPIO.wait_for_edge(self.sensePIN, GPIO.BOTH, timeout=30000)
        GPIO.output(self.controlPIN, False)
      self.queue.task_done()
    

if __name__ == "__main__":
  desk = Desk()
  server = SockServer(addr="0.0.0.0")
  desk.queue.put(server.recv()[1])
