import RPi.GPIO as GPIO
import time
import pygame
from twilio.rest import TwilioRestClient
from threading import Thread


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
        seconds = seconds - 2;
        time.sleep(1)


def play(songname, window):
    start = time.time()
    pygame.mixer.init()
    pygame.mixer.music.load(songname)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() and time.time() - start < window:
        continue


def textme(message):
    client = TwilioRestClient("AC53dbff6bf8a76f141fb50a6d37d96223",
                              "7b04a0394a3ca7022d7d34a655b43a8f")
    client.messages.create(to="+18604717675", from_="+19592008885",
                           body= "Satellite alert: " + message)

def alert(message, window):
    textme(message)
    t1 = Thread(target=blink, args=(window,))
    t2 = Thread(target=play, args=('trap.wav',window,))

if __name__ == '__main__':
    alert('this is a test', 10)
