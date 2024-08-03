import signal
from gevent.pywsgi import WSGIServer
from main import app

address = "0.0.0.0"
port = 5000

# Start the server
http_server = WSGIServer((address, port), app)
http_server.serve_forever()
