#!/usr/bin/python
from SerialReader import create_serial_reader
import MqttClient
from time import sleep
import sys
import config
import signal
import logging
from logging.handlers import RotatingFileHandler


def signal_handler(signal, frame):
    config.running = False


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler = RotatingFileHandler('enocean.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    logger.addHandler(steam_handler)
    return logger

if __name__ == '__main__':
    config.system_logger = create_logger()
    broker = None
    port = None
    topic = None
    if len(sys.argv) == 4:
        broker = sys.argv[1]
        port = sys.argv[2]
        topic = sys.argv[3]
        config.mqtt_topic = topic
    else:
        sys.exit("Wrong parameters")

    MqttClient.mqtt_client = MqttClient.create_mqtt_client(broker, port, topic)
    serial_thread = create_serial_reader(config.enocean_device)
    while config.running:
        sleep(40)
        serial_thread.command_read_base_id()
    sys.exit(0)
