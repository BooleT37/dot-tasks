# Task 1. Thrift


## Launch Guide:
1. Install build tools:<br/>
`$ sudo apt install automake bison flex g++ git libboost-all-dev libevent-dev libssl-dev libtool make pkg-config`
1. Install python 2:
`$ sudo apt install python-all python-all-dev python-all-dbg`
1. Install python dependencies (you might want to make it in virtualenv):
`$ pip install -r requirements.txt`
1. Install nodejs:<br/>
 `$ curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -`<br/>
 `$ sudo apt install nodejs npm`
1. Install npm dependencies:<br/>
`$ sudo npm install`
1. [Download](http://thrift.apache.org/download) and extract Thrift
1. cd to Thrift directory
1. `$ ./bootstrap.sh`
1. `$ ./configure`
1. `$ sudo make`<br/>(If you see EACCESS errors, try run manually `$ sudo npm install --unsafe-perms` in thrift directory (this shit took me 2 hours to figure out 😠))
1. `$ sudo make check` - to make sure everything is working
1. Generate nodejs code:<br/>
`$ thrift --gen js:node task1.thrift`
1. Generate nodejs code:<br/>
`$ thrift --gen py task1.thrift`
1. Grant server and client execution rights:<br/>
`$ chmod +x server.js`
`$ chmod +x client.py`
1. Run server (assuming node alias in in `/usr/bin/node`):<br/>
`$ ./server.js`
1. Run client (assuming python3 alias in in `/usr/bin/python3`):<br/>
`$ ./client.js`