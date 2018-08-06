from flask import Flask, jsonify, request
from check_params import check_params
import logging

app = Flask(__name__)
logging.basicConfig(
        format='%(asctime)s @%(name)s [%(levelname)s]:%(message)s',
        level = logging.DEBUG)

@app.route('/calc/<params>', methods=['GET', 'POST'])
def executor(params=None):
    result = check_params(params)
    return str(eval(result))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    