# ZeroMQ CURVE

## ZeroMQ Authentication Protocol with CURVE

### Windows with two terminals on one machine

1.  Generate the public and private key pairs for the client and server

```
python generate_keys.py
```

2. Start Wireshark and listen on the Adapter for loopback traffic capture

3. Filter for TCP data packets on the specified port 5555

```
tcp.port == 5555 && tcp.len > 0
```

4. Start the server script in one terminal

```
python server.py
```

5. Start the client script in another terminal

```
python request.py
```

6. The actual data packets will be encrypted
