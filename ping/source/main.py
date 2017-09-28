import paho.mqtt.client as mqtt
from socket import error as socket_error
import errno
from threading import Thread
from time import sleep
import sys
import signal
import json
import os


def signal_handler(signal, frame):
    print("Interpreted signal "+str(signal)+", exiting now...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

TOPICS = [] #topics to subscribe to
BROKER = "192.168.1.20"
PORT = 1883


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connection to broker OK')
    else:
        print('Connection to broker KO, with result code '+str(rc))
    for topic in TOPICS:
        client.subscribe(topic)
        print('Subscribed to \"'+topic+'\"')


def on_disconnect(client, userdata, rc):
    print('Disconnected from broker with result code '+str(rc))
    connected = False
    while not connected:
        try:
            print('Trying to reconnect to broker...')
            rc = client.reconnect()
        except socket_error as serr:
            print('Error while connecting to broker: '+str(serr.errno)+', '+errno.errorcode.get(serr.errno))
            sleep(2)
        if rc == 0:
            connected = True


def on_message(client, userdata, msg):
    print('New message from MQTT broker :')
    print('[TOPIC] : '+msg.topic)
    print('[PAYLOAD] : '+msg.payload)
    rc = event_manager(msg.topic, msg.payload)
    print('Message handled with result code '+str(rc))


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
        print('Connecting to broker '+self.addr+':'+str(self.port)+'...')
        self.mqtt_client.loop_forever()

    def publish(self, topic, message):
        print('Publishing to broker '+self.addr+':'+str(self.port)+' in topic '+topic)
        rc, count = self.mqtt_client.publish(topic, message)
        if rc == 0:
            print('Publish OK')
        else:
            print('Publish OK, with result '+self.publish_errors(rc))

    @staticmethod
    def publish_errors(error):
        if error == -1:
            return 'MQTT_ERR_AGAIN'
        elif error == 0:
            return 'MQTT_ERR_SUCCESS'
        elif error == 1:
            return 'MQTT_ERR_NOMEM'
        elif error == 2:
            return 'MQTT_ERR_PROTOCOL'
        elif error == 3:
            return 'MQTT_ERR_INVAL'
        elif error == 4:
            return 'MQTT_ERR_NO_CONN'
        elif error == 5:
            return 'MQTT_ERR_CONN_REFUSED'
        elif error == 6:
            return 'MQTT_ERR_NOT_FOUND'
        elif error == 7:
            return 'MQTT_ERR_CONN_LOST'
        elif error == 8:
            return 'MQTT_ERR_TLS'
        elif error == 9:
            return 'MQTT_ERR_PAYLOAD_SIZE'
        elif error == 10:
            return 'MQTT_ERR_NOT_SUPPORTED'
        elif error == 11:
            return 'MQTT_ERR_AUTH'
        elif error == 12:
            return 'MQTT_ERR_ACL_DENIED'
        elif error == 13:
            return 'MQTT_ERR_UNKNOWN'
        elif error == 14:
            return 'MQTT_ERR_ERRNO'


def create_mqtt_client(addr, port):
    print('Creating mqtt client on broker : '+addr+':'+str(port))
    mqtt_cli_tmp = MqttClient(addr, port)
    mqtt_cli_tmp.daemon = True
    mqtt_cli_tmp.start()
    return mqtt_cli_tmp
    
mqtt_client = create_mqtt_client(BROKER, PORT)

def set_payload(value):
	hd_payload = json.JSONEncoder().encode({
	"HD_FEATURE": "HD_PING",
	"HD_IDENTIFIER": "HD_ARMHFTOUCH",
	"HD_VALUE": value
	})
	return hd_payload

while True:
	try:
		ping = os.popen('ping www.google.com -c 1')
		res = ping.readlines()
		index = res[1].find('time=')
		res = res[1][80:]
		index = res.find(' ')
		res = res[:index]
		res = float(res)
		if (res > 0) and (res < 1000):
			payload = set_payload(res)
			mqtt_client.publish("inputs", payload)
		elif res > 1000:
			payload = set_payload(1000)
			mqtt_client.publish("inputs", payload)
			
	except Exception as e:
		print('Error '+str(e)+' in main')
	sleep(5)
