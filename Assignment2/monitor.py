from RPi import GPIO
import queue

class LEDController:
  
  maxVal = 1.0
  minVal = 0.0
  divPoint1 = (maxVal - minVal) / 4 + minVal
  divPoint2 = (maxVal - minVal) * 3 / 4 + minVal
  
  RED = 25
  GREEN = 24
  BLUE = 23
  
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((self.BLUE, self.RED, self.GREEN), GPIO.OUT)
    self.greenPWM = GPIO.PWM(self.GREEN, 120)
    self.redPWM = GPIO.PWM(self.RED, 120)
    self.queue = queue.Queue()
    

  def modLED(self):
    self.greenPWM.start(0)
    self.redPWM.start(0)
    try:
      while True:
        val = self.queue.get()
        if self.minVal < val <= self.divPoint2:
          redVal = (val - self.minVal) / (self.divPoint2 - self.minVal) * 100.0
        else:
          redVal = 0.0
        if self.divPoint1 < val <= self.maxVal:
          greenVal = (val - self.divPoint1) / (self.maxVal - self.divPoint1) * 100.0
        else:
          greenVal = 0.0
        self.redPWM.ChangeDutyCycle(redVal)
        self.greenPWM.ChangeDutyCycle(greenVal)
    finally:
      self.redPWM.stop()
      self.greenPWM.stop()
      
  def __exit__(self, exc_type, exc_val, exc_tb):
    GPIO.cleanup()
      
      

      
      
