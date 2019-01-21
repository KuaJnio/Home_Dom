from flask import Flask, jsonify
import json
import logging
from homedom_logger import set_logger
set_logger("config", logging.DEBUG)

app = Flask(__name__)


@app.route('/')
def config():
    try:
        data = json.load(open('config.json'))
        return jsonify(data), 200
    except Exception as e:
        logging.error("Error in config: " + str(e))
        return str(e), 500


def main():
    try:
        logging.debug("Initializing config server...")
        app.run(host='0.0.0.0', port=80)
    except Exception as e:
        logging.error('Error in main: ' + str(e))


if __name__ == '__main__':
    main()
