from SerialReader import create_serial_reader
from time import sleep
import sys
import signal
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


def on_message(client, userdata, msg):
    print('New message from MQTT broker :')
    print('[TOPIC] : '+msg.topic)
    print('[PAYLOAD] : '+msg.payload)
    rc = event_manager(msg.topic, msg.payload)
    print('Message handled with result code '+str(rc))


def event_manager(topic, payload):
    try:
        pass
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    mqtt_client = create_mqtt_client(MQTT_BROKER, MQTT_PORT, on_message, MQTT_TOPICS)
    serial_thread = create_serial_reader('/dev/ttyENOCEAN', mqtt_client)
    while True:
        sleep(1)
