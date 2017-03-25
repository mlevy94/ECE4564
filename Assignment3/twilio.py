import subprocess
from time import sleep
from threading import Thread

activate_this_file = "/home/pi/sendsms/bin/activate_this.py"

execfile(activate_this_file, dict(__file__=activate_this_file))

from ISStreamer.Streamer import Streamer
import twilio
import twilio.rest
from twilio.rest import TwilioRestClient

#for sms alerts
client = TwilioRestClient("AC53dbff6bf8a76f141fb50a6d37d96223", "7b04a0394a3ca7022d7d34a655b43a8f")

# Edit these for how many people/devices you want to track
occupant = ["Jacques", "Matt", "Ray"]

# MAC addresses for our phones
address = ["24:f0:94:6b:fa:4e","bc:9f:ef:ba:1c:ae", "e0:b5:2d:df:21:dd"]

# Sleep once right when this script is called to give the Pi enough time
# to connect to the network
sleep(60)

# Initialize the Initial State streamer
# Be sure to add your unique access key
streamer = Streamer(bucket_name="Who's home", bucket_key="CXG7KL96HMBS", access_key="GYYFh9n7BJ9YGAmTyFDALZsIhDWUknrV")

# Some arrays to help minimize streaming and account for devices
# disappearing from the network when asleep
firstRun = [1] * len(occupant)
presentSent = [0] * len(occupant)
notPresentSent = [0] * len(occupant)
counter = [0] * len(occupant)

# Function that checks for device presence
def whosHere(i):

    # 30 second pause to allow main thread to finish arp-scan and populate output
    sleep(30)

    # Loop through checking for devices and counting if they're not present
    while True:

        # Exits thread if Keyboard Interrupt occurs
        if stop == True:
            print ("Exiting Thread")
            exit()
        else:
            pass

        # If a listed device address is present print and stream
        if address[i] in output:
            print(occupant[i] + "'s device is connected to your network")
            if presentSent[i] == 0:
                # Stream that device is present
                streamer.log(occupant[i],":office:")
                streamer.flush()
                print(occupant[i] + " present streamed")

                #send sms
                client.messages.create(to="+18604717675", from_="+19592008885", 
                       body= occupant[i] + " is home!")
                # Reset counters so another stream isn't sent if the device
                # is still present
                firstRun[i] = 0
                presentSent[i] = 1
                notPresentSent[i] = 0
                counter[i] = 0
                sleep(900)
            else:
                # If a stream's already been sent, just wait for 15 minutes
                counter[i] = 0
                sleep(900)
        # If a listed device address is not present, print and stream
        else:
            print(occupant[i] + "'s device is not present")
            # Only consider a device offline if it's counter has reached 30
            # This is the same as 15 minutes passing
            if counter[i] == 30 or firstRun[i] == 1:
                firstRun[i] = 0
                if notPresentSent[i] == 0:
                    # Stream that device is not present
                    streamer.log(occupant[i],":no_entry_sign::office:")
                    streamer.flush()
                    print(occupant[i] + " not present streamed")
                    #send sms
                    client.messages.create(to="+18604717675", from_="+19592008885", 
                       body= occupant[i] + " has left!")
                    # Reset counters so another stream isn't sent if the device
                    # is still present
                    notPresentSent[i] = 1
                    presentSent[i] = 0
                    counter[i] = 0
                else:
                    # If a stream's already been sent, wait 30 seconds
                    counter[i] = 0
                    sleep(30)
            # Count how many 30 second intervals have happened since the device 
            # disappeared from the network
            else:
                counter[i] = counter[i] + 1
                print(occupant[i] + "'s counter at " + str(counter[i]))
                sleep(30)


# Main thread

try:

    # Initialize a variable to trigger threads to exit when True
    global stop
    stop = False

    # Start the thread(s)
    # It will start as many threads as there are values in the occupant array
    for i in range(len(occupant)):
        t = Thread(target=whosHere, args=(i,))
        t.start()

    while True:
        # Make output global so the threads can see it
        global output
        # Assign list of devices on the network to "output"
        output = subprocess.check_output("sudo arp-scan -l", shell=True)
        # Wait 30 seconds between scans
        sleep(30)

except KeyboardInterrupt:
    # On a keyboard interrupt signal threads to exit
    stop = True
    exit()

