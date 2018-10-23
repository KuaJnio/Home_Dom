import requests


def get_parameter(key):
    try:
        print("Getting parameter {}...".format(key))
        r = requests.get("http://192.168.1.23:8090/", timeout=1)
        return r.json().get(key, None)
    except Exception as e:
        print("Error...{}".format(e))
        return None
