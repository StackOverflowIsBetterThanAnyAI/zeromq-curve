#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects "Hello" from client, replies with "World"
#   The whole data traffic is encrypted
#

import time
import zmq
import asyncio
import sys
from zmq.auth import load_certificate
from zmq.auth.thread import ThreadAuthenticator

# Windows only: use SelectorEventLoop instead of DefaultEventLoop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

context = zmq.Context()

# Start ZAP
auth = ThreadAuthenticator(context)
auth.start()
auth.allow("127.0.0.1")
auth.configure_curve(domain="*", location=".keys/authorized_clients")

server_public, server_secret = load_certificate(".keys/server/server.key_secret")

# Setup REP-Socket with CURVE
socket = context.socket(zmq.REP)
socket.curve_secretkey = server_secret
socket.curve_publickey = server_public
socket.curve_server = True

socket.bind("tcp://*:5555")

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

try:
    print("Server has been started.")
    while True:
        socks = dict(poller.poll(timeout=2500))
        if socket in socks and socks[socket] == zmq.POLLIN:
            message = socket.recv()
            print(f"Received request: {message}")

            time.sleep(1)

            socket.send(b"World")

except KeyboardInterrupt:
    print("Script has been terminated.")

except Exception as e:
    print(f"Unexpected error: {e}.")

finally:
    socket.close()
    auth.stop()
    context.term()
    print("Server has been terminated.")
