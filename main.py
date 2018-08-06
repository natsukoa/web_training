from flask import Flask, jsonify, request
from calc import calc
import logging

app = Flask(__name__)
logging.basicConfig(
        format='%(asctime)s @%(name)s [%(levelname)s]:%(message)s',
        level = logging.DEBUG)

@app.route('/calc?<params>', methods=['GET'])
def executor(params):
    logging.info('start model update process')
    print(calc(params))
    logging.info('complete model update process')
    return jsonify({'result': 'complete update model'})



if __name__ == '__main__':
    app.run(host='172.31.15.95', port=8080)
    try:
        logging.info('API service started')
    finally:
        logging.info('API service stopped')