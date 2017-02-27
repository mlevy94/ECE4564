import json
import sys
import time
import numpy as np
import pika
Raw from __future__ import print_function

# import rabbitmq




# read in cmd line arguments 
cmd_error = "Incorrect command line parameters"
if len(sys.argv) == 9:
	if sys.argv[1] = "-b" and sys.argv[3] = "-p" and sys.argv[5] = "-c" and sys.argv[7] = "-k":
		mssBroker = sys.argv[2]
		vhost = sys.argv[4]
		hostpass = sys.argv[6]
		routekey = sys.argv[8]
	else:
		print(cmd_error)
elif len(sys.argv) == 5:
	if sys.argv[1] = "-b" and sys.argv[3] = "-k" :
		mssBroker = sys.argv[2]
		vhost = "/"
		#hostpass =  
		routekey = sys.argv[4]
	
else:
	print(cmd_error)

# create bindings to RabbitMQ

if len(sys.argv) == 9:
credentials = pika.PlainCredentials(vhost, hostpass)
parameters = pika.ConnectionParameters(mssBroker,
                                         5672,
                                         vhost,
                                         credentials)

else:                 # guest login
    parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(parameters)  
channel = connection.channel()
channel.exchange_declare(exchange='pi_utilization',
                          type='direct')
    

while True: 
	# establish a clock
	time = time.time()
	new_time = time
	#Creates initial 2d numpy arrays out of provided text files
	# find network data by reading every second and finding the difference from the previous second


	net_data =  np.loadtxt(fname='/proc/net/dev', skiprows = 2, usecols=range(1,16))
	lrx1 = net_data[0,0]
	ltx1 = net_data[0,8]

	wrx1 = net_data[1,0]
	wtx1 = net_data[1,8]

	erx1 = net_data[2,0]
	etx1 = net_data[2,8]

	#print(net_data)
	#print(lrx1)
	#print(ltx1)
	#print(wrx1)
	#print(wtx1)
	#print(erx1)
	#print(etx1)

	#Retrieve CPU data
	with open('/proc/stat') as f:
		  fields = [float(column) for column in f.readline().strip().split()[1:]]
	idle1, total1 = fields[3], sum(fields)
	f.close()
	#print(idle1)
	#print(total1)

	# Wait 1 second and sample data again
	time.sleep(1)
	new_time = time.time()
	time_delta = new_time - time

	net_data =  np.loadtxt('/proc/net/dev', skiprows = 2, usecols=range(1,16))
	lrx2 = net_data[0,0]
	ltx2 = net_data[0,8]

	wrx2 = net_data[1,0]
	wtx2 = net_data[1,8]

	erx2 = net_data[2,0]
	etx2 = net_data[2,8]

	#print(net_data)
	#print(lrx2)
	#print(ltx2)
	#print(wrx2)
	#print(wtx2)
	#print(erx2)
	#print(etx2)

	with open('/proc/stat') as f:
		  fields = [float(column) for column in f.readline().strip().split()[1:]]
	idle2, total2 = fields[3], sum(fields)
	f.close()

	idle_delta = idle2 - idle1
	total_delta = total2 - total1

	#print(idle_delta)
	#print(total_delta)


	#Utilization math 

	#lo throughput

	lrxout = (lrx2 - lrx1 ) / time_delta
	ltxout = (ltx2 - ltx1) / time_delta

	#wifi throughput
	wrxout = (wrx2 - wrx1) / time_delta
	wtxout = (wtx2 - wtx1) / time_delta

	#ethernet throughput
	erxout = (erx2 - erx1) / time_delta
	etxout = (etx2 - etx1) / time_delta

	#cpu utilization

	cpu_out = 100.0 * (1.0 - idle_delta/total_delta)


	 # store data 
	stats = {"net": {"lo": {"rx": lrxout,"tx": ltxout},"wlan0": {"rx": wrxout,"tx": wtxout},"eth0": {"rx": erxout,"tx": etxout}},"cpu": cpu_out}

	#send message to broker
	channel.basic_publish(exchange='pi_utilization',
						  routing_key=routekey,
						  body=json.dumps(stats))
