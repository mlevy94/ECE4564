import RPi.GPIO as GPIO
import time

def color(player):
	GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4,GPIO.OUT)
	GPIO.setup(17,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)
	
	col = player % 3;
	
	if col == 0:
		GPIO.output(17,GPIO.LOW)
		GPIO.output(27,GPIO.LOW)
		GPIO.output(4,GPIO.HIGH)
	
    else if col == 1:
		GPIO.output(4,GPIO.LOW)
		GPIO.output(27,GPIO.LOW)
		GPIO.output(17,GPIO.HIGH)
		
	else:
		GPIO.output(4,GPIO.LOW)
		GPIO.output(17,GPIO.LOW)
		GPIO.output(27,GPIO.HIGH)
		
	finally:
		GPIO.cleanup()

if __name__ == "__main__":
    color(0)