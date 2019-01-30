from time import time, sleep
from re import search
from threading import Thread, Lock
from json import JSONEncoder, load, dump
import logging


class PayloadConsumer(Thread):
    def __init__(self, payload, rules_handler, regexs_handler, database_handler):
        Thread.__init__(self)
        self.payload = payload
        self.rules_handler = rules_handler
        self.regexs_handler = regexs_handler
        self.database_handler = database_handler

    def look_for_regexs(self):
        try:
            result = []
            for regex in self.regexs_handler.regexs:
                r = search(self.regexs_handler.regexs[regex], self.payload)
                if r is not None:
                    result.append(regex)
            return result
        except Exception as e:
            logging.error('Error in PayloadConsumer.look_for_regexs: ' + str(e))
            return result

    def run(self):
        try:
            matches = self.look_for_regexs()
            for match in matches:
                timestamp = int(time())
                self.database_handler.insert_match(timestamp, match)
                self.rules_handler.handle_match(match, self.payload)
                logging.debug("Got match for regex " + match)
        except Exception as e:
            logging.error('Error in PayloadConsumer.run: ' + str(e))


class RegexsHandler(object):
    def __init__(self):
        try:
            self.regexs = {}
        except Exception as e:
            logging.error('Error in RegexsHandler.__init__: ' + str(e))

    def add_regex(self, name, value):
        try:
            self.regexs[name] = value
            logging.debug("Added regex " + name + " : " + value)
        except Exception as e:
            logging.error('Error in RegexsHandler.add_regex: ' + str(e))

    def reset(self):
        del self.regexs
        self.regexs = {}


class Rule(object):
    def __init__(self, regexs_yes, regexs_no, window, mode, hold, name, output_topic, mqtt_client):
        try:
            self.regexs_yes = regexs_yes
            self.regexs_no = regexs_no
            self.window = window
            self.mode = mode
            self.hold = hold
            self.name = name
            self.mqtt_client = mqtt_client
            self.output_topic = output_topic

            self.callback_template = None
            self.pending = False
            self.remaining_regexs = list(self.regexs_yes)
            self.start_time = None
            self.completed = False
            self.completed_time = None
            self.triggering_payloads = {}

        except Exception as e:
            logging.error('Error in Rule.__init__: ' + str(e))

    def has_regex(self, regex):
        try:
            if not len(self.remaining_regexs) == 0:
                if self.mode == "strict":
                    if self.remaining_regexs[0] == regex:
                        return True
                    else:
                        return False
                else:
                    if regex in self.remaining_regexs:
                        return True
                    else:
                        return False
            else:
                return False
        except Exception as e:
            logging.error('Error in Rule.has_regex: ' + str(e))
            return False

    def is_completed(self):
        return self.completed

    def complete(self):
        self.completed = True
        self.completed_time = time()

    def is_finished(self):
        res = False
        if ((len(self.remaining_regexs) == 0) or (self.mode == "one")):
            res = True
        return res

    def is_expired(self):
        return time() - self.start_time > self.window

    def is_on_hold(self):
        return time() - self.completed_time < self.hold

    def del_regex(self, regex):
        try:
            del self.remaining_regexs[self.remaining_regexs.index(regex)]
        except Exception as e:
            logging.error('Error in Rule.del_regex: ' + str(e))

    def reset_rule(self):
        try:
            self.pending = False
            self.completed = False
            self.completed_time = None
            self.remaining_regexs = list(self.regexs_yes)
            self.triggering_payloads = {}
            self.callback_payload = ""
        except Exception as e:
            logging.error('Error in Rule.reset_rule: ' + str(e))

    def start_rule(self):
        try:
            self.pending = True
            self.start_time = time()
            logging.debug("Initiated rule " + self.name)
        except Exception as e:
            logging.error('Error in Rule.start_rule: ' + str(e))

    def callback(self):
        try:
            #TODO support jinja template to format callback payload
            self.callback_payload = JSONEncoder().encode(
                {
                    "timestamp": int(time()),
                    "name": self.name,
                    "triggering_payload": self.triggering_payloads
                }
            )
            logging.info('Triggered rule \'' + self.name + '\'')
            self.mqtt_client.publish(self.output_topic, self.callback_payload)
        except Exception as e:
            logging.error('Error in Rule.callback: ' + str(e))


class RulesHandler(Thread):
    def __init__(self, database_handler):
        Thread.__init__(self)
        self.rules = []
        self.database_handler = database_handler

    def add_rule(self, rule):
        try:
            self.rules.append(rule)
        except Exception as e:
            logging.error('Error in RulesHandler.add_rule: ' + str(e))

    def check_rules(self):
        try:
            for rule in self.rules:
                if rule.pending:
                    if rule.completed:
                        if rule.is_on_hold():
                            pass
                        else:
                            trigger = True
                            for value in rule.regexs_no:
                                timestamp = int(time()) - rule.regexs_no[value]
                                if self.database_handler.check_for_value(timestamp, value):
                                    logging.debug("Cancelling rule " + rule.name + " because \'regex_no\' " + value + " was found in the last " + str(rule.regexs_no[value]) + " seconds")
                                    trigger = False
                            if trigger:
                                rule.callback()
                            else:
                                pass
                            rule.reset_rule()
                    else:
                        if rule.is_finished():
                            rule.complete()
                        elif rule.is_expired():
                            rule.reset_rule()
                            logging.debug("Reseted rule " + rule.name + " because of expiration")
        except Exception as e:
            logging.error('Error in RulesHandler.check_rules: ' + str(e))

    def handle_match(self, name, payload):
        try:
            for rule in self.rules:
                if rule.pending:
                    if rule.has_regex(name):
                        rule.del_regex(name)
                        rule.triggering_payloads[name] = payload
                else:
                    if rule.has_regex(name):
                        rule.start_rule()
                        rule.triggering_payloads[name] = payload
                        rule.del_regex(name)
        except Exception as e:
            logging.error('Error in RulesHandler.handle_match: ' + str(e))

    def reset(self):
        del self.rules
        self.rules = []

    def run(self):
        try:
            while True:
                self.check_rules()
                sleep(0.05)
        except Exception as e:
            logging.error('Error in RulesHandler.run: ' + str(e))


def create_rules_handler(database_handler):
    rules_handler = RulesHandler(database_handler)
    rules_handler.daemon = True
    rules_handler.start()
    return rules_handler


def create_rule(regexs_yes, regexs_no, window, mode, hold, name, output_topic, mqtt_client, rules_handler):
    isPresent = False
    for rule in rules_handler.rules:
        if rule.name == name:
            isPresent = True

    if not isPresent:
        rule = Rule(regexs_yes, regexs_no, window, mode, hold, name, output_topic, mqtt_client)
        rules_handler.add_rule(rule)
        logging.debug("Added rule " + name)
    else:
        logging.error('Tried to add rule with name ' + name + ' but a rule with the same name already exists, aborting...')


class ConfigHandler(object):
    def __init__(self):
        self.file_name = "config.json"
        self.lock = Lock()

    def get_config(self):
        self.lock.acquire()
        with open(self.file_name, 'r') as f:
            data = load(f)
            self.lock.release()
            return data

    def has_regex(self, name):
        self.lock.acquire()
        with open(self.file_name, 'r') as f:
            data = load(f)
            self.lock.release()
            return name in data['regexs']

    def add_regex(self, name, regex):
        self.lock.acquire()
        with open(self.file_name, 'r+') as f:
            data = load(f)
            data['regexs'][name] = regex
            f.seek(0)
            dump(data, f, indent=4)
            f.truncate()
        self.lock.release()

    def del_regex(self, name):
        self.lock.acquire()
        with open(self.file_name, 'r+') as f:
            data = load(f)
            del data['regexs'][name]
            f.seek(0)
            dump(data, f, indent=4)
            f.truncate()
        self.lock.release()

    def get_regexs(self):
        self.lock.acquire()
        with open(self.file_name, 'r') as f:
            data = load(f)
            self.lock.release()
            return data['regexs']

    def get_regex_by_name(self, name):
        self.lock.acquire()
        with open(self.file_name, 'r') as f:
            data = load(f)
            self.lock.release()
            return data['regexs'][name]

    def enable_regex(self, name):
        self.lock.acquire()
        with open(self.file_name, 'r+') as f:
            data = load(f)
            data['regexs'][name]['enabled'] = True
            f.seek(0)
            dump(data, f, indent=4)
            f.truncate()
            self.lock.release()

    def disable_regex(self, name):
        self.lock.acquire()
        with open(self.file_name, 'r+') as f:
            data = load(f)
            data['regexs'][name]['enabled'] = False
            f.seek(0)
            dump(data, f, indent=4)
            f.truncate()
            self.lock.release()

    def has_rule(self, name):
        self.lock.acquire()
        with open(self.file_name, 'r') as f:
            data = load(f)
            self.lock.release()
            return name in data['rules']

    def add_rule(self, name, rule):
        self.lock.acquire()
        with open(self.file_name, 'r+') as f:
            data = load(f)
            data['rules'][name] = rule
            f.seek(0)
            dump(data, f, indent=4)
            f.truncate()
        self.lock.release()

    def del_rule(self, name):
        self.lock.acquire()
        with open(self.file_name, 'r+') as f:
            data = load(f)
            del data['rules'][name]
            f.seek(0)
            dump(data, f, indent=4)
            f.truncate()
        self.lock.release()

    def get_rules(self):
        self.lock.acquire()
        with open(self.file_name, 'r') as f:
            data = load(f)
            self.lock.release()
            return data['rules']

    def get_rule_by_name(self, name):
        self.lock.acquire()
        with open(self.file_name, 'r') as f:
            data = load(f)
            self.lock.release()
            return data['rules'][name]

    def enable_rule(self, name):
        self.lock.acquire()
        with open(self.file_name, 'r+') as f:
            data = load(f)
            data['rules'][name]['enabled'] = True
            f.seek(0)
            dump(data, f, indent=4)
            f.truncate()
            self.lock.release()

    def disable_rule(self, name):
        self.lock.acquire()
        with open(self.file_name, 'r+') as f:
            data = load(f)
            data['rules'][name]['enabled'] = False
            f.seek(0)
            dump(data, f, indent=4)
            f.truncate()
            self.lock.release()

    def is_regex(self, data):
        if len(data) == 2 and 'value' in data and 'enabled' in data:
            if isinstance(data['value'], str) and isinstance(data['enabled'], bool):
                pass
            else:
                return False
        else:
            return False
        return True

    def is_rule(self, data):
        if len(data) == 8 and 'enabled' in data and 'name' in data and 'regexs_yes' in data and 'regexs_no' in data and 'mode' in data and 'hold' in data and 'window' in data and 'output_topic' in data:
            if isinstance(data['enabled'], bool) and isinstance(data['name'], str) and isinstance(data['regexs_yes'], dict) and isinstance(data['regexs_no'], dict) and isinstance(data['mode'], str) and isinstance(data['window'], int) and isinstance(data['hold'], int) and isinstance(data['output_topic'], str):
                for regex in data['regexs_yes']:
                    if isinstance(data['regexs_yes'][regex], str):
                        pass
                    else:
                        return False
            else:
                return False
        else:
            return False
        return True

    def is_config(self, data):
        if len(data) == 2 and 'regexs' in data and 'rules' in data:
            if isinstance(data['regexs'], dict) and isinstance(data['rules'], dict):
                for regex in data['regexs']:
                    if self.is_regex(data['regexs'][regex]):
                        pass
                    else:
                        return False
                for rule in data['rules']:
                    if self.is_rule(data['rules'][rule]):
                        pass
                    else:
                        return False
            else:
                return False
        else:
            return False
        return True
