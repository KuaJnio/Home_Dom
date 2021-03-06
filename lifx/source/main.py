from time import sleep
from threading import Thread
import lifxlan
import sys
import signal
import json
from MQTTClient import create_mqtt_client
from get_config import get_parameter
import logging
from homedom_logger import set_logger
set_logger("lifx", logging.DEBUG)


def signal_handler(signal, frame):
    logging.info("Interpreted signal {}, exiting now...".format(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = get_parameter("lifx_topics")
IP = get_parameter("lifx_1_ip")
MAC = get_parameter("lifx_1_mac")
mqtt_client = None


def on_message(client, userdata, msg):
    payload = str(msg.payload, 'utf-8')
    event_manager(msg.topic, payload)


def turnOnLampWithLifx(lifxcolor):
    bulb = lifxlan.Light(MAC, IP)
    bulb.set_color(lifxcolor)
    bulb.set_power("on")


def turnOffLampWithLifx():
    bulb = lifxlan.Light(MAC, IP)
    bulb.set_power("off")


def event_manager(topic, payload):
    try:
        json_payload = json.loads(payload)
        target = json_payload['target']
        if target == "lifx":
            power = json_payload['power']
            color = json_payload['color']
            if power == "on":
                turnOnLampWithLifx(color)
            elif power == "off":
                turnOffLampWithLifx()
    except Exception as e:
        logging.error("Error in event_manager(): {}".format(e))


def create_healthcheck(app_name):
    class HealthCheck(Thread):
        def __init__(self, name):
            Thread.__init__(self)
            self.name = name

        def run(self):
            try:
                while True:
                    mqtt_client.publish("status", self.name)
                    sleep(1)
            except Exception as e:
                logging.error("Error in HealthCheck.run(): {}".format(e))

    healthcheck = HealthCheck(app_name)
    healthcheck.daemon = True
    healthcheck.start()


if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
    create_healthcheck("lifx")
    while True:
        sleep(1)
