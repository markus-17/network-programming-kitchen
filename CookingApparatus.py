import time
import queue
import threading

from settings import MENU, TIME_UNIT
from OrderList import OrderList


class Stove(threading.Thread):
    foods_to_prepare = queue.Queue()

    def __init__(self, *args, **kwargs):
        super(Stove, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            food = Stove.foods_to_prepare.get()
            food_id = food['food_id']
            preparation_time = MENU[food_id]['preparation-time'] * TIME_UNIT
            time.sleep(preparation_time)
            OrderList.submit_cooking_apparatus_prepared_foods(food)


class Oven(threading.Thread):
    foods_to_prepare = queue.Queue()

    def __init__(self, *args, **kwargs):
        super(Oven, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            food = Oven.foods_to_prepare.get()
            food_id = food['food_id']
            preparation_time = MENU[food_id]['preparation-time'] * TIME_UNIT
            time.sleep(preparation_time)
            OrderList.submit_cooking_apparatus_prepared_foods(food)
