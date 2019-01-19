from time import sleep, time
import sys
import signal
import json
from MQTTClient import create_mqtt_client
from get_config import get_parameter
import urllib.request
import pytz
import datetime
from googletrans import Translator
import logging
from homedom_logger import set_logger
set_logger("weather", logging.DEBUG)


def signal_handler(signal, frame):
    logging.debug("Interpreted signal {}, exiting now...".format(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = get_parameter("weather_topics")
mqtt_client = None
tz = pytz.timezone('Europe/Paris')
translator = Translator()

RENNES = 2983990
APIKEY = "98a19c144b3105dc774646a8a9429a52"
FORECAST_SIZE = 3


def weather_data_to_string(data):
    date = datetime.datetime.fromtimestamp(data['dt'], tz)
    #meteo_main = translator.translate(data['weather'][0]['main'], src='en', dest='fr').text
    meteo_description = translator.translate(data['weather'][0]['description'], src='en', dest='fr').text
    temperature = round((data['main']['temp'] - 273.15), 1)
    humidity = data['main']['humidity']
    cloudiness = data['clouds']['all']
    wind_speed = round(data['wind']['speed'] * 3.6)
    wind_deg = int(data['wind']['deg'])
    wind_direction = ""
    if wind_deg in range(0, 12):
        wind_direction = "nord"
    elif wind_deg in range(12, 34):
        wind_direction = "nord-nord-est"
    elif wind_deg in range(34, 57):
        wind_direction = "nord-est"
    elif wind_deg in range(57, 79):
        wind_direction = "est-nord-est"
    elif wind_deg in range(79, 102):
        wind_direction = "est"
    elif wind_deg in range(102, 124):
        wind_direction = "est-sud-est"
    elif wind_deg in range(124, 147):
        wind_direction = "sud-est"
    elif wind_deg in range(147, 169):
        wind_direction = "sud-sud-est"
    elif wind_deg in range(169, 192):
        wind_direction = "sud"
    elif wind_deg in range(192, 214):
        wind_direction = "sud-sud-ouest"
    elif wind_deg in range(214, 237):
        wind_direction = "sud-ouest"
    elif wind_deg in range(237, 259):
        wind_direction = "ouest-sud-ouest"
    elif wind_deg in range(259, 282):
        wind_direction = "ouest"
    elif wind_deg in range(282, 304):
        wind_direction = "ouest-nord-ouest"
    elif wind_deg in range(304, 327):
        wind_direction = "nord-ouest"
    elif wind_deg in range(327, 349):
        wind_direction = "nord-nord-ouest"
    elif wind_deg in range(349, 361):
        wind_direction = "nord"

    return "A {} {} {} degrer et {} pourcent dhumiditer {} pourcent de couverture nuageuse avec du vent {} a {} kilometre heure".format(date.strftime("%H:%M:%S"), meteo_description, temperature, humidity, cloudiness, wind_direction, wind_speed).replace('.', ',')


def weather_current():
    url = "http://api.openweathermap.org/data/2.5/weather?id={}&APPID={}".format(RENNES, APIKEY)
    res = urllib.request.urlopen(url)
    res_body = res.read()
    data = json.loads(res_body.decode("utf-8"))

    hd_payload = json.JSONEncoder().encode({
        "target": "hometts",
        "tts": weather_data_to_string(data)
    })
    mqtt_client.publish("outputs", hd_payload)


def weather_forecast():
    url = "http://api.openweathermap.org/data/2.5/forecast?id={}&APPID={}".format(RENNES, APIKEY)
    res = urllib.request.urlopen(url)
    res_body = res.read()
    j = json.loads(res_body.decode("utf-8"))
    forecast = j['list']
    for i in range(0, FORECAST_SIZE):
        hd_payload = json.JSONEncoder().encode({
            "target": "hometts",
            "tts": weather_data_to_string(forecast[i])
        })
        mqtt_client.publish("outputs", hd_payload)


def on_message(client, userdata, msg):
    payload = str(msg.payload, 'utf-8')
    event_manager(msg.topic, payload)


def event_manager(topic, payload):
    try:
        json_payload = json.loads(payload)
        target = json_payload['target']
        if target == 'weather':
            weather_type = json_payload['type']
            if weather_type == "current":
                weather_current()
            elif weather_type == "forecast":
                weather_forecast()

    except Exception as e:
        logging.debug("Error in event_manager(): {}".format(e))


if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
    while True:
        sleep(1)
