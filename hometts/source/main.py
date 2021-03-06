from threading import Lock, Thread
from time import sleep
import sys
import signal
import json
import os
from MQTTClient import create_mqtt_client
from get_config import get_parameter
import logging
from homedom_logger import set_logger
set_logger("hometts", logging.DEBUG)


def signal_handler(signal, frame):
    logging.info("Interpreted signal {}, exiting now...".format(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = get_parameter("hometts_topics")
mqtt_client = None
tts_lock = Lock()


def on_message(client, userdata, msg):
    payload = str(msg.payload, 'utf-8')
    event_manager(msg.topic, payload)


def event_manager(topic, payload):
    try:
        json_payload = json.loads(payload)
        target = json_payload['target']
        if target == 'hometts':
            tts = json_payload['tts']
            tts_lock.acquire()
            logging.debug("/usr/bin/mpg123 'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={}&tl=fr' > /dev/null 2>&1".format(tts))
            os.system("/usr/bin/mpg123 'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={}&tl=fr' > /dev/null 2>&1".format(tts))
            tts_lock.release()
    except Exception as e:
        logging.error("Error in event_manager(): {}".format(e))


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
    create_healthcheck("hometts")
    while True:
        sleep(1)
