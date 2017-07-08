from flask import Flask, request, redirect, url_for, render_template, Response
from gevent.wsgi import WSGIServer
from functools import wraps

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == '' and password == ''


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)

@app.route('/')
@requires_auth
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='', port=800, debug=True)
    #http_server = WSGIServer(('', 80), app)
    #http_server.serve_forever()
