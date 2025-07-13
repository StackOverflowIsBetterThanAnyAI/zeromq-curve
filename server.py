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
# avoid known asyncio issues
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# new ZeroMQ context for managing sockets
context = zmq.Context()

# start a ZAP handler
auth = ThreadAuthenticator(context)
auth.start()
auth.allow("127.0.0.1")
# only allow explicitly trusted public keys
auth.configure_curve(domain="*", location=".keys/authorized_clients")

server_public, server_secret = load_certificate(".keys/server/server.key_secret")

# setup reply socket with CURVE
# assigns the CURVE keys to the sockets
socket = context.socket(zmq.REP)
socket.curve_secretkey = server_secret
socket.curve_publickey = server_public
socket.curve_server = True

socket.bind("tcp://*:5555")

# allows to forcefully terminate the script
# poller lets the program wait for an event without blocking forever (request-reply pattern)
poller = zmq.Poller()
# registers the socket for readable events
poller.register(socket, zmq.POLLIN)

try:
    print("Server has been started.")
    # waits up to 2.5 seconds for incoming messages
    while True:
        socks = dict(poller.poll(timeout=2500))
        # checks if there is data ready to read on the server socket during the poll cycle
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
