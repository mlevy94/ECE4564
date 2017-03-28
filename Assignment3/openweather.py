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
  
  
if __name__ == "__main__":
  import time
  ret = getWeather(zip, time.time())
  print(ret)
  
