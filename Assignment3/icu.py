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






# set alarms
