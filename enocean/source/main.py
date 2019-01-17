from SerialReader import create_serial_reader
from time import sleep
import sys
import signal
from MQTTClient import create_mqtt_client
from get_config import get_parameter
import logging
from homedom_logger import set_logger
set_logger("enocean", logging.DEBUG)


def signal_handler(signal, frame):
    logging.debug("Interpreted signal {}, exiting now...".format(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = get_parameter("enocean_topics")
mqtt_client = None


def on_message(client, userdata, msg):
    payload = str(msg.payload, 'utf-8')
    event_manager(msg.topic, payload)


def event_manager(topic, payload):
    try:
        pass
    except Exception as e:
        logging.debug("Error in event_manager(): {}".format(e))


if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
    serial_thread = create_serial_reader('/dev/ttyENOCEAN', mqtt_client)
    while True:
        sleep(1)
