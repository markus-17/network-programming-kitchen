import math
import time
import queue
import threading

import requests

from settings import MENU, kitchen_print, TIME_UNIT, KITCHEN_HOSTNAME, DINING_HALL_PORT


class OrderList:
    orders_priority_queue = queue.PriorityQueue()
    orders_in_progress_lock = threading.Lock()
    orders_in_progress = {}
    foods_to_prepare = {k: queue.Queue() for k in (1, 2, 3)}
    
    stove_foods_to_prepare = queue.Queue()
    oven_foods_to_prepare = queue.Queue()

    @staticmethod
    def handle_new_order():
        _, order = OrderList.orders_priority_queue.get()
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
                OrderList.stove_foods_to_prepare.put({
                    'food_id': food_id,
                    'order_id': order_id
                })
            elif cooking_apparatus == 'oven':
                OrderList.oven_foods_to_prepare.put({
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
