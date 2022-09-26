import math
import time
import queue
import threading
import itertools

import requests
from flask import Flask, request

from settings import COLORS, DINING_HALL_PORT, KITCHEN_PORT, TIME_UNIT, MENU, KITCHEN_HOSTNAME, COOKS_CONFIGURATIONS

flask_app = Flask(__name__)
cook_threads = []


def kitchen_print(msg, color=COLORS.OKGREEN):
    print(f'{color}|-- KITCHEN --->>> {msg}')


class OrderList:
    orders_in_progress_lock = threading.Lock()
    orders_in_progress = {}
    foods_to_prepare = {
        1: queue.Queue(),
        2: queue.Queue(),
        3: queue.Queue()
    }

    class Stove:
        foods_to_prepare = {
            1: queue.Queue(),
            2: queue.Queue(),
            3: queue.Queue()
        }
        # In the test configuration there is only 1 Stove
        stove_lock = threading.Lock()

    class Ovens:
        foods_to_prepare = {
            1: queue.Queue(),
            2: queue.Queue(),
            3: queue.Queue()
        }
        # In the test configuration there are 2 Ovens
        ovens_semaphore = threading.Semaphore(value=2)

    @staticmethod
    def handle_new_order(order):
        order_id = order['order_id']
        order['cooking_details'] = []

        with OrderList.orders_in_progress_lock:
            OrderList.orders_in_progress[order_id] = order

        for food_id in order['items']:
            complexity = MENU[food_id]['complexity']
            cooking_apparatus = MENU[food_id]['cooking-apparatus']

            if cooking_apparatus is None:
                OrderList.foods_to_prepare[complexity].put({
                    'food_id': food_id,
                    'order_id': order_id
                })
            elif cooking_apparatus == 'stove':
                OrderList.Stove.foods_to_prepare[complexity].put({
                    'food_id': food_id,
                    'order_id': order_id
                })
            elif cooking_apparatus == 'oven':
                OrderList.Ovens.foods_to_prepare[complexity].put({
                    'food_id': food_id,
                    'order_id': order_id
                })

    @staticmethod
    def give_prepared_food(food):
        with OrderList.orders_in_progress_lock:
            order_id = food['order_id']
            order_in_progress = OrderList.orders_in_progress[order_id]
            order_in_progress['cooking_details'].append(food)
            finished_foods = len(order_in_progress['cooking_details'])
            total_foods = len(order_in_progress['items'])
            done = (finished_foods == total_foods)
        
        kitchen_print(f'Ready!!! {food} - {finished_foods}/{total_foods}')

        if done:
            order_in_progress['cooking_time'] = (math.floor(time.time()) - order_in_progress['pick_up_time']) / TIME_UNIT
            cooks = set(food['cook_id'] for food in order_in_progress['cooking_details'])
            kitchen_print(f'The food for Table_{order_in_progress["table_id"]}, Waiter_{order_in_progress["waiter_id"]}, Order_{order_in_progress["order_id"]} was prepared by these cooks {cooks} in {order_in_progress["cooking_time"]} time units.')
            requests.post(
                url=f'http://{KITCHEN_HOSTNAME}:{DINING_HALL_PORT}/distribution',
                json=order_in_progress
            )


@flask_app.route('/order', methods=['POST'])
def post_order():
    order = request.get_json()
    kitchen_print(
        f'Received from Table_{order["table_id"]} using Waiter_{order["waiter_id"]} Order_{order["order_id"]} with items {order["items"]}'
    )
    OrderList.handle_new_order(order)
    return {'status_code': 200}


class CookThread(threading.Thread):
    def __init__(self, cook_id, rank, *args, **kwargs):
        super(CookThread, self).__init__(*args, **kwargs)
        self.cook_id = cook_id
        self.rank = rank

    def run(self):
        while True:
            # Work with the Oven 
            is_free = OrderList.Ovens.ovens_semaphore.acquire(timeout=0.01*TIME_UNIT)
            if is_free:
                for complexity in range(self.rank, 0, -1):
                    try:
                        food = OrderList.Ovens.foods_to_prepare[complexity].get_nowait()
                        self.prepare_food(food)
                        break
                    except queue.Empty:
                        pass
                    
                OrderList.Ovens.ovens_semaphore.release()

            # Work with Stove
            is_free = OrderList.Stove.stove_lock.acquire(timeout=0.01*TIME_UNIT)
            if is_free:
                for complexity in range(self.rank, 0, -1):
                    try:
                        food = OrderList.Stove.foods_to_prepare[complexity].get_nowait()
                        self.prepare_food(food)
                        break
                    except queue.Empty:
                        pass

                OrderList.Stove.stove_lock.release()

            # Work with Regular Orders
            for complexity in range(self.rank, 0, -1):
                try:
                    food = OrderList.foods_to_prepare[complexity].get(timeout=0.01*TIME_UNIT)
                    self.prepare_food(food)
                    break
                except queue.Empty:
                    pass

    def prepare_food(self, food):
        food_id = food['food_id']
        preparation_time = MENU[food_id]['preparation-time'] * TIME_UNIT
        time.sleep(preparation_time)
        food["cook_id"] = self.cook_id
        OrderList.give_prepared_food(food)


if __name__ == '__main__':
    server_thread = threading.Thread(
        target=lambda: flask_app.run(
            host='0.0.0.0', port=KITCHEN_PORT, debug=False, use_reloader=False)
    )

    for cook_id, cook_configuration in COOKS_CONFIGURATIONS.items():
        for _ in range(cook_configuration["proficiency"]):
            cook_thread = CookThread(cook_id, cook_configuration['rank'])
            cook_threads.append(cook_thread)

    for thread in itertools.chain([server_thread], cook_threads):
        thread.start()
