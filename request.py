#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#   The whole data traffic is encrypted
#

import zmq
from zmq.auth import load_certificate

# new ZeroMQ context for managing sockets
context = zmq.Context()
# new request socket which expects a reply response
socket = context.socket(zmq.REQ)

client_public, client_secret = load_certificate(".keys/client/client.key_secret")
server_public, _ = load_certificate(".keys/server/server.key")

# assigns the CURVE keys to the sockets
socket.curve_publickey = client_public
socket.curve_secretkey = client_secret
socket.curve_serverkey = server_public

print("Connecting to Hello World server …")
socket.connect("tcp://localhost:5555")

# allows to forcefully terminate the script
# poller lets the program wait for an event without blocking forever (request-reply pattern)
poller = zmq.Poller()
# registers the socket for readable and writable events, useful for timeout handling
poller.register(socket, zmq.POLLIN | zmq.POLLOUT)


try:
    for request in range(10):
        print(f"Sending request {request} …")

        # tries to send a non-blocking request
        # if the socket is not ready, it breaks out of the loop
        try:
            socket.send(b"Hello", flags=zmq.NOBLOCK)
        except zmq.Again:
            break

        # waits for a reply with a 5-second timeout
        # if a reply is received, it is read from the socket
        socks = dict(poller.poll(timeout=5000))
        
        # checks if the server has sent a reply and is waiting
        # for the client to read it during the poll cycle
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
