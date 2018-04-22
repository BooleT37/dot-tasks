# Task 6. ZeroMQ

###Launch guide:
1. Setup virtualenv
1. Grant execution rights to every *.py file
1. Launch broker<br/>
`$ ./broker.py`
Broker is middleware server that connects server and worker together.
1. Launch Flask server:<br/>`$ ./server.py`<br/> The server accepts filename in HTTP request (`[GET] /file/{:filename}`) and redirects this filename in socket message to broker. When broker sends back file content, it serves it as HTTP response.
1. Launch worker:<br/>
`$ ./worker.py`<br/>

Worker listens to broker messages with file names, when it receives one, it reads file content from disk and sends message with this content back to broker.

#### There are two ways to test how server works:
1. Via direct curl requests to files, i.e.:<br/>
`$ curl  http://127.0.0.1:5000/file/Lorem.txt`
1. By visiting page `http://127.0.0.1:5000/` in your browser