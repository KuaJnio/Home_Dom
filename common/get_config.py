import requests
import logging
from time import sleep


def get_parameter(key):
    while True:
        try:
            logging.info("Getting parameter {}...".format(key))
            r = requests.get("http://192.168.1.36:8090/", timeout=1)
            res = r.json().get(key, None)
            if res:
                return res
            else:
                logging.warning("Failed to get config {}".format(key))
        except Exception as e:
            logging.error("{}".format(e))
        sleep(3)
