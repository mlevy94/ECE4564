import argparse
import requests
import zipcode
import datetime
import xmltodict
import datetime
import requests # needs to be installed
import json
# import RPi.GPIO as GPIO
import time
# import pygame
# import twilio
# import twilio.rest
# from twilio.rest import TwilioRestClient
# from threading import Thread


# OpenWeather API code
# ===================================================================================================
fiveDay = "http://api.openweathermap.org/data/2.5/forecast?zip={zip},us&APPID={key}"
sixteenDay = "http://api.openweathermap.org/data/2.5/forecast/daily?zip={zip},us&cnt=16&APPID={key}"

zip = 24060

apiKey = "231ea1f95f5b7e73a482ffcdc9772060"

def getWeather(zipcode, startTime):
  if isinstance(startTime, float):
    startTime = datetime.datetime.utcfromtimestamp(startTime)
  request = sixteenDay.format(zip=zipcode, key=apiKey)
  answer = requests.get(request)
  if not answer.ok:
    raise ConnectionError("Bad API Response: code {}, request: {}".format(answer.status_code, request))
  forcastList = json.loads(answer.text)["list"]
  targetDay = None
  for day in forcastList:
    forcastDate = datetime.datetime.fromtimestamp(day["dt"])
    if forcastDate.date() == startTime.date():
      targetDay = day
      break
  try:
    return targetDay["clouds"]
  except TypeError:
    return None
# ===================================================================================================

# Event notifiaction code
# ===================================================================================================
# def blink(seconds):
#     while(seconds > 0):
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setwarnings(False)
#         GPIO.setup(4,GPIO.OUT)
#         GPIO.output(4,GPIO.HIGH)
#         time.sleep(1)
#         GPIO.output(4,GPIO.LOW)
#         seconds = seconds - 2;
#         time.sleep(1)
#
#
# def play(songname, window):
#     start = time.time()
#     pygame.mixer.init()
#     pygame.mixer.music.load(songname)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy() and time.time() - start < window:
#         continue
#
#
# def textme(message):
#     client = TwilioRestClient("AC53dbff6bf8a76f141fb50a6d37d96223",
#                               "7b04a0394a3ca7022d7d34a655b43a8f")
#     client.messages.create(to="+18604717675", from_="+19592008885",
#                            body= "Satellite alert: " + message)
#
#
# def alert(message, window):
#     textme(message)
#     t1 = Thread(target=blink, args=(window,))
#     t2 = Thread(target=play, args=('trap.wav',window,))
#     t1.start()
#     t2.start()
# ======================================================================================================

if __name__ == "__main__":
    # Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-z", "--zip", action="store", default="24060")
    parser.add_argument("-s", "--satellite", action="store", default="25544")
    fields = parser.parse_args()

    # get satellite
    usr = 'Huntw94@vt.edu'
    psw = 'Redmoney424242*'
    query = 'https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/{}/orderby/NORAD_CAT_ID ASC/format/3le'.format(
        fields.satellite)
    query2 = 'https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/{}/orderby/NORAD_CAT_ID ASC/format/tle'.format(
        fields.satellite)
    payload = {'identity': usr, 'password': psw, 'query': query}
    payload2 = {'identity': usr, 'password': psw, 'query': query2}
    r = requests.post('https://www.space-track.org/ajaxauth/login', payload)
    q = requests.post('https://www.space-track.org/ajaxauth/login', payload2)
    if (q.status_code != 200):
        print("an error has occured. Error {}".format(r.status_code))
    else:
        print(q.text)

    myzip = zipcode.isequal(fields.zip)
    print('Latitude:',str(myzip.lat))
    print('Longitude:',str(myzip.lon))

    # Print 15 day cloud coverage forecast
    # ===================================================================================================
    t = time.time()
    day = 0
    print("")
    while day < 15:
        timestamp = t + day * 86400
        value = datetime.datetime.fromtimestamp(timestamp)
        print(value.strftime('%Y-%m-%d %H:%M:%S'), 'clouds:', str(getWeather('06066', timestamp)) + '%')
        day += 1

# set alarms
#     n = 0
#     while(1):
#         if datetime.time() == view[n]:
#             alert(message[n], 900)
#             n+=1
#         time.sleep(1)