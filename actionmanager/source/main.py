from time import sleep
import sys
import signal
import json
from MQTTClient import create_mqtt_client


def signal_handler(signal, frame):
    print("Interpreted signal "+str(signal)+", exiting now...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


MQTT_BROKER = sys.argv[1]
MQTT_PORT = sys.argv[2]
MQTT_TOPICS = sys.argv[3].split(',')

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
    print('[PAYLOAD] : '+msg.payload)
    rc = event_manager(msg.topic, msg.payload)
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
        json_payload = json.loads(payload)
        feature = json_payload['HD_FEATURE']
        identifier = json_payload['HD_IDENTIFIER']
        value = json_payload['HD_VALUE']
        if feature == "HD_SWITCH":
            if value == 1 or value == 3:
                send_lifx_command("on", GOLD)
            elif value == 2 or value == 4:
                send_lifx_command("off", GOLD)
        elif feature == "HD_CONTACT":
            if value == 0:
                send_hometts_command("Porte ouverte")
            elif value == 1:
                send_hometts_command("Porte fermer")
        elif feature == "HD_TEMPERATURE":
            send_hometts_command("Il fait "+str(value)+" degrer")
        elif feature == "HD_HUMIDITY":
            send_hometts_command("Lumiditer est de "+str(value)+" pourcent")
        return "OK"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_BROKER, MQTT_PORT, on_message, MQTT_TOPICS)
    while True:
        sleep(1)
