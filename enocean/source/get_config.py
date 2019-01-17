import requests
import logging


def get_parameter(key):
    try:
        logging.debug("Getting parameter {}...".format(key))
        r = requests.get("http://192.168.1.16:8090/", timeout=1)
        return r.json().get(key, None)
    except Exception as e:
        logging.debug("Error...{}".format(e))
        return None
