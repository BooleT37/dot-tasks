from flask import Flask, send_from_directory, send_file

from api import setup_api

app = Flask(__name__)


@app.route('/static/<path:path>')
def send_static_file(path):
    return send_from_directory('static', path)


@app.route('/swagger-specs/<path:path>')
def send_swagger_json(path):
    return send_from_directory('swagger-specs', path)


@app.route('/swagger')
def swagger():
    return send_file('./static/swagger.html')


setup_api(app)

app.run(debug=True, use_debugger=False, use_reloader=False)