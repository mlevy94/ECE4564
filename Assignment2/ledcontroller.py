from RPi import GPIO
import queue
import threading

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
        if GPIO.input(self.SPECIAL_SWITCH): # Complex output
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
        else: # Simple output
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
      
      

      
      
