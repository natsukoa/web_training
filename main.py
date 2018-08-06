from flask import Flask, request
import logging

app = Flask(__name__)
logging.basicConfig(
        format='%(asctime)s @%(name)s [%(levelname)s]:%(message)s',
        level = logging.DEBUG)

@app.route('/<params>', defaults={'param2': '+0'}, methods=['GET'])
@app.route('/<params>/<param2>', methods=['GET'])
def executor(params, param2):
    params = request.path[1:]
    result = []
    for param in params:
        if not param.isdecimal() and \
                param not in ['+', '-', '*', '/', '(', ')']:
            return 'ERROR'
        else:
            result.append(param)
    return str(eval(''.join(result)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    