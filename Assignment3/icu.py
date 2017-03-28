import argparse
import requests
import zipcode
import datetime
import xmltodict
import ephem
import datetime
import math
import calendar
import zipcode
import geocoder


#================openweather=====================
import datetime
import requests # needs to be installed
import json


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
    return 100
#================openweather end=====================


if __name__ == "__main__":
    # Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-z", "--zip", action="store", default="24060")
    parser.add_argument("-s", "--satellite", action="store", default="25397")
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

    if (r.status_code != 200):
        print("an error has occured. Error {}".format(r.status_code))
    else:
        print(r.text)

    myzip = zipcode.isequal(fields.zip)
    print(str(myzip.lat))
    print(str(myzip.lon))

    # get visibility data
    #find altitude
    alt = geocoder.google([myzip.lat, myzip.lon], method='elevation')
    tle = q.text

def seconds_between(d1, d2):
    return abs((d2 - d1).seconds)

def datetime_from_time(tr):
    year, month, day, hour, minute, second = tr.tuple()
    dt = datetime.datetime(year, month, day, hour, minute, int(second))
    return dt

def get_next_pass(lon, lat, alt, tle):

    sat = ephem.readtle(r.text.splitlines()[0], r.text.splitlines()[1], r.text.splitlines()[2])

    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.long = str(lon)
    observer.elevation = alt
    observer.pressure = 0
    observer.horizon = '-0:34'

    now = datetime.datetime.utcnow()

    observer.date = now
    #print(now)
    seenCount = 0
    seenList = [None]*5

    for day in range(15):
        for veiwing in range(15):
            tr, azr, tt, altt, ts, azs = observer.next_pass(sat)



            duration = int((ts - tr) *60*60*24)
            rise_time = datetime_from_time(tr)
            max_time = datetime_from_time(tt)
            set_time = datetime_from_time(ts)

            observer.date = max_time

            sun = ephem.Sun()
            sun.compute(observer)
            sat.compute(observer)

            sun_alt = math.degrees(sun.alt)

            #checks for visibiliy and checks if the weather is clear
            visible = False
            if sat.eclipsed is False and -18 < math.degrees(sun_alt) < -6 \
                    and getWeather(str(fields.zip),ephem.localtime(tr)) < 20:
                visible = True
            if visible:
                visibleTime = float(calendar.timegm(rise_time.timetuple()))
                #print(tr, visible)

                seenList[seenCount] = (tr, visible, math.degrees(azr),math.degrees(azs), duration)
                seenCount += 1
                if seenCount == 5:
                    break
                observer.date = ts
            else:
                #print(tr, visible)
                observer.date = ts
    observer.date = observer.date + 1
    #print(seenCount)
    #print(seenList)
    
    if seenCount != 5:
        print('Do to weather, there are only' , seenCount, 'sightings possible in the next 15 days')
    for passing in range(seenCount):
        print("Pass number: ", passing+1)
        print("Date/time", seenList[passing][0])
        print("Visible: ", seenList[passing][1])
        print("Rise azimuth: ", seenList[passing][2])
        print("Set azimuth: ", seenList[passing][3])
        print("Pass duration: ", seenList[passing][4]/60)

    return seenCount, seenList #{
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

count, res = get_next_pass(myzip.lat, myzip.lon, alt.meters, tle)

for c in range(count):
    print(res[c])
# set alarms
