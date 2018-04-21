#!venv/bin/python3

import os
from flask import Flask


FILE_PATH = os.path.abspath("files")

import zmq

#  Prepare our context and sockets
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5559")

app = Flask(__name__)

@app.route('/')
def list_fles():
    files = [f for f in os.listdir(FILE_PATH) if os.path.isfile(os.path.join(FILE_PATH, f))]
    page = "<html>\r\n<body><h2>Files:</h1><ul>\r\n"
    for f in files:
        page += '<li><a href="/file/{0}">{0}</a></li>\r\n'.format((f))
    page += "</ul></body>\r\n</html>"
    return page

@app.route('/file/<string:filename>')
def file_handle(filename):
    socket.send(bytes(filename, 'utf-8'))
    file_strs = socket.recv()
    return file_strs

if __name__ == '__main__':
    app.run(debug=True)
