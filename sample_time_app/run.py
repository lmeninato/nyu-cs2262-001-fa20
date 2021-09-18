from flask import Flask
import time

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/time')
def get_time():
    # from https://stackoverflow.com/a/40359683
    curr_time = time.strftime('%A %B, %d %Y %H:%M:%S')
    return "The current time is {}".format(curr_time)


app.run(host='0.0.0.0',
        port=8080,
        debug=True)
