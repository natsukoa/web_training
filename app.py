from flask import Flask, request
import logging
from db import DB

app = Flask(__name__)
logging.basicConfig(
    format='%(asctime)s @%(name)s [%(levelname)s]:%(message)s',
    level=logging.DEBUG)
db = DB()

@app.route('calc/<params>', defaults={'param2': '+0'}, methods=['GET'])
@app.route('calc/<params>/<param2>', methods=['GET'])
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


@app.route('stocker/addstock/<name>/<int:amount>', methods=['GET'])
def addstock(name, amount=1):
    """
    在庫の追加
    :param name: 
    :param amount: 
    :return: None
    """
    # amountの値チェック
    if type(amount) is not int or amount <= 0:
        return 'ERROR'

    sql = """SELECT amount FROM stock WHERE product_name = '{}';""".format(name)
    try:
        # 商品が在庫に存在する場合
        current_amount = db.execute(sql)

        new_amount = current_amount[0]['amount'] + amount
        sql = """UPDATE stock SET amount = {} WHERE product_name = '{}';""".format(
            new_amount, name)
        db.execute(sql)

    except:
        # 商品が在庫に存在しなかった場合
        sql = '''INSERT INTO stock VALUES ({}, {});'''.format(name, amount)
        try:
            db.execute(sql)
        except:
            return 'ERROR'
    return ''


@app.route('stocker/checkstock', methods=['GET'])
@app.route('stocker/checkstock/<name>', methods=['GET'])
def checkstock(name=None):
    """
    在庫チェック
    :param name: 
    :return: [name]: [amount]
    """
    # 商品名を指定されなかった場合
    if name is None:
        sql = """SELECT product_name, amount FROM stock;"""
        try:
            stock_sets = db.execute(sql)
            stocks = {stock['product_name']: stock['amount'] for stock in
                      stock_sets}
            result = ['{}: {}</br>'.format(k, v) for k, v in
                      sorted(stocks.items(), key=lambda x: x[0])]
            return ''.join(result)
        except:
            return 'ERROR'
    # 商品名を指定された場合
    else:
        sql = """SELECT amount FROM stock WHERE product_name = '{}';""".format(
            name)
        amount = db.execute(sql)
        return "{}: {}".format(name, amount[0]['amount'])


@app.route('stocker/sell/<name>', defaults={'amount': 1, 'price': 1}, methods=['GET'])
@app.route('stocker/sell/<name>/<int:amount>', defaults={'price': 1}, methods=['GET'])
@app.route('stocker/sell/<name>/<int:amount>/<float:price>', methods=['GET'])
def sell(name, amount=1, price=0):
    """
    販売
    :param name: 
    :param amount: 
    :param price: 
    :return: None
    """
    # amountの値チェック
    if type(amount) is not int or amount <= 0:
        return 'ERROR'
    # if (type(price) is not int or type(price) is not float) or price <= 0:
    if price <= 0:
        return 'ERROR'

    try:
        # 在庫テーブルの商品数を確認
        sql = """SELECT amount FROM stock WHERE product_name = '{}';""".format(
            name)
        current_amount = db.execute(sql)
        # 在庫テーブルをUPDATE
        sql1 = """UPDATE stock SET amount = {} WHERE product_name = '{}';""".format(
            current_amount[0]['amount'] - (amount * price), name)
        # 販売テーブルをUPDATE
        sql2 = """UPDATE sell SET amount = {} WHERE product_name = '{}';""".format(
            (amount * price), name)
        db.execute(sql1)
        db.execute(sql2)
    except:
        return 'ERROR'
    return ''


@app.route('stocker/checksales', methods=['GET'])
def checksales():
    """
    売上チェック
    :return:  sales: [sales]
    """
    sql = """SELECT amount FROM sell;"""
    try:
        amount = db.execute(sql)
        result = [row['amount'] for row in amount]
    except:
        return 'ERROR'
    return 'sales: {}'.format(sum(result))


@app.route('stocker/deleteall', methods=['GET'])
def deleteall():
    """
    テーブルの全削除
    :return: None
    """
    try:
        sql1 = """DROP TABLE IF EXISTS stock CASCADE;"""
        db.execute(sql1)
        sql2 = """DROP TABLE IF EXISTS sell CASCADE;"""
        db.execute(sql2)
        sql3 = """
        CREATE TABLE stock
            (
              product_name varchar not null
                constraint stock_pkey
                primary key,
              amount       integer,
              price        numeric
            );
        """
        db.execute(sql3)
        sql4 = """
        CREATE TABLE sell
                (
                  product_name char    not null
                    constraint sell_pkey
                    primary key,
                  amount       integer not null
                );
        """
        db.execute(sql4)
    except:
        return "ERROR"
    return ''


if __name__ == '__main__':
    app.run()
