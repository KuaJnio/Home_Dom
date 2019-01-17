from time import sleep
import sys
import signal
import json
from MQTTClient import create_mqtt_client
from get_config import get_parameter
import requests
import logging
from homedom_logger import set_logger
set_logger("actionmanager", logging.DEBUG)


def signal_handler(signal, frame):
    logging.debug("Interpreted signal {}, exiting now...".format(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = get_parameter("actionmanager_topics")
HOMEVENTS_IP = get_parameter("homevents_ip")
HOMEVENTS_PORT = get_parameter("homevents_port")
HOMEVENTS_URL = "http://{}:{}".format(HOMEVENTS_IP, HOMEVENTS_PORT)
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
    payload = str(msg.payload, 'utf-8')
    event_manager(msg.topic, payload)


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


def disable_regex(regex):
    requests.post("{}/regex/{}/disable".format(HOMEVENTS_URL, regex))


def enable_regex(regex):
    requests.post("{}/regex/{}/enable".format(HOMEVENTS_URL, regex))


def event_manager(topic, payload):
    try:
        logging.debug("{} :: {}".format(topic, payload))
        if topic == "inputs":
            json_payload = json.loads(payload)
            feature = json_payload['HD_FEATURE']
            #identifier = json_payload['HD_IDENTIFIER']
            value = json_payload['HD_VALUE']
            #if feature == "HD_CONTACT":
            #    if value == 0:
            #        send_hometts_command("Porte ouverte")
            #    elif value == 1:
            #        send_hometts_command("Porte fermer")
            #elif feature == "HD_TEMPERATURE":
            #    send_hometts_command("Il fait {} degrer".format(value).replace('.', ','))
            #elif feature == "HD_HUMIDITY":
            #    send_hometts_command("Lumiditer est de {} pourcent".format(value).replace('.', ','))
            if feature == "HD_WEATHER":
                send_hometts_command(value)
            return "OK"
        elif topic == "events":
            json_payload = json.loads(payload)
            name = json_payload['name']
            if name == "LAMPE_CUISINE_ON":
                send_lifx_command("on", GOLD)
            elif name == "LAMPE_CUISINE_OFF":
                send_lifx_command("off", GOLD)
            #elif name == "PRESENCE_SALON_ENABLE":
            #    enable_regex("PRESENCE_SALON_ON")
            #elif name == "PRESENCE_SALON_DISABLE":
            #    disable_regex("PRESENCE_SALON_ON")
            elif name == "REQUEST_WEATHER_CURRENT":
                payload = json.JSONEncoder().encode({
                    "target": "weather",
                    "type": "current"
                })
                mqtt_client.publish("outputs", payload)
            elif name == "REQUEST_WEATHER_FORECAST":
                payload = json.JSONEncoder().encode({
                    "target": "weather",
                    "type": "forecast"
                })
                mqtt_client.publish("outputs", payload)

    except Exception as e:
        logging.debug("Error in event_manager(): {}".format(e))


if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
    while True:
        sleep(1)
