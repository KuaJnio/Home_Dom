from time import sleep
import lifxlan
import sys
import signal
import json
from MQTTClient import create_mqtt_client
from get_config import get_parameter


def signal_handler(signal, frame):
    print("Interpreted signal "+str(signal)+", exiting now...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = get_parameter("lifx_topics")

IP = get_parameter("lifx_1_ip")
MAC = get_parameter("lifx_1_mac")

mqtt_client = None


def turnOnLampWithLifx(lifxcolor):
    bulb = lifxlan.Light(MAC, IP)
    bulb.set_color(lifxcolor)
    bulb.set_power("on")

def turnOffLampWithLifx():
    bulb = lifxlan.Light(MAC, IP)
    bulb.set_power("off")


def on_message(client, userdata, msg):
    print('New message from MQTT broker :')
    print('[TOPIC] : '+msg.topic)
    payload = str(msg.payload, 'utf-8')
    print('[PAYLOAD] : '+payload)
    rc = event_manager(msg.topic, payload)
    print('Message handled with result code '+str(rc))


def event_manager(topic, payload):
    try:
        json_payload = json.loads(payload)
        target=json_payload['target']
        if target == "lifx":
            power=json_payload['power']
            color=json_payload['color']
            if power == "on":
                turnOnLampWithLifx(color)
            elif power == "off":
                turnOffLampWithLifx()
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
    while True:
        sleep(1)
