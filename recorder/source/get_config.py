import requests


def get_parameter(key):
    try:
        print("Getting parameter {}...".format(key))
        r = requests.get("http://192.168.1.13:8090/", timeout=1)
        return r.json().get(key, None)
    except:
        print("Error...")
        return None
