
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Up'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

"""
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/)
def index():
    pod_name = os.getenv("HOSTNAME")  
    pod_ip = request.remote_addr 
    return f'Hello! This is pod: {pod_name} with IP: {pod_ip}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='9090')
"""