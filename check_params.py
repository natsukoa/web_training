

def check_params(params):
    print(params)
    result = []
    for param in params:
        if not param.isdecimal() and \
                param not in ['+', '-', '*', '/', '(', ')']:
            return 'ERROR'
        else:
            result.append(param)
    return ''.join(result)

