import os
import logging
import paho.mqtt.client as mqtt
from socket import error as socket_error
import errno
from threading import Thread
from time import sleep
import json

TOPICS = ['enocean.inputs'] #topics to subscribe to
ADDRESS = '192.168.1.100' #address of mqtt broker use for events, can be dns name
PORT = 1883 #port of mqtt broker used for events


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
    print('MQTT >>> Message handled with return code '+str(rc))



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
        print('MQTT >>> Publishing to broker '+self.addr+':'+str(self.port)
        +' in topic '+topic)
        self.mqtt_client.publish(topic, message)


def create_mqtt_client(addr, port):
    print('MQTT >>> Creating mqtt client on broker : '+addr+':'+str(port))
    mqtt_cli_tmp = MqttClient(addr, port)
    mqtt_cli_tmp.daemon = True
    mqtt_cli_tmp.start()
    return mqtt_cli_tmp
    
mqtt_client = create_mqtt_client(ADDRESS, PORT)

def event_manager(topic, payload):
    payload_json_raw = '['+payload+']'
    json_payload = json.loads(payload_json_raw)[0]
    if json_payload['type'] == "BUTTON" and json_payload["value"] == "A1_PRESSED":
        mqtt_client.publish("lifx", "on")
    if json_payload['type'] == "BUTTON" and json_payload["value"] == "B1_PRESSED":
        mqtt_client.publish("lifx", "on")
    if json_payload['type'] == "BUTTON" and json_payload["value"] == "A0_PRESSED":
        mqtt_client.publish("lifx", "off")
    if json_payload['type'] == "BUTTON" and json_payload["value"] == "B0_PRESSED":
        mqtt_client.publish("lifx", "off")
    rc = 0
    return rc


def main():
    while True:
        sleep(1)

if __name__ == "__main__":
    main()
