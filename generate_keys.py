import os
import shutil
from zmq.auth import create_certificates

os.makedirs(".keys/authorized_clients", exist_ok=True)
os.makedirs(".keys/client", exist_ok=True)
os.makedirs(".keys/server", exist_ok=True)

create_certificates(".keys/client", "client")
create_certificates(".keys/server", "server")

shutil.copy(".keys/client/client.key", ".keys/authorized_clients/")
