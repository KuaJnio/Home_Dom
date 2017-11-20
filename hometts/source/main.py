from threading import Lock
from time import sleep
import sys
import signal
import json
import os
from MQTTClient import create_mqtt_client

tts_lock = Lock()


def signal_handler(signal, frame):
    print("Interpreted signal "+str(signal)+", exiting now...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


MQTT_BROKER = sys.argv[1]
MQTT_PORT = sys.argv[2]
MQTT_TOPICS = sys.argv[3].split(',')

mqtt_client = None


def on_message(client, userdata, msg):
    print('New message from MQTT broker :')
    print('[TOPIC] : '+msg.topic)
    print('[PAYLOAD] : '+msg.payload)
    rc = event_manager(msg.topic, msg.payload)
    print('Message handled with result code '+str(rc))


def event_manager(topic, payload):
    try:
        json_payload = json.loads(payload)
        target = json_payload['target']
        if target == 'hometts':
            tts = json_payload['tts']
            tts_lock.acquire()
            print "/usr/bin/mpg123 'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q="+tts+"&tl=fr' > /dev/null 2>&1"
            os.system("/usr/bin/mpg123 'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q="+tts+"&tl=fr' > /dev/null 2>&1")
            tts_lock.release()
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_BROKER, MQTT_PORT, on_message, MQTT_TOPICS)
    while True:
        sleep(1)
