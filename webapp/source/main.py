import os
from flask import Flask, request, redirect, url_for, render_template, Response, send_file, jsonify
import glob
import sys
from time import sleep
import json
import signal
import requests

app = Flask(__name__)


@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        print("Error in home: "+str(e))
        return str(e)
        
@app.route('/actuators')
def actuators():
    try:
        return render_template('actuators.html')
    except Exception as e:
        print("Error in home: "+str(e))
        return str(e)

def signal_term_handler(signal, frame):
    print('Catched signal SIGTERM')
    print('Executing some actions before exiting process...') 
    try:
        pass
    except Exception as e:
        print('Error in signal_term_handler: '+str(e))
    print('Done handling signal SIGTERM, exiting now!')
    sys.exit(0)


def main():
    try:
        signal.signal(signal.SIGTERM, signal_term_handler)
        print("Initializing server...")
        app.run(host='0.0.0.0', port=80, debug=True)
    except Exception as e:
        print('Error in main: '+str(e))
    while True:
        sleep(1)


if __name__ == '__main__':
    main()
