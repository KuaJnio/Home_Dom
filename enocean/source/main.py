#!/usr/bin/python
from SerialReader import create_serial_reader
from MqttClient import create_mqtt_client
from time import sleep
import sys
import signal


def signal_handler(signal, frame):
    print("Interpreted signal "+str(signal))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    try:
        broker = sys.argv[1]
        port = sys.argv[2]
        topic = sys.argv[3]
    except Exception as e:
        sys.exit(str(e))

    mqtt_client = create_mqtt_client(broker, port, topic)
    serial_thread = create_serial_reader('/dev/ttyENOCEAN', mqtt_client)
    while True:
        sleep(1)
    sys.exit(0)
