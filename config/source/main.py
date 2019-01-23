from flask import Flask, jsonify
from time import sleep
from threading import Thread
import json
import logging
from MQTTClient import create_mqtt_client
from homedom_logger import set_logger
set_logger("config", logging.DEBUG)

app = Flask(__name__)
MQTT_HOST = None
MQTT_PORT = None
MQTT_TOPICS = None
mqtt_client = None


def on_message(client, userdata, msg):
    payload = str(msg.payload, 'utf-8')
    event_manager(msg.topic, payload)


def event_manager(topic, payload):
    try:
        pass
    except Exception as e:
        logging.error("Error in event_manager(): {}".format(e))


@app.route('/')
def config():
    try:
        data = json.load(open('config.json', 'r'))
        return jsonify(data), 200
    except Exception as e:
        logging.error("Error in config: " + str(e))
        return str(e), 500


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
    try:
        with open('config.json') as f:
            data = json.load(f)
            MQTT_HOST = data["mqtt_host"]
            MQTT_PORT = data["mqtt_port"]
        mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
        create_healthcheck("config")
        logging.debug("Initializing config server...")
        app.run(host='0.0.0.0', port=80)
    except Exception as e:
        logging.error('Error in main: ' + str(e))
