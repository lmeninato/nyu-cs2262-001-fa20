from flask import Flask, request
import socket

app = Flask(__name__)

UDP_PORT = 53533

@app.route('/')
def hello_world():
    return 'Hello world!'

'''
Example:

curl -X POST -F "abc=def" http://192.168.86.139:9090/register
curl -X POST -F "hostname=fibonacci.com" -F "ip=192.168.86.139" -F "as_ip=192.168.86.139" -F "as_port=53533" http://192.168.86.139:9090/register

'''

@app.route('/register', methods = ['POST'])
def register():
    data = request.form

    for info in ['hostname', 'ip', 'as_ip', 'as_port']:
        if info not in data:
            return f"Missing {info}", 400

    hostname = data['hostname']
    ip = data['ip']
    as_ip = data['as_ip']
    as_port = data['as_port']

    send_registration_request(hostname, ip, as_ip, as_port)

    return 'Registration Successful', 201

def send_registration_request(hostname, ip, as_ip, as_port):
    message = ["TYPE=A", f"NAME={hostname}", f"VALUE={ip}", "TTL=100"]
    message = str.encode("\n".join(message))
    print(f"sending message {message} to {(as_ip, UDP_PORT)}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (as_ip, UDP_PORT))

@app.route('/fibonacci')
def fibonacci():
    number = request.args.get('number')

    if number is None:
        return "Bad request", 400

    try:
        number = int(number)
    except:
        print("unknown exception")
        return "Bad request - unable to parse number", 400

    fib = fibonacci_helper(number)

    return str(fib), 200


def fibonacci_helper(n):
    if n <= 1:
        return n

    prev2 = 0
    prev1 = 1

    for i in range(2, n+1):
        curr = prev1+prev2
        prev2 = prev1
        prev1 = curr

    return curr

app.run(host='0.0.0.0',
        port=9090,
        debug=True)