import requests
import logging


def get_parameter(key):
    try:
        logging.info("Getting parameter {}...".format(key))
        r = requests.get("http://192.168.1.16:8090/", timeout=30)
        return r.json().get(key, None)
    except Exception as e:
        logging.error("{}".format(e))
        return None
