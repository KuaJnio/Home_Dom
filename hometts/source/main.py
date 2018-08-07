from threading import Lock
from time import sleep
import sys
import signal
import json
import os
from MQTTClient import create_mqtt_client
from get_config import get_parameter


def signal_handler(signal, frame):
    print("Interpreted signal {}, exiting now...".format(signal))
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
            print("/usr/bin/mpg123 'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={}&tl=fr' > /dev/null 2>&1".format(tts))
            os.system("/usr/bin/mpg123 'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={}&tl=fr' > /dev/null 2>&1".format(tts))
            tts_lock.release()
    except Exception as e:
        print("Error in event_manager(): {}".format(e))


if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
    while True:
        sleep(1)
