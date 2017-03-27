import argparse
import requests
import zipcode
import datetime
import xmltodict


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
print(str(myzip.lat))
print(str(myzip.lon))

call = 'https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php? \
whichClient=NDFDgenMultiZipCode&lat=&lon=&listLatLon=&lat1=&lon1=&lat2=&lon2=&resolutionSub=&listLat1=&listLon1=&listLat2=&listLon2=&resolutionList=&endPoint1Lat=&endPoint1Lon=&endPoint2Lat=&endPoint2Lon=&listEndPoint1Lat=&listEndPoint1Lon=&listEndPoint2Lat=&listEndPoint2Lon=& \
zipCodeList={zip}&listZipCodeList=&centerPointLat=&centerPointLon=&distanceLat=&distanceLon=&resolutionSquare=&listCenterPointLat=&listCenterPointLon=&listDistanceLat=&listDistanceLon=&listResolutionSquare=&citiesLevel=&listCitiesLevel=&sector=&gmlListLatLon=&featureType=&requestedTime=&startTime=&endTime=&compType=&propertyName=&product= \
time-series&begin={start}&end={end}&Unit=e&sky=sky&wx=wx&Submit=Submit'

zip = fields.zip

begin = '2017-03-20T02:55:00'.replace(":", "%3A")

end = '2017-03-20T03:10:00'.replace(":", "%3A")

timestring = '%Y-%m-%dT%H:%M:00'

timedel = datetime.timedelta(minutes=15)


def getSkyCover(zipcode, starttime):
  if isinstance(starttime, float):
    starttime = datetime.datetime.utcfromtimestamp(starttime)
  endtime = starttime + timedel
  print("Checking for times: {} to {}".format(starttime.strftime(timestring), endtime.strftime(timestring)))
  answer = requests.get(call.format(
    zip=zipcode,
    start=starttime.strftime(timestring).replace(":", "%3A"),
    end=endtime.strftime(timestring).replace(":", "%3A"),
  ))
  xmlAnswer = xmltodict.parse(answer.text)
  parameters = xmlAnswer["dwml"]["data"]["parameters"]
  return parameters["cloud-amount"]["value"]


if __name__ == "__main__":
  import time

  ret = getSkyCover(zip, time.time())
  print(ret, "CLEAR" if int(ret) <= 20 else "NOT CLEAR")

  
# set alarms
