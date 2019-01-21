from flask import Flask, render_template
import sys
import signal
import logging
from homedom_logger import set_logger
set_logger("webapp", logging.DEBUG)


def signal_handler(signal, frame):
    logging.info("Interpreted signal {}, exiting now...".format(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

app = Flask(__name__)


@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        logging.error("Error in home: {}".format(e))
        return str(e)


@app.route('/actuators')
def actuators():
    try:
        return render_template('actuators.html')
    except Exception as e:
        logging.error("Error in home: {}".format(e))
        return str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
