#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#   The whole data traffic is encrypted
#

import zmq
from zmq.auth import load_certificate

context = zmq.Context()
socket = context.socket(zmq.REQ)

client_public, client_secret = load_certificate(".keys/client/client.key_secret")
server_public, _ = load_certificate(".keys/server/server.key")

socket.curve_publickey = client_public
socket.curve_secretkey = client_secret
socket.curve_serverkey = server_public

print("Connecting to Hello World server …")
socket.connect("tcp://localhost:5555")

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN | zmq.POLLOUT)


try:
    for request in range(10):
        print(f"Sending request {request} …")

        try:
            socket.send(b"Hello", flags=zmq.NOBLOCK)
        except zmq.Again:
            break

        socks = dict(poller.poll(timeout=5000))
        if socket in socks and (socks[socket] & zmq.POLLIN):
            message = socket.recv()
            print(f"Received reply {request} [ {message} ]")
        else:
            print("No reply within timeout, exiting script.")
            break

except KeyboardInterrupt:
    print("Script has been terminated.")

except Exception as e:
    print(f"Unexpected error: {e}.")

finally:
    socket.close()
    print("Client has been terminated.")
