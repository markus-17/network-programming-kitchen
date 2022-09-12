import time
import threading

import requests
from flask import Flask, request

from settings import COLORS, DINING_HALL_PORT, KITCHEN_PORT, TIME_UNIT, MENU, KITCHEN_HOSTNAME, NR_OF_COOKS


def kitchen_print(msg, color=COLORS.OKGREEN):
    print(f'{color}|-- KITCHEN --->>> {msg}')


class OrderList:
    def __init__(self):
        self.__order_list = []
        self.__lock = threading.Lock()

    def add_order(self, order):
        with self.__lock:
            self.__order_list.append(order)

    def is_empty(self):
        with self.__lock:
            return len(self.__order_list) == 0

    def pop_order(self):
        with self.__lock:
            return self.__order_list.pop()


flask_app = Flask(__name__)
order_list = OrderList()


@flask_app.route('/order', methods=['POST'])
def post_order():
    order = request.get_json()
    order_list.add_order(order)
    kitchen_print(
        f'Received Order {order["order_id"]} from Table {order["table_id"]}: ')
    return {'status_code': 200}


class Cook(threading.Thread):
    def __init__(self, cook_id, *args, **kwargs):
        super(Cook, self).__init__(*args, **kwargs)
        self.cook_id = cook_id

    def run(self):
        while True:
            if order_list.is_empty():
                time.sleep(0.1 * TIME_UNIT)
                continue

            order = order_list.pop_order()
            order = self.cook_order(order)
            _ = requests.post(
                url=f'http://{KITCHEN_HOSTNAME}:{DINING_HALL_PORT}/distribution',
                json=order
            )

    def cook_order(self, order):
        # This logic is just a placeholder for the moment
        cooking_time = max(MENU[i]["preparation-time"] for i in order['items'])
        time.sleep(cooking_time)
        order["cooking_time"] = cooking_time
        order['cooking_details'] = [
            {'food_id': food_id, 'cook_id': self.cook_id}
            for food_id in order['items']
        ]
        return order


if __name__ == '__main__':
    main_thread = threading.Thread(
        target=lambda: flask_app.run(
            host='0.0.0.0', port=KITCHEN_PORT, debug=False, use_reloader=False)
    )

    threads = [main_thread]

    for cook_id in range(1, NR_OF_COOKS + 1):
        cook = Cook(cook_id)
        threads.append(cook)

    for thread in threads:
        thread.start()
