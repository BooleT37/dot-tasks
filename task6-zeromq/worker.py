#!venv/bin/python3

import os
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5560")

FILE_PATH = os.path.abspath("files")

while True:
    filename = socket.recv()
    print("Requested file: %s" % filename)
    with open(os.path.join(FILE_PATH, filename.decode('utf-8') )) as f:
        fi = f.read()
        socket.send(bytes(fi, 'utf-8'))

