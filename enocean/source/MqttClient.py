import paho.mqtt.client as mqtt
from threading import Thread
from time import sleep
import config

mqtt_client = None


def on_connect(client, userdata, flag, rc):
    config.system_logger.debug(rc)
    if rc == 0:
        config.system_logger.debug('Connection ok')
    else:
        config.system_logger.debug('Connection ko, connected with result code'+str(rc))


def on_disconnect(client, userdata, rc):
    if rc != 0:
        config.system_logger.debug('Disconnected with result code' + str(rc))
        client.reconnect()
    else:
        config.system_logger.debug("Disconnected successfully")


class MqttClient(Thread):
    def __init__(self, addr, port, topic):
        Thread.__init__(self)
        config.system_logger.debug('Initialising mqtt client')
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = on_connect
        self.addr = addr
        self.port = port
        self.topic = topic

    def run(self):
        config.system_logger.debug('Connecting to broker '+self.addr+':'+str(self.port)+'...')
        connected = False
        while not connected:
            try:
                self.mqtt_client.connect(host=self.addr, port=self.port, keepalive=60)
                connected = True
            except:
                config.system_logger.debug('Error while connecting to mqtt broker '+self.addr+':'+str(self.port)+', trying again ...')
                sleep(5)

        self.mqtt_client.loop_forever()

    def publish(self, message):
        config.system_logger.debug('Publishing to broker '+self.addr+':'+str(self.port)+' in topic '+self.topic)
        rc, count = self.mqtt_client.publish(self.topic, message)
        if rc == 0:
            config.system_logger.debug('Publish '+str(count)+' ok')
        else:
            config.system_logger.debug('Publish '+str(count)+' ko, published with result '+self.publish_errors(rc))

    @staticmethod
    def publish_errors(error):
        if error == -1:
            return 'MQTT_ERR_AGAIN'
        elif error == 0:
            return 'MQTT_ERR_SUCCESS'
        elif error == 1:
            return 'MQTT_ERR_NOMEM'
        elif error == 2:
            return 'MQTT_ERR_PROTOCOL'
        elif error == 3:
            return 'MQTT_ERR_INVAL'
        elif error == 4:
            return 'MQTT_ERR_NO_CONN'
        elif error == 5:
            return 'MQTT_ERR_CONN_REFUSED'
        elif error == 6:
            return 'MQTT_ERR_NOT_FOUND'
        elif error == 7:
            return 'MQTT_ERR_CONN_LOST'
        elif error == 8:
            return 'MQTT_ERR_TLS'
        elif error == 9:
            return 'MQTT_ERR_PAYLOAD_SIZE'
        elif error == 10:
            return 'MQTT_ERR_NOT_SUPPORTED'
        elif error == 11:
            return 'MQTT_ERR_AUTH'
        elif error == 12:
            return 'MQTT_ERR_ACL_DENIED'
        elif error == 13:
            return 'MQTT_ERR_UNKNOWN'
        elif error == 14:
            return 'MQTT_ERR_ERRNO'


def create_mqtt_client(addr, port, topic):
    mqtt_cli_tmp = MqttClient(addr, port, topic)
    mqtt_cli_tmp.daemon = True
    mqtt_cli_tmp.start()
    return mqtt_cli_tmp
