import discord
import asyncio
import time
import datetime
import pytz #pip
import sys
import json
from MQTTClient import create_mqtt_client
from get_config import get_parameter


token           = sys.argv[1]
client          = discord.Client()
MQTT_HOST       = get_parameter("mqtt_host")
MQTT_PORT       = get_parameter("mqtt_port")
MQTT_TOPICS     = []

mqtt_client = None

def on_message(client, userdata, msg):
    pass

def get_time():
    tz = pytz.timezone('Europe/Berlin')
    berlin_now = datetime.datetime.now(tz)
    return berlin_now.strftime('%d-%m-%Y %H:%M:%S')

@client.event
async def on_ready():
    pass


@client.event
async def on_message(message):
    try:
        if message.content == "on":
            payload = json.JSONEncoder().encode({"HD_FEATURE": "HD_BUTTON", "HD_IDENTIFIER": "DISCORD", "HD_VALUE": 1})
            mqtt_client.publish("inputs", payload)
        elif message.content == "off":
            payload = json.JSONEncoder().encode({"HD_FEATURE": "HD_BUTTON", "HD_IDENTIFIER": "DISCORD", "HD_VALUE": 0})
            mqtt_client.publish("inputs", payload)
    except Exception as e:
        print('Error in on_message: '+str(e))

if __name__ == '__main__':
    try:
        mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
        client.run(token)
    except Exception as e:
        print('Error in main: '+str(e))