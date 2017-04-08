import RPi.GPIO as GPIO
import time


class playerLed:

    def gettoken(self):
        return self.token

    def incrementtoken(self):
        self.token += 1
        return self.token

    def addplayer(self):
        self.numplayers += 1
        return self.numplayers

    def getplayer(self):
        return self.numplayers

    def __del__(self):
        GPIO.cleanup()

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(4, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)
        self.token = 0
        self.numplayers = 0

    def color(self):
        col = self.token % 3

        if col == 1:
            GPIO.output(17,GPIO.LOW)
            GPIO.output(27,GPIO.LOW)
            GPIO.output(4,GPIO.HIGH)

        elif col == 2:
            GPIO.output(4,GPIO.LOW)
            GPIO.output(27,GPIO.LOW)
            GPIO.output(17,GPIO.HIGH)

        else:
            GPIO.output(4, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)


if __name__ == "__main__":
    color(0)
