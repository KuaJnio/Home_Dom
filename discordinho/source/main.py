from time import sleep
from threading import Thread
import sys
import signal
import discord
import asyncio
import json
from MQTTClient import create_mqtt_client
from get_config import get_parameter
import logging
from homedom_logger import set_logger
set_logger("discordinho", logging.INFO)


def signal_handler(signal, frame):
    logging.info("Interpreted signal {}, exiting now...".format(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = get_parameter("discordinho_topics")
mqtt_client = None

#discord specific

client = discord.Client()
server_name = 'Home_Dom'
channel_inputs = None
channel_outputs = None
channel_events = None


@client.event
async def on_ready():
    logging.info(server_name)
    global channel_inputs
    channel_inputs = discord.utils.get(client.get_all_channels(), server__name=server_name, name="inputs")
    global channel_outputs
    channel_outputs = discord.utils.get(client.get_all_channels(), server__name=server_name, name="outputs")
    global channel_events
    channel_events = discord.utils.get(client.get_all_channels(), server__name=server_name, name="events")


async def send_message(client, channel, message):
    await client.send_message(channel, message)


def send_to_discord(channel, payload):
    async def task_send_message():
        await send_message(client, channel, payload)
    task = client.loop.create_task(task_send_message())


def on_message(client, userdata, msg):
    payload = str(msg.payload, 'utf-8')
    event_manager(msg.topic, payload)


def event_manager(topic, payload):
    try:
        if topic == "inputs":
            send_to_discord(channel_inputs, payload)
        elif topic == "outputs":
            send_to_discord(channel_outputs, payload)
        elif topic == "events":
            send_to_discord(channel_events, payload)

        return "OK"

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
    try:
        with open('token') as t:
            token = json.load(t)
        mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
        create_healthcheck("discordinho")
        client.run(token)

    except Exception as e:
        logging.error("Error in main(): {}".format(e))
