from time import sleep
import sys
import signal
import json
import os
from MQTTClient import create_mqtt_client


def signal_handler(signal, frame):
    print("Interpreted signal "+str(signal)+", exiting now...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


MQTT_BROKER = sys.argv[1]
MQTT_PORT = sys.argv[2]
MQTT_TOPICS = []

mqtt_client = None


def on_message(client, userdata, msg):
    print('New message from MQTT broker :')
    print('[TOPIC] : '+msg.topic)
    print('[PAYLOAD] : '+msg.payload)
    rc = event_manager(msg.topic, msg.payload)
    print('Message handled with result code '+str(rc))


def set_payload(value):
    hd_payload = json.JSONEncoder().encode({
    "HD_FEATURE": "HD_PING",
    "HD_IDENTIFIER": "HD_ARMHFTOUCH",
    "HD_VALUE": value
    })
    return hd_payload


if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_BROKER, MQTT_PORT, on_message, MQTT_TOPICS)
    while True:
        try:
            ping = os.popen('ping www.google.com -c 1')
            res0 = ping.readlines()
            index0 = res0[1].find('time=')
            res1 = res0[1][index0+5:]
            index1 = res1.find(' ')
            res2 = res1[:index1]
            res = float(res2)
            if (res > 0) and (res < 1000):
                payload = set_payload(res)
                mqtt_client.publish("inputs", payload)
            elif res > 1000:
                payload = set_payload(1000)
                mqtt_client.publish("inputs", payload)
        except Exception as e:
            print('Error '+str(e)+' in main')
        sleep(5)
