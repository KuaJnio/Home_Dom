from time import sleep
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
MQTT_TOPICS = get_parameter("actionmanager_topics")

mqtt_client = None

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


def on_message(client, userdata, msg):
    print('New message from MQTT broker :')
    print('[TOPIC] : '+msg.topic)
    payload = str(msg.payload, 'utf-8')
    print('[PAYLOAD] : '+payload)
    rc = event_manager(msg.topic, payload)
    print('Message handled with result code '+str(rc))


def send_lifx_command(power, color):
    payload = json.JSONEncoder().encode({
        "target": "lifx",
        "power": power,
        "color": color
    })
    mqtt_client.publish("outputs", payload)


def send_hometts_command(tts):
    payload = json.JSONEncoder().encode({
        "target": "hometts",
        "tts": tts
    })
    mqtt_client.publish("outputs", payload)


def event_manager(topic, payload):
    try:
        if topic == "inputs":
            json_payload = json.loads(payload)
            feature = json_payload['HD_FEATURE']
            identifier = json_payload['HD_IDENTIFIER']
            value = json_payload['HD_VALUE']
            if feature == "HD_CONTACT":
                if value == 0:
                    send_hometts_command("Porte ouverte")
                elif value == 1:
                    send_hometts_command("Porte fermer")
            elif feature == "HD_TEMPERATURE":
                send_hometts_command("Il fait "+str(value)+" degrer")
            elif feature == "HD_HUMIDITY":
                send_hometts_command("Lumiditer est de "+str(value)+" pourcent")
            return "OK"
        elif topic == "events":
            json_payload = json.loads(payload)
            name = json_payload['name']
            if name == "LAMPE_CHAMBRE_ON":
                 send_lifx_command("on", GOLD)
            elif name == "LAMPE_CHAMBRE_OFF":
                 send_lifx_command("off", GOLD)
            return "OK"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
    while True:
        sleep(1)
