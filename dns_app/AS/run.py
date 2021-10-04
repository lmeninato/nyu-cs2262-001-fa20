import socket
import os

UDP_IP = "0.0.0.0"
UDP_PORT = 53533

FILE = "dns_records.txt"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

def read_record(TYPE, NAME):
    if not os.path.exists(FILE):
        print("records file does not exist")
        return

    lines = []
    with open(FILE, 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if NAME in line:
            items = [item.split("=")[1].strip() for item in line.split(",")]
            print("parsed the following items")
            items = str.encode("\n".join(items))
            print(items)
            return items
    return b'Unable to parse UDP'

def store_record(TYPE, NAME, VALUE=None, TTL=None):
    with open(FILE, 'w+') as f:
        f.write(f"TYPE={TYPE},NAME={NAME}")
        if VALUE:
            f.write(f",VALUE={VALUE}")
        if TTL:
            f.write(f",TTL={TTL}")
        f.write("\n")

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

    try:
        data = data.decode()
        print(data)
        data = [item.split("=")[1] for item in data.split("\n")]
        print(data)
        if len(data) == 2:
            TYPE, NAME = data
            print(f'Received TYPE={TYPE}, NAME={NAME}')

            # need to respond to request
            response = read_record(TYPE, NAME)
            print(f'response is {response}')
            sock.sendto(response, addr)

        elif len(data) == 4:
            TYPE, NAME, VALUE, TTL = data
            print(f'Received TYPE={TYPE}, NAME={NAME}, VALUE={VALUE}, TTL={TTL}')

            # need to store as record
            store_record(TYPE, NAME, VALUE, TTL)
            # sock.sendto(b'ack', addr) send ack? i guess lets not worry about dropped messages...
        else:
            raise Exception
    except:
        print("unable to parse UDP packet")


