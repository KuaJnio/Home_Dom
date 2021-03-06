import signal
import json
import sys
from threading import Thread
from time import sleep
from MQTTClient import create_mqtt_client
from get_config import get_parameter
from models import Data
from database import DatabaseHandler
from flask import Flask, jsonify
import pytz
import logging
from homedom_logger import set_logger
set_logger("recorder", logging.DEBUG)


def signal_handler(signal, frame):
    logging.info("Interpreted signal {}, exiting now...".format(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = get_parameter("recorder_topics")
DATABASE_PATH = get_parameter("database_path")
mqtt_client = None
database_handler = None
app = Flask(__name__)
tz = pytz.timezone('Europe/Paris')


def on_message(client, userdata, msg):
    payload = str(msg.payload, 'utf-8')
    event_manager(msg.topic, payload)


def event_manager(topic, payload):
    try:
        json_payload = json.loads(payload)
        data = Data.from_dict(json_payload)
        database_handler.insert_data(data)
    except Exception as e:
        logging.error("Error in event_manager(): {}".format(e))


@app.route('/data', methods=['GET'])
def get_data():
    try:
        plot_data = {}
        data_list = database_handler.get_data()
        for data in data_list:
            if data.feature not in plot_data:
                plot_data[data.feature] = {}
                plot_data[data.feature][data.identifier] = {}
                plot_data[data.feature][data.identifier][data.timestamp] = data.value
            elif data.identifier not in plot_data[data.feature]:
                plot_data[data.feature][data.identifier] = {}
                plot_data[data.feature][data.identifier][data.timestamp] = data.value
            else:
                plot_data[data.feature][data.identifier][data.timestamp] = data.value

        return jsonify(plot_data), 200
    except Exception as e:
        logging.error("Error in get_data: {}".format(e))
        return "", 500


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
    database_handler = DatabaseHandler(DATABASE_PATH)
    create_healthcheck("recorder")
    app.run(host='0.0.0.0', port=80)
