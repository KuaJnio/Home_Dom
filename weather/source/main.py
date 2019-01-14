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


def signal_handler(signal, frame):
    print("Interpreted signal {}, exiting now...".format(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = get_parameter("weather_topics")
mqtt_client = None
tz = pytz.timezone('Europe/Paris')


RENNES = 2983990
APIKEY = "98a19c144b3105dc774646a8a9429a52"


def weather_forecast():
    url = "http://api.openweathermap.org/data/2.5/forecast?id={}&APPID={}".format(RENNES, APIKEY)
    res = urllib.request.urlopen(url)
    res_body = res.read()
    j = json.loads(res_body.decode("utf-8"))
    forecast = j['list']
    string = ""

    for element in forecast:
        element = json.loads(list_sample)
        string += "{} ==> {}%H / {}°C\n".format(element['dt_txt'], element['main']['humidity'], round((element['main']['temp'] - 273.15), 1))
    
    print(string)

    hd_payload = json.JSONEncoder().encode({
        "HD_FEATURE": "HD_WEATHER",
        "HD_IDENTIFIER": "NONE",
        "HD_VALUE": string,
        "HD_TIMESTAMP": int(time())
    })
    return hd_payload



def weather_current():
    url = "http://api.openweathermap.org/data/2.5/weather?id={}&APPID={}".format(RENNES, APIKEY)
    res = urllib.request.urlopen(url)
    res_body = res.read()
    data = json.loads(res_body.decode("utf-8"))
    translator = Translator()
    date = datetime.datetime.fromtimestamp(data['dt'], tz)
    meteo_main = translator.translate(data['weather'][0]['main'], src='en', dest='fr').text
    meteo_description = translator.translate(data['weather'][0]['description'], src='en', dest='fr').text
    temperature = round((data['main']['temp'] - 273.15), 1)
    humidity = data['main']['humidity']
    couverture = data['clouds']['all']
    vent_vitesse = round(data['wind']['speed'] * 3.6)
    vent_deg = data['wind']['deg']
    vent_origin = ""
    if vent_deg in range(0, 12):
        vent_origin = "nord"
    elif vent_deg in range(12, 34):
        vent_origin = "nord-nord-est"
    elif vent_deg in range(34, 57):
        vent_origin = "nord-est"
    elif vent_deg in range(57, 79):
        vent_origin = "est-nord-est"
    elif vent_deg in range(79, 102):
        vent_origin = "est"
    elif vent_deg in range(102, 124):
        vent_origin = "est-sud-est"
    elif vent_deg in range(124, 147):
        vent_origin = "sud-est"
    elif vent_deg in range(147, 169):
        vent_origin = "sud-sud-est"
    elif vent_deg in range(169, 192):
        vent_origin = "sud"
    elif vent_deg in range(192, 214):
        vent_origin = "sud-sud-ouest"
    elif vent_deg in range(214, 237):
        vent_origin = "sud-ouest"
    elif vent_deg in range(237, 259):
        vent_origin = "ouest-sud-ouest"
    elif vent_deg in range(259, 282):
        vent_origin = "ouest"
    elif vent_deg in range(282, 304):
        vent_origin = "ouest-nord-ouest"
    elif vent_deg in range(304, 327):
        vent_origin = "nord-ouest"
    elif vent_deg in range(327, 349):
        vent_origin = "nord-nord-ouest"
    elif vent_deg in range(349, 361):
        vent_origin = "nord"

    string = "A {} {} {} degrer et {} pourcent dhumiditer {} pourcent de couverture nuageuse avec du vent {} a {} kilometre heure".format(date.strftime("%H:%M:%S"), meteo_description, temperature, humidity, couverture, vent_origin, vent_vitesse).replace('.', ',')

    hd_payload = json.JSONEncoder().encode({
        "HD_FEATURE": "HD_WEATHER",
        "HD_IDENTIFIER": "NONE",
        "HD_VALUE": string,
        "HD_TIMESTAMP": int(time())
    })
    return hd_payload


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
                mqtt_client.publish("inputs", weather_current())
            elif weather_type == "forecast":
                mqtt_client.publish("inputs", weather_forecast())
                
            
    except Exception as e:
        print("Error in event_manager(): {}".format(e))


if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
    mqtt_client.publish("inputs", weather_current())
    while True:
        sleep(1)
