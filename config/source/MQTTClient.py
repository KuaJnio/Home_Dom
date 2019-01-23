import paho.mqtt.client as mqtt
from threading import Thread
from time import sleep
import logging

TOPICS = None


def on_connect(client, userdata, flags, rc):
    try:
        if rc == 0:
            logging.info("Connection to broker OK")
        else:
            logging.warning("Connection to broker KO, with result code {}".format(rc))
        if TOPICS:
            for topic in TOPICS:
                client.subscribe(topic)
                logging.info("Subscribed to \"{}\"".format(topic))
    except Exception as e:
        logging.error("Error in on_connect(): {}".format(e))


def on_disconnect(client, userdata, rc):
    logging.warning("Disconnected from broker with result code {}".format(rc))
    connected = False
    while not connected:
        try:
            rc = client.reconnect()
        except Exception:
            sleep(1)
        if rc == 0:
            connected = True


class MqttClient(Thread):
    def __init__(self, addr, port, on_message):
        try:
            Thread.__init__(self)
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.on_connect = on_connect
            self.mqtt_client.on_disconnect = on_disconnect
            self.mqtt_client.on_message = on_message
            self.addr = addr
            self.port = port
        except Exception as e:
            logging.error("Error in MqttClient.__init__(): {}".format(e))

    def run(self):
        try:
            logging.info("Connecting to broker {}:{}...".format(self.addr, self.port))
            connected = False
            while not connected:
                try:
                    self.mqtt_client.connect(host=self.addr, port=self.port)
                    connected = True
                except Exception:
                    sleep(1)
            self.mqtt_client.loop_forever()
        except Exception as e:
            logging.error("Error in MqttClient.run(): {}".format(e))

    def publish(self, topic, message):
        try:
            #logging.debug("Publishing to broker {}:{} in topic {}".format(self.addr, self.port, topic))
            rc, count = self.mqtt_client.publish(topic, message)
            if rc == 0:
                #logging.debug("Publish OK")
                pass
            else:
                logging.warning("Publish KO, with result {}".format(self.publish_errors(rc)))
        except Exception as e:
            logging.error("Error in MqttClient.publish(): {}".format(e))

    @staticmethod
    def publish_errors(error):
        try:
            if error == -1:
                return "MQTT_ERR_AGAIN"
            elif error == 0:
                return "MQTT_ERR_SUCCESS"
            elif error == 1:
                return "MQTT_ERR_NOMEM"
            elif error == 2:
                return "MQTT_ERR_PROTOCOL"
            elif error == 3:
                return "MQTT_ERR_INVAL"
            elif error == 4:
                return "MQTT_ERR_NO_CONN"
            elif error == 5:
                return "MQTT_ERR_CONN_REFUSED"
            elif error == 6:
                return "MQTT_ERR_NOT_FOUND"
            elif error == 7:
                return "MQTT_ERR_CONN_LOST"
            elif error == 8:
                return "MQTT_ERR_TLS"
            elif error == 9:
                return "MQTT_ERR_PAYLOAD_SIZE"
            elif error == 10:
                return "MQTT_ERR_NOT_SUPPORTED"
            elif error == 11:
                return "MQTT_ERR_AUTH"
            elif error == 12:
                return "MQTT_ERR_ACL_DENIED"
            elif error == 13:
                return "MQTT_ERR_UNKNOWN"
            elif error == 14:
                return "MQTT_ERR_ERRNO"
        except Exception as e:
            logging.error("Error in MqttClient.publish_errors(): {}".format(e))


def create_mqtt_client(addr, port, on_message, topics):
    try:
        logging.info("Creating mqtt client on broker : {}:{}".format(addr, port))
        global TOPICS
        TOPICS = topics
        mqtt_cli_tmp = MqttClient(addr, port, on_message)
        mqtt_cli_tmp.daemon = True
        mqtt_cli_tmp.start()
        return mqtt_cli_tmp
    except Exception as e:
        logging.error("Error in create_mqtt_client(): {}".format(e))
