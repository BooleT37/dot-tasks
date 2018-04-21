# Task 6. ZeroMQ

###Launch guide:
1. Setup virtualenv
- Grant execution rights to every *.py file
- Launch broker<br/>
`$ ./broker.py`
Broker is middleware server that connects server and worker together.
- Launch Flask server:<br/>`$ ./server.py`<br/> The server accepts filename in HTTP request (`[GET] /file/{:filename}`) and redirects this filename in socket message to broker. When broker sends back file content, it serves it as HTTP response.
- Launch worker:<br/>
`$ ./worker.py`<br/>
Worker listens to broker messages with file names, when it receives one, it reads file content from disk and sends message with this content back to broker.

- There are two ways to test how server works:
- - Via direct curl requests to files, i.e.:<br/>
`$ curl  http://127.0.0.1:5000/file/Lorem.txt`
- - By visiting page `http://127.0.0.1:5000/` in your browser