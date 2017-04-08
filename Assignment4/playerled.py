import RPi.GPIO as GPIO
import time


class playerLed:

    token = 0
    numPlayers = 0

    def gettoken(self):
        return token

    def incrementtoken(self):
        token += 1

    def addplayer(self):
        numPlayers += 1

    def __del__(self):
        GPIO.cleanup()

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(4, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)

    def color(self):
        col = token % 3

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
