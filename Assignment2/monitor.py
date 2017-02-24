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
  SPECIAL_SWITCH = 17
  SPECIAL_SWITCH_ON = 27
  HOST_SWITCH = 16
  HOST_SWITCH_ON = 20
  
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((self.BLUE, self.RED, self.GREEN, self.SPECIAL_SWITCH_ON, self.HOST_SWITCH_ON), GPIO.OUT)
    GPIO.output((self.BLUE, self.RED, self.GREEN), False)
    GPIO.setup((self.SPECIAL_SWITCH, self.HOST_SWITCH), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    self.greenPWM = GPIO.PWM(self.GREEN, 120)
    self.redPWM = GPIO.PWM(self.RED, 120)
    self.queue = queue.Queue()
    
  def host_select(self):
    return GPIO.input(self.HOST_SWITCH)

  def modLED(self):
    self.greenPWM.start(0)
    self.redPWM.start(0)
    GPIO.output(self.SPECIAL_SWITCH_ON, True)
    GPIO.output(self.HOST_SWITCH_ON, True)
    try:
      while True:
        val = self.queue.get()
        if GPIO.input(self.SPECIAL_SWITCH):
          if self.minVal <= val < self.divPoint2:
            greenVal = 100 - ((val - self.minVal) / (self.divPoint2 - self.minVal) * 100.0)
          else:
            greenVal = 0.0
          if self.divPoint1 < val <= self.maxVal:
            redVal = (val - self.divPoint1) / (self.maxVal - self.divPoint1) * 100.0
          else:
            redVal = 0.0
        else:
          greenVal = 0.0
          redVal = 0.0
          if val <= self.divPoint2:
            greenVal = 100.0
          if val >= self.divPoint1:
            redVal = 100.0
        print("Red: {} Green: {}".format(redVal, greenVal))
        self.redPWM.ChangeDutyCycle(redVal)
        self.greenPWM.ChangeDutyCycle(greenVal)
    finally:
      self.redPWM.stop()
      self.greenPWM.stop()
      
  def __exit__(self, exc_type, exc_val, exc_tb):
    GPIO.cleanup()
      
      

      
      
