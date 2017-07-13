import paho.mqtt.client as mqtt
from socket import error as socket_error
import errno
from threading import Thread
from time import sleep
import lifxlan
import sys
import signal
import json


def signal_handler(signal, frame):
    print("Interpreted signal "+str(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

IP = "192.168.1.33"
MAC = "d0:73:d5:21:89:a6"
TOPIC = "lifx.outputs"

def event_manager(topic, payload):
    try:
        def turnOnLampWithLifx(lifxcolor):
            bulb = lifxlan.Light(MAC, IP)
            bulb.set_color(lifxcolor)
            bulb.set_power("on")


        def turnOffLampWithLifx():
            bulb = lifxlan.Light(MAC, IP)
            bulb.set_power("off")
            
            
        json_payload = json.loads(payload)
        power=json_payload['power']
        color=json_payload['color']

        if power == "on":
            turnOnLampWithLifx(color)
        elif power == "off":
            turnOffLampWithLifx()
    except Exception as e:
        return str(e)


def on_connect(client, userdata, flag, rc):
    if rc == 0:
        print('MQTT >>> Connection OK')
    else:
        print('MQTT >>> Connection KO, connected with result code '+str(rc))
    client.subscribe(TOPIC)
    print('MQTT >>> Subscribed to '+str(TOPIC))


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
        print('MQTT >>> Publishing to broker '+self.addr+':'+str(self.port)
        +' in topic '+topic)
        self.mqtt_client.publish(topic, message)


def create_mqtt_client(addr, port):
    print('MQTT >>> Creating mqtt client on broker : '+addr+':'+str(port))
    mqtt_cli_tmp = MqttClient(addr, port)
    mqtt_cli_tmp.daemon = True
    mqtt_cli_tmp.start()
    return mqtt_cli_tmp


def main():
    BROKER = sys.argv[1]
    PORT = sys.argv[2]
    mqtt_client = create_mqtt_client(BROKER, PORT)
    while True:
        sleep(1)

if __name__ == "__main__":
    main()
