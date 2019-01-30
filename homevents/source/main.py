from flask import Flask, request, jsonify
import sys
from time import sleep
import logging
import json
import signal
from threading import Thread
from MQTTClient import create_mqtt_client
from get_config import get_parameter
import cep
import database
from homedom_logger import set_logger
set_logger("homevents", logging.DEBUG)


app = Flask(__name__)

mqtt_client = None
regexs_handler = None
rules_handler = None
config_handler = None
database_handler = None

MQTT_HOST = get_parameter("mqtt_host")
MQTT_PORT = get_parameter("mqtt_port")
MQTT_TOPICS = ["#"]


@app.route('/config', methods=['GET'])
def get_config():
    try:
        logging.info(request.method + " " + request.url + " ...")
        data = config_handler.get_config()
        return jsonify(data)
    except Exception as e:
        logging.error("Error in get_config: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/regexs', methods=['GET'])
def get_regexs():
    try:
        logging.info(request.method + " " + request.url + " ...")
        regexs = config_handler.get_regexs()
        return jsonify(regexs)
    except Exception as e:
        logging.error("Error in get_regexs: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/regex/<string:regex_name>', methods=['GET'])
def get_regex_by_name(regex_name):
    try:
        logging.info(request.method + " " + request.url + " ...")
        if config_handler.has_regex(regex_name):
            return jsonify(config_handler.get_regex_by_name(regex_name))
        else:
            return jsonify({'error': 'regex not found'}), 404
    except Exception as e:
        logging.error("Error in get_regex_by_name: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/regex/<string:regex_name>', methods=['PUT'])
def add_regex(regex_name):
    try:
        logging.info(request.method + " " + request.url + " ...")
        data = request.data
        regex = json.loads(data)
        if config_handler.is_regex(regex):
            if config_handler.has_regex(regex_name):
                config_handler.add_regex(regex_name, regex)
                restart()
                return '', 204
            else:
                config_handler.add_regex(regex_name, regex)
                restart()
                return '', 201
        else:
            return jsonify({"error": "bad regex format"}), 400
    except Exception as e:
        logging.error("Error in add_regex: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/regex/<string:regex_name>', methods=['DELETE'])
def del_regex(regex_name):
    try:
        logging.info(request.method + " " + request.url + " ...")
        if config_handler.has_regex(regex_name):
            config_handler.del_regex(regex_name)
            restart()
            return '', 204
        else:
            return jsonify({'error': 'regex not found'}), 404
    except Exception as e:
        logging.error("Error in del_regex: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/regex/<string:regex_name>/enable', methods=['POST'])
def enable_regex(regex_name):
    try:
        logging.info(request.method + " " + request.url + " ...")
        if config_handler.has_regex(regex_name):
            config_handler.enable_regex(regex_name)
            restart()
            return '', 204
        else:
            return jsonify({'error': 'regex not found'}), 404
    except Exception as e:
        logging.error("Error in enable_regex: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/regex/<string:regex_name>/disable', methods=['POST'])
def disable_regex(regex_name):
    try:
        logging.info(request.method + " " + request.url + " ...")
        if config_handler.has_regex(regex_name):
            config_handler.disable_regex(regex_name)
            restart()
            return '', 204
        else:
            return jsonify({'error': 'regex not found'}), 404
    except Exception as e:
        logging.error("Error in disable_regex: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/rules', methods=['GET'])
def get_rules():
    try:
        logging.info(request.method + " " + request.url + " ...")
        rules = config_handler.get_rules()
        return jsonify(rules)
    except Exception as e:
        logging.error("Error in get_rules: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/rule/<string:rule_name>', methods=['GET'])
def get_rule_by_name(rule_name):
    try:
        logging.info(request.method + " " + request.url + " ...")
        if config_handler.has_rule(rule_name):
            return jsonify(config_handler.get_rule_by_name(rule_name))
        else:
            return jsonify({'error': 'rule not found'}), 404
    except Exception as e:
        logging.error("Error in get_rule_by_name: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/rule/<string:rule_name>', methods=['PUT'])
def add_rule(rule_name):
    try:
        logging.info(request.method + " " + request.url + " ...")
        data = request.data
        rule = json.loads(data)
        if config_handler.is_rule(rule):
            if config_handler.has_rule(rule_name):
                config_handler.add_rule(rule_name, rule)
                restart()
                return '', 204
            else:
                config_handler.add_rule(rule_name, rule)
                restart()
                return '', 201
        else:
            return jsonify({"error": "bad rule format"}), 400
    except Exception as e:
        logging.error("Error in add_rule: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/rule/<string:rule_name>', methods=['DELETE'])
def del_rule(rule_name):
    try:
        logging.info(request.method + " " + request.url + " ...")
        if config_handler.has_rule(rule_name):
            config_handler.del_rule(rule_name)
            restart()
            return '', 204
        else:
            return jsonify({'error': 'rule not found'}), 404
    except Exception as e:
        logging.error("Error in del_rule: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/rule/<string:rule_name>/enable', methods=['POST'])
def enable_rule(rule_name):
    try:
        logging.info(request.method + " " + request.url + " ...")
        if config_handler.has_rule(rule_name):
            config_handler.enable_rule(rule_name)
            restart()
            return '', 204
        else:
            return jsonify({'error': 'rule not found'}), 404
    except Exception as e:
        logging.error("Error in enable_rule: " + str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/rule/<string:rule_name>/disable', methods=['POST'])
def disable_rule(rule_name):
    try:
        logging.info(request.method + " " + request.url + " ...")
        if config_handler.has_rule(rule_name):
            config_handler.disable_rule(rule_name)
            restart()
            return '', 204
        else:
            return jsonify({'error': 'rule not found'}), 404
    except Exception as e:
        logging.error("Error in disable_rule: " + str(e))
        return jsonify({"error": str(e)}), 500


def parse_config():
    try:
        with open(app.root_path + '/config.json') as json_data_file:
            data = json.load(json_data_file)
            if config_handler.is_config(data):

                for regex in data['regexs']:
                    if data['regexs'][regex]['enabled']:
                        global regexs_handler
                        regexs_handler.add_regex(regex, data['regexs'][regex]['value'])

                for rule in data['rules']:
                    regexTest = True
                    if data['rules'][rule]['enabled']:
                        reg_list = []
                        for regex in data['rules'][rule]['regexs_yes']:
                            reg_list.append(data['rules'][rule]['regexs_yes'][regex])
                        if regexTest:
                            cep.create_rule(regexs_yes=reg_list, regexs_no=data['rules'][rule]['regexs_no'], window=data['rules'][rule]["window"], hold=data['rules'][rule]["hold"], mode=data['rules'][rule]["mode"], mqtt_client=mqtt_client, rules_handler=rules_handler, name=data['rules'][rule]["name"], output_topic=data['rules'][rule]["output_topic"])
            else:
                raise Exception('Bad config format, aborting...')
    except Exception as e:
        logging.error('Error in parse_config: ' + str(e))


def restart():
    logging.info('Restarting CEP...')
    global rules_handler
    rules_handler.reset()
    global regexs_handler
    regexs_handler.reset()
    parse_config()


def on_message(client, userdata, msg):
    try:
        payload = str(msg.payload, 'utf-8')
        payload_consumer = cep.PayloadConsumer(payload, rules_handler, regexs_handler, database_handler)
        payload_consumer.start()
    except Exception as e:
        logging.error('Error in on_message: ' + str(e))


def signal_term_handler(signal, frame):
    logging.info('Catched signal SIGTERM')
    logging.info('Executing some actions before exiting process...')
    try:
        pass
    except Exception as e:
        logging.error('Error in signal_term_handler: ' + str(e))
    logging.info('Done handling signal SIGTERM, exiting now!')
    sys.exit(0)


def create_healthcheck(app_name):
    class HealthCheck(Thread):
        def __init__(self, name):
            Thread.__init__(self)
            self.name = name

        def run(self):
            try:
                while True:
                    mqtt_client.publish("status", self.name)
                    sleep(1)
            except Exception as e:
                logging.error("Error in HealthCheck.run(): {}".format(e))

    healthcheck = HealthCheck(app_name)
    healthcheck.daemon = True
    healthcheck.start()


if __name__ == '__main__':
    try:
        signal.signal(signal.SIGTERM, signal_term_handler)

        database_handler = database.DatabaseHandler(":memory:")
        #database_handler = database.DatabaseHandler("database.db")

        regexs_handler = cep.RegexsHandler()
        rules_handler = cep.create_rules_handler(database_handler)
        mqtt_client = mqtt_client = create_mqtt_client(MQTT_HOST, MQTT_PORT, on_message, MQTT_TOPICS)
        config_handler = cep.ConfigHandler()
        sleep(1)
        parse_config()
        create_healthcheck("homevents")
        logging.info("Initializing server...")
        app.run(host='0.0.0.0', port=80)
    except Exception as e:
        logging.error('Error in main: ' + str(e))
