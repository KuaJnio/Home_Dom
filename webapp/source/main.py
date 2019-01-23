from flask import Flask, render_template
from threading import Thread
from time import sleep
import sys
import signal
import logging
from MQTTClient import create_mqtt_client
from get_config import get_parameter
from homedom_logger import set_logger
set_logger("webapp", logging.DEBUG)

MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = get_parameter("actionmanager_topics")
mqtt_client = None


def on_message(client, userdata, msg):
    payload = str(msg.payload, 'utf-8')
    event_manager(msg.topic, payload)


def event_manager(topic, payload):
    try:
        pass
    except Exception as e:
        logging.error("Error in event_manager(): {}".format(e))


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


def create_healthcheck(app_name):
    class HealthCheck(Thread):
        def __init__(self, name):
            Thread.__init__(self)
            self.name = name

        def run(self):
            try:
                while True:
                    mqtt_client.publish("status", self.name)
                    sleep(1)
            except Exception as e:
                logging.error("Error in HealthCheck.run(): {}".format(e))

    healthcheck = HealthCheck(app_name)
    healthcheck.daemon = True
    healthcheck.start()


if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
    create_healthcheck("webapp")
    app.run(host='0.0.0.0', port=80, debug=True)
