#!venv/bin/python

import pika
import sys
import matplotlib.pyplot as plt

data = dict()
lines = dict()
axis = [i for i in range(20)]

ax = plt.subplot(111)
plt.ion()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='monitoring',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]

if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='monitoring',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] PC uses %r percent of %r" % (body, method.routing_key))
    if method.routing_key.startswith('cpu'):
        data_cpu = data.setdefault(method.routing_key, [0]*20)
        data_cpu.pop(0)
        data_cpu.append(int(body))
        data[method.routing_key] = data_cpu
    if method.routing_key.startswith('ram'):
        data_ram = data.setdefault(method.routing_key, [0]*20)
        data_ram.pop(0)
        data_ram.append(int(body))
        data[method.routing_key] = data_ram
    ax.cla()
    for key in data.keys():
    	lines[dict], = ax.plot(axis, data[key], lw=1, label=key)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    plt.show(block=False)
    plt.pause(0.001)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
