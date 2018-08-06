

def calc(params):
    print(params)
    result = []
    for param in params:
        print(param)
        if not param.isdecimal() and \
                param not in ['+', '-', '*', '/', '(', ')']:
            return 'ERROR'
        else:
            if param.isdecimal():
                result.append(int(param))
            else:
                result.append(param)
    return result

