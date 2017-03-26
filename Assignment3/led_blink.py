import RPi.GPIO as GPIO
import time

def blink(seconds):
    while(seconds > 0):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(4,GPIO.OUT)
        print ("LED on")
        GPIO.output(4,GPIO.HIGH)
        time.sleep(1)
        print ("LED off")
        GPIO.output(4,GPIO.LOW)
        seconds = seconds - 1;

if __name__ == "__main__":
    blink(5)