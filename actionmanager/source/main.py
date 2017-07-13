import os
import logging
import paho.mqtt.client as mqtt
from socket import error as socket_error
import errno
from threading import Thread
from time import sleep
import signal
import json
import sys


RED = [65535, 65535, 65535, 3500]
ORANGE = [6500, 65535, 65535, 3500]
YELLOW = [9000, 65535, 65535, 3500]
GREEN = [16173, 65535, 65535, 3500]
CYAN = [29814, 65535, 65535, 3500]
BLUE = [43634, 65535, 65535, 3500]
PURPLE = [50486, 65535, 65535, 3500]
PINK = [58275, 65535, 47142, 3500]
WHITE = [58275, 0, 65535, 5500]
COLD_WHITE = [58275, 0, 65535, 9000]
WARM_WHITE = [58275, 0, 65535, 3200]
GOLD = [58275, 0, 65535, 2500]


def signal_handler(signal, frame):
    print("Interpreted signal "+str(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

TOPICS = ['sensor.inputs'] #topics to subscribe to
BROKER = "homedom"
PORT = 1883

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('MQTT >>> Connection OK')
    else:
        print('MQTT >>> Connection KO, connected with result code '+str(rc))
    for topic in TOPICS:
        client.subscribe(topic)
        print('MQTT >>> Subscribed to \"'+topic+'\"')


def on_disconnect(client, userdata, rc):
    print('MQTT >>> Disconnected with result code '+str(rc))

    connected = False
    while not connected:
        try:
            print('MQTT >>> Trying to reconnect...')
            rc = client.reconnect()
        except socket_error as serr:
            print('MQTT >>> Error: '+str(serr.errno)+', '
            +errno.errorcode.get(serr.errno))
            sleep(2)
        if rc == 0:
            connected = True


def on_message(client, userdata, msg):
    print('MQTT')
    print('MQTT >>> New message :')
    print('MQTT >>> [TOPIC] : '+msg.topic)
    print('MQTT >>> [PAYLOAD] : '+msg.payload)
    rc = event_manager(msg.topic, msg.payload)
    print('MQTT >>> Message handled with result '+str(rc))



class MqttClient(Thread):
    def __init__(self, addr, port):
        Thread.__init__(self)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_disconnect = on_disconnect
        self.mqtt_client.on_message = on_message
        self.addr = addr
        self.port = port

    def run(self):
        self.mqtt_client.connect(host=self.addr, port=self.port)
        print('MQTT >>> Connecting to broker '+self.addr+':'+str(self.port)+'...')
        self.mqtt_client.loop_forever()

    def publish(self, topic, message):
        print('MQTT >>> Publishing to broker '+self.addr+':'+str(self.port)+' in topic '+topic)
        self.mqtt_client.publish(topic, message)


def create_mqtt_client(addr, port):
    print('MQTT >>> Creating mqtt client on broker : '+addr+':'+str(port))
    mqtt_cli_tmp = MqttClient(addr, port)
    mqtt_cli_tmp.daemon = True
    mqtt_cli_tmp.start()
    return mqtt_cli_tmp
    
mqtt_client = create_mqtt_client(BROKER, PORT)

def event_manager(topic, payload):
    try:
        json_payload = json.loads(payload)
        feature = json_payload['HD_FEATURE']
        identifier = json_payload['HD_IDENTIFIER']
        value = json_payload['HD_VALUE']
        if feature == "HD_SWITCH":
            if value == "1" or value == "3":
                lifx_payload = json.JSONEncoder().encode({
                    "power": "on",
                    "color": WHITE
                })
                mqtt_client.publish("lifx.outputs", lifx_payload)
            elif value == "2" or value == "4":
                lifx_payload = json.JSONEncoder().encode({
                    "power": "off",
                    "color": WHITE
                })
                mqtt_client.publish("lifx.outputs", lifx_payload)
        elif feature == "HD_CONTACT":
            if value == "0":
                lifx_payload = json.JSONEncoder().encode({
                    "power": "on",
                    "color": GOLD
                })
                mqtt_client.publish("lifx.outputs", lifx_payload)
            elif value == "1":
                lifx_payload = json.JSONEncoder().encode({
                    "power": "off",
                    "color": WHITE
                })
                mqtt_client.publish("lifx.outputs", lifx_payload)
        return "OK"
    except Exception as e:
        return str(e)

def main():
    while True:
        sleep(1)

if __name__ == "__main__":
    main()
