import datetime
import requests
import json


fiveDay = "http://api.openweathermap.org/data/2.5/forecast?zip={zip},us&APPID={key}"
sixteenDay = "http://api.openweathermap.org/data/2.5/forecast/daily?zip={zip},us&APPID={key}"

zip = 24060

apiKey = "327ac52ecbb2877d22adb0efdc283505"

def getWeather(zipcode, startTime):
  if isinstance(startTime, float):
    startTime = datetime.datetime.utcfromtimestamp(startTime)
  request = sixteenDay.format(zip=zipcode, key=apiKey)
  answer = requests.get(request)
  if not answer.ok:
    raise ConnectionError("Bad API Response: code {}, request: ".format(answer.status_code, request))
  forcastList = json.loads(answer.text)["list"]
  targetDay = None
  for day in forcastList:
    forcastDate = datetime.datetime.fromtimestamp(day["dt"])
    if forcastDate.date() == startTime.date():
      targetDay = day
      break
  import pdb; pdb.set_trace()
  try:
    return targetDay["clouds"]
  except TypeError:
    return None
  
  
if __name__ == "__main__":
  import time
  ret = getWeather(zip, time.time())
  print(ret)
  
