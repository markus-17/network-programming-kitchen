from flask import Flask, request

from OrderList import OrderList
from settings import kitchen_print


flask_app = Flask(__name__)

@flask_app.route('/order', methods=['POST'])
def post_order():
    order = request.get_json()
    kitchen_print(
        f'Received from Table_{order["table_id"]} using Waiter_{order["waiter_id"]} Order_{order["order_id"]} with items {order["items"]}'
    )
    OrderList.handle_new_order(order)
    return {'status_code': 200}
