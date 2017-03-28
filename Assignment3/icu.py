import argparse
import requests
import ephem
import datetime
import math
import zipcode
import geocoder
import json
import pygame
import sched
import time
from twilio.rest import TwilioRestClient
from threading import Thread
import RPi.GPIO as GPIO
from textwrap import dedent

# harcoded tle's

tle1 = ("0 TECHSAT 1B (GO-32)",
        "1 25397U 98043D   17083.85494572 -.00000014  00000-0  12820-4 0  9996",
        "2 25397  98.6023  28.0049 0000466 179.5244 180.5936 14.23617620971570")
isstle = ("ISS (ZARYA)",
          "1 25544U 98067A   17085.86699654  .00002420  00000-0  43611-4 0  9991",
          "2 25544  51.6419  88.6361 0007310 341.9191  96.9999 15.54263976 48954")

eventData = dedent("""\
    Date/time: {}
    Visible: {}
    Rise azimuth: {:.4f}
    Set azimuth: {:.4f}
    Pass duration: {:.2f}\
    """)

#================alerts==========================
def blink(seconds):
    try:
        while(seconds > 0):
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(4,GPIO.OUT)
            GPIO.output(4,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(4,GPIO.LOW)
            seconds = seconds - 2
            time.sleep(1)
    finally:
        GPIO.cleanup()


def play(songname, window):
    start = time.time()
    pygame.mixer.init()
    pygame.mixer.music.load(songname)
    while time.time() - start <= window:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        time.sleep(1)


def textme(message):
    client = TwilioRestClient("AC53dbff6bf8a76f141fb50a6d37d96223",
                              "7b04a0394a3ca7022d7d34a655b43a8f")
    client.messages.create(to="+18604717675", from_="+19592008885",
                           body= "Satellite alert: " + message)

def sendAlert(event, window):
    textme(eventData.format(event[0], event[1], event[2], event[3], event[4]/60))
    t1 = Thread(target=blink, args=(window,))
    t2 = Thread(target=play, args=('trap.wav',window,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
#================end alert=================================
#================PyEphem Functions=========================
def seconds_between(d1, d2):
    return abs((d2 - d1).seconds)


def datetime_from_time(tr):
    year, month, day, hour, minute, second = tr.tuple()
    dt = datetime.datetime(year, month, day, hour, minute, int(second))
    return dt


def get_next_pass(lon, lat, alt, tle):
    sat = ephem.readtle(tle.text.splitlines()[0], tle.text.splitlines()[1], tle.text.splitlines()[2])

    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.long = str(lon)
    observer.elevation = alt
    observer.pressure = 0
    observer.horizon = '-0:34'

    now = datetime.datetime.utcnow()
    observer.date = now

    seenCount = 0
    seenList = [None] * 5

    for day in range(15):
        for veiwing in range(15):
            sat.compute(observer)
            if sat.neverup is False and sat.circumpolar is False:
                tr, azr, tt, altt, ts, azs = observer.next_pass(sat)
            else:
                print("The satellite ", tle.text.splitlines()[0], " never passes the horizon, try another one!")
                exit(0)

            duration = int((ts - tr) * 60 * 60 * 24)
            rise_time = datetime_from_time(tr)
            max_time = datetime_from_time(tt)
            set_time = datetime_from_time(ts)

            observer.date = max_time

            sun = ephem.Sun()
            sun.compute(observer)
            sat.compute(observer)

            sun_alt = math.degrees(sun.alt)

            # checks for visibiliy and checks if the weather is clear
            visible = False
            if sat.eclipsed is False and -18 < math.degrees(sun_alt) < -6 \
                    and getWeather(str(fields.zip), ephem.localtime(tr)) < 20:
                visible = True
            if visible:
                seenList[seenCount] = (tr, visible, math.degrees(azr), math.degrees(azs), duration)
                seenCount += 1
                if seenCount == 5:
                    break
                observer.date = ts
            else:
                observer.date = ts
    observer.date = observer.date + 1

    if seenCount != 5:
        print('Due to weather, ', seenCount, ' sightings possible in the next 15 days')
    for passing in range(seenCount):
        print(dedent("""\
        Pass number: {}
        {}
        """).format(passing + 1, eventData).format(
            seenList[passing][0],
            seenList[passing][1],
            seenList[passing][2],
            seenList[passing][3],
            seenList[passing][4] / 60)
        )

    return seenCount, seenList  # {
    #          "rise_time": calendar.timegm(rise_time.timetuple()),
    #          "rise_azimuth": math.degrees(azr),
    #          "max_time": calendar.timegm(max_time.timetuple()),
    #          "max_alt": math.degrees(altt),
    #          "set_time": calendar.timegm(set_time.timetuple()),
    #          "set_azimuth": math.degrees(azs),
    #          "elevation": sat.elevation,
    #          "sun_alt": sun_alt,
    #          "duration": duration,
    #          "visible": visible
    #
    #        }

#====================End PyEphem Functions============================

#================openweather=====================
fiveDay = "http://api.openweathermap.org/data/2.5/forecast?zip={zip},us&APPID={key}"

sixteenDay = "http://api.openweathermap.org/data/2.5/forecast/daily?zip={zip},us&cnt=16&APPID={key}"

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
        return 100
    
#============= Satelite Function===========
def getSatelite():
    # get satellite
    # credentials used for space-track
    usr = 'Huntw94@vt.edu'
    psw = 'Redmoney424242*'
    # query for 3le information
    query = 'https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/{}/orderby/NORAD_CAT_ID ASC/format/3le'.format(
        fields.satellite)

    # payload info for 3le
    payload = {'identity': usr, 'password': psw, 'query': query}

    # request response
    thrleresp = requests.post('https://www.space-track.org/ajaxauth/login', payload)

    # error checking for failed response
    if (thrleresp.status_code != 200):
        print("an error has occured. Error {}".format(thrleresp.status_code))
    else:
        print("Satelite TLE information:")
        print(thrleresp.text.splitlines()[1])
        print(thrleresp.text.splitlines()[2])
    return thrleresp
#  ===================end ====================

def scheduleAlerts(alerts, res):
    s = sched.scheduler()
    for alert, result in zip(alerts, res):
        aTime = alert.timestamp() - time.time() - 900 
        aTime = aTime if aTime > 0 else 0
        alertDuration = 900 if aTime > 900 else aTime
        s.enter(aTime, 1, sendAlert, argument=[result, alertDuration])
        print("Event happening in {} seconds".format(aTime))
    s.run()

if __name__ == "__main__":
    # Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-z", "--zip", action="store", default="24060")
    parser.add_argument("-s", "--satellite", action="store", default="25397")
    fields = parser.parse_args()

    # get satellite
    tle = getSatelite()

    myzip = zipcode.isequal(fields.zip)
    print("For zipcode: ", fields.zip)
    print("Latitude: ", str(myzip.lat))
    print("Longitude: ", str(myzip.lon))

    # ======================PyEphem===========================================
    # get visibility data
    # find altitude
    alt = geocoder.google([myzip.lat, myzip.lon], method='elevation')

    alerttime = []
    count, res = get_next_pass(myzip.lat, myzip.lon, alt.meters, tle)
    for c in range(count):
        value = ephem.localtime(res[c][0])
        alerttime.append(value)
    # set alarms

    timedel = datetime.timedelta(minutes=15)
    i = 0
    
    scheduleAlerts(alerttime, res)

