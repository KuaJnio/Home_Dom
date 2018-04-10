import paho.mqtt.client as mqtt
from threading import Thread
from time import sleep

TOPICS = None


def on_connect(client, userdata, flags, rc):
    try:
        if rc == 0:
            print('Connection to broker OK')
        else:
            print('Connection to broker KO, with result code '+str(rc))
        for topic in TOPICS:
            client.subscribe(topic)
            print('Subscribed to \"'+topic+'\"')
    except Exception as e:
        print('Error in on_connect(): '+str(e))


def on_disconnect(client, userdata, rc):
    print('Disconnected from broker with result code '+str(rc))
    connected = False
    while not connected:
        try:
            print('Trying to reconnect to broker...')
            rc = client.reconnect()
        except Exception as e:
            print('Error in on_disconnect(): '+str(e))
            sleep(2)
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
            print('Error in MqttClient.__init__(): '+str(e))

    def run(self):
        try:
            self.mqtt_client.connect(host=self.addr, port=self.port)
            print('Connecting to broker '+self.addr+':'+str(self.port)+'...')
            self.mqtt_client.loop_forever()
        except Exception as e:
            print('Error in MqttClient.run(): '+str(e))

    def publish(self, topic, message):
        try:
            print('Publishing to broker '+self.addr+':'+str(self.port)+' in topic '+topic)
            rc, count = self.mqtt_client.publish(topic, message)
            if rc == 0:
                print('Publish OK')
            else:
                print('Publish KO, with result '+self.publish_errors(rc))
        except Exception as e:
            print('Error in MqttClient.publish(): '+str(e))

    @staticmethod
    def publish_errors(error):
        try:
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
        except Exception as e:
            print('Error in MqttClient.publish_errors(): '+str(e))


def create_mqtt_client(addr, port, on_message, topics):
    try:
        print('Creating mqtt client on broker : '+addr+':'+str(port))
        global TOPICS
        TOPICS = topics
        mqtt_cli_tmp = MqttClient(addr, port, on_message)
        mqtt_cli_tmp.daemon = True
        mqtt_cli_tmp.start()
        return mqtt_cli_tmp
    except Exception as e:
        print('Error in create_mqtt_client(): '+str(e))
