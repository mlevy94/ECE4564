HOW TO:
	pistatsd.py - [host] Gathers data from the device to send to the monitor
	pistastsview.py - [monitor] Listens for information from a host.
	
ARGUMENTS:
	file [-b message broker] [–p virtual host] [–c login:password] –k routing key
	DEFAULTS:
		-b localhost
		-p /
		-c guest
	
DEPENDENCIES:
	host:
		Programs:
			rabbitmq-server
		Python Modules:
			pika
	monitor:
		Programs:
			rabbitmq-server
			mongodb
			python 3.4
		Python Modules:
			pika
			pymongo