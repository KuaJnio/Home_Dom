from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/')
def config():
    try:
        data = json.load(open('config.json'))
        return jsonify(data), 200
    except Exception as e:
        print("Error in config: "+str(e))
        return str(e), 500

def main():
    try:
        print("Initializing config server...")
        app.run(host='0.0.0.0', port=80)
    except Exception as e:
        print('Error in main: '+str(e))

if __name__ == '__main__':
    main()
