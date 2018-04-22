# Task 5. AMQP
### Launch guide:
1. Install latest version of rabbitmq-server:<br/>
`$ sudo apt install rabbitmq-server`
1. Start RabbitMQ srever:<br/>
`$ sudo systemctl start rabbitmq-server`
1. Activate virtualenv:<br/>
`$ virtualenv venv`
1. Install dependencies:<br/>
`$ pip install -r requirements.txt`
1. Install python-tk:<br/>
`$ sudo apt install python-tk`
1. Grant execution rights:
   * chmod +x emit_monitoring.py
   * chmod +x receive_monitoring.py
1. Emit monitoring:<br/>
`$ ./emit_monitoring.py [cpu_num]`<br/>
(cpu num is any integer <= number of your CPUs, i.e. 1)
1. Draw graph:<br/>
`$ ./receive_monitoring.py [binding_key]`<br/>
Where binding_key is cpu or ram routing key from `emit_monitoring` output, i.e. `cpu.1` or `ram.1`

To observe the server you can use:<br/>
* `$ sudo systemctl status rabbitmq-server` to check the server status
* `$ sudo rabbitmqctl list_exchanges` to view exchanges
* `$ sudo rabbitmqctl list_bindings` to view existing bindings
