#!venv/bin/python

import pika
import sys
import random as r
import time
import psutil


if len(sys.argv) == 1:
  sys.stderr.write("Usage: %s [cpu_num]\n" % sys.argv[0])
  sys.exit(1)

while True:

	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.exchange_declare(exchange='monitoring', exchange_type='topic')
	
	routing_key_cpu = 'cpu.' + sys.argv[1]
	routing_key_ram = 'ram.' + sys.argv[1]

	cpu = int(psutil.cpu_percent())
	ram = int(psutil.virtual_memory().percent)

	message_cpu = str(cpu)
	message_ram = str(ram)

	channel.basic_publish(exchange='monitoring',
			              routing_key=routing_key_cpu,
			              body=message_cpu)
	channel.basic_publish(exchange='monitoring',
			              routing_key=routing_key_ram,
			              body=message_ram)

	print(" PC uses %r percent of %r" % (message_cpu, routing_key_cpu))
	print(" PC uses %r percent of %r" % (message_ram, routing_key_ram))

	connection.close()
	time.sleep(5)
