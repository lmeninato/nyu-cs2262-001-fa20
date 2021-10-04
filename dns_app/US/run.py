from flask import Flask, request
import socket
import requests

app = Flask(__name__)

UDP_PORT = 53533

@app.route('/')
def hello_world():
    return 'Hello world!'

"""
e.g.
http://192.168.86.139:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=10&as_ip=192.168.86.139&as_port=53533
"""

@app.route('/fibonacci')
def get_fib():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    for param in [hostname,fs_port,number, as_ip, as_port]:
        if param is None:
            return "Bad request", 400

    print(f'Hostname={hostname}, fs_port={fs_port}, number={number}, as_ip={as_ip}, as_port={as_port}\n')

    # need to query DNS server for Fibonacci server IP address

    message = ["TYPE=A", f"NAME={hostname}"]
    message = str.encode("\n".join(message))
    print(f"sending message {message} to {(as_ip, UDP_PORT)}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (as_ip, UDP_PORT))

    data, _ = sock.recvfrom(1024)
    print(f"got {data} from AS")

    data = data.decode().split("\n")
    print(data)
    _, _, fs_ip, _ = data

    print(f"making request http://{fs_ip}:{fs_port}/fibonacci")
    r = requests.get(f"http://{fs_ip}:{fs_port}/fibonacci?number={number}")
    print(r.text)

    try:
        result = int(r.text)
        return f"Fibonacci({number}) is {result}", 200
    except:
        return "Error parsing response from Fibonacci Server", 400

app.run(host='0.0.0.0',
        port=8080,
        debug=True)