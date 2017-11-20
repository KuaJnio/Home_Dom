from influxdb import InfluxDBClient
import signal
from time import sleep
import json
import sys
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

INFLUX_HOST = sys.argv[4]
INFLUX_PORT = sys.argv[5]
INFLUX_USER = sys.argv[6]
INFLUX_PASSWD = sys.argv[7]
INFLUX_DATABASE = sys.argv[8]

influxdb_client = InfluxDBClient(host=INFLUX_HOST, port=int(INFLUX_PORT), username=INFLUX_USER, password=INFLUX_PASSWD, database=INFLUX_DATABASE)


def on_message(client, userdata, msg):
    print('New message from MQTT broker')
    rc = event_manager(msg.topic, msg.payload)
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
    mqtt_client = create_mqtt_client(MQTT_BROKER, MQTT_PORT, on_message, MQTT_TOPICS)
    while True:
        sleep(1)

