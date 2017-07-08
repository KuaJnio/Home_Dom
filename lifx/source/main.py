import os
import logging
from logging.handlers import RotatingFileHandler
import paho.mqtt.client as mqtt
from socket import error as socket_error
import errno
from threading import Thread
from time import sleep
import lifxlan

def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler = RotatingFileHandler('lifx.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    logger.addHandler(steam_handler)
    return logger

ADDRESS = '192.168.1.100' #address of mqtt broker use for events, can be dns name
PORT = 1883 #port of mqtt broker used for events
event_logger = create_logger()

def event_manager(topic, payload):
    RED = [65535, 65535, 65535, 3500]
    ORANGE = [5525, 65535, 65535, 3500]
    YELLOW = [7000, 65535, 65535, 3500]
    GREEN = [16173, 65535, 65535, 3500]
    CYAN = [29814, 65535, 65535, 3500]
    BLUE = [43634, 65535, 65535, 3500]
    PURPLE = [50486, 65535, 65535, 3500]
    PINK = [58275, 65535, 47142, 3500]
    WHITE = [58275, 0, 65535, 5500]
    COLD_WHITE = [58275, 0, 65535, 9000]
    WARM_WHITE = [58275, 0, 65535, 3200]
    GOLD = [58275, 0, 65535, 2500]

    HOST = "192.168.1.33"
    MAC = "d0:73:d5:21:89:a6"


    def turnOnLampWithLifx(lifxcolor):
        bulb = lifxlan.Light(MAC, HOST)
        bulb.set_color(lifxcolor)
        bulb.set_power("on")


    def turnOffLampWithLifx():
        bulb = lifxlan.Light(MAC, HOST)
        bulb.set_power("off")


    if topic == "lifx" and payload == "off":
        turnOffLampWithLifx()
    elif topic == "lifx" and payload == "on":
        turnOnLampWithLifx(GOLD)


def on_connect(client, userdata, flag, rc):
    if rc == 0:
        event_logger.info('MQTT >>> Connection OK')
    else:
        event_logger.info('MQTT >>> Connection KO, connected with result code '+str(rc))
    client.subscribe('lifx')
    event_logger.info('MQTT >>> Subscribed to \"lifx\"')


def on_disconnect(client, userdata, rc):
    event_logger.info('MQTT >>> Disconnected with result code '+str(rc))

    connected = False
    while not connected:
        try:
            event_logger.info('MQTT >>> Trying to reconnect...')
            rc = client.reconnect()
        except socket_error as serr:
            event_logger.info('MQTT >>> Error: '+str(serr.errno)+', '
            +errno.errorcode.get(serr.errno))
            sleep(2)
        if rc == 0:
            connected = True


def on_message(client, userdata, msg):
    event_logger.info('MQTT')
    event_logger.info('MQTT >>> New message :')
    event_logger.info('MQTT >>> [TOPIC] : '+msg.topic)
    event_logger.info('MQTT >>> [PAYLOAD] : '+msg.payload)
    try:
        event_manager(msg.topic, msg.payload)
        event_logger.info('MQTT >>> Message handled successfully')
    except:
        event_logger.info('MQTT >>> Error while handlin message...')



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
        event_logger.info('MQTT >>> Connecting to broker '+self.addr+':'+str(self.port)+'...')
        self.mqtt_client.loop_forever()

    def publish(self, topic, message):
        event_logger.info('MQTT >>> Publishing to broker '+self.addr+':'+str(self.port)
        +' in topic '+topic)
        self.mqtt_client.publish(topic, message)


def create_mqtt_client(addr, port):
    event_logger.info('MQTT >>> Creating mqtt client on broker : '+addr+':'+str(port))
    mqtt_cli_tmp = MqttClient(addr, port)
    mqtt_cli_tmp.daemon = True
    mqtt_cli_tmp.start()
    return mqtt_cli_tmp


def main():
    mqtt_client = create_mqtt_client(ADDRESS, PORT)
    while True:
        sleep(1)

if __name__ == "__main__":
    main()
