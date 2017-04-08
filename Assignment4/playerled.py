import RPi.GPIO as GPIO
import time


class playerLed:

    def gettoken(self):
        if self.turn == -1:
            return 0
        return (self.turn % self.numplayers) + 1

    def incrementturn(self):
        self.turn += 1

    def getturn(self):
        return self.turn

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
        self.turn = 0
        self.numplayers = 0

    def color(self):
        try:
            col = self.gettoken()
        except ZeroDivisionError:
            col = 0

        if col == -1:
            GPIO.output(4, GPIO.HIGH)
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(27, GPIO.HIGH)

        elif col == 1:
            GPIO.output(17,GPIO.LOW)
            GPIO.output(27,GPIO.LOW)
            GPIO.output(4,GPIO.HIGH)

        elif col == 2:
            GPIO.output(4,GPIO.LOW)
            GPIO.output(27,GPIO.LOW)
            GPIO.output(17,GPIO.HIGH)

        elif col == 3:
            GPIO.output(4, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)

        else:
            GPIO.output(4, GPIO.LOW)
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)


if __name__ == "__main__":
    color(0)
