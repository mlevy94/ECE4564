import twilio
import twilio.rest
from twilio.rest import TwilioRestClient

#for sms alerts
client = TwilioRestClient("AC53dbff6bf8a76f141fb50a6d37d96223", "7b04a0394a3ca7022d7d34a655b43a8f")

client.messages.create(to="+18604717675", from_="+19592008885", 
                       body= "this is a test")
