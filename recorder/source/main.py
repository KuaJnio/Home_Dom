from influxdb import InfluxDBClient
import signal
from time import sleep
import json
import sys
from MQTTClient import create_mqtt_client
from get_config import get_parameter


def signal_handler(signal, frame):
    print("Interpreted signal "+str(signal)+", exiting now...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = get_parameter("recorder_topics")

mqtt_client = None

INFLUX_HOST = get_parameter("influx_host")
INFLUX_PORT = get_parameter("influx_port")
INFLUX_USER = get_parameter("influx_user")
INFLUX_PASSWD = get_parameter("influx_password")
INFLUX_DATABASE = get_parameter("influx_database")

influxdb_client = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT, username=INFLUX_USER, password=INFLUX_PASSWD, database=INFLUX_DATABASE)


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
        feature = json_payload['HD_FEATURE']
        identifier = json_payload['HD_IDENTIFIER']
        value = json_payload['HD_VALUE']
        
        json_body = [
            {
                "measurement": feature,
                "tags": {
                    "identifier": identifier
                },
                "fields": {
                    "value": value
                }
            }
        ]
        influxdb_client.write_points(json_body)
        return "OK"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
    while True:
        sleep(1)
