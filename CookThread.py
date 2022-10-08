import time
import queue
import threading

from OrderList import OrderList
from settings import TIME_UNIT, MENU
from CookingApparatus import Stove, Oven


class CookThread(threading.Thread):
    def __init__(self, cook_id, rank, *args, **kwargs):
        super(CookThread, self).__init__(*args, **kwargs)
        self.cook_id = cook_id
        self.rank = rank

    def run(self):
        while True:
            for complexity in range(self.rank, 0, -1):
                # Check if there are foods to put in cooking apparatus
                self.send_cooking_apparatus_foods()
                # Submit any Prepared foods from cooking apparatus
                OrderList.submit_cooking_apparatus_prepared_foods()

                try:
                    food = OrderList.foods_to_prepare[complexity].get(timeout=0.01*TIME_UNIT)
                    self.prepare_food(food)
                    break
                except queue.Empty:
                    pass

    def send_cooking_apparatus_foods(self):
        # Work with Cooking Apparatus
        for complexity in range(self.rank, 0, -1):
            while True:
                try:
                    food = OrderList.cooking_apparatus_to_prepare_foods[complexity].get_nowait()
                    food['cook_id'] = self.cook_id
                    cooking_apparatus = MENU[food['food_id']]['cooking-apparatus']
                    food['cooking-apparatus'] = cooking_apparatus
                    if cooking_apparatus == 'oven':
                        Oven.foods_to_prepare.put(food)
                    elif cooking_apparatus == 'stove':
                        Stove.foods_to_prepare.put(food)
                except queue.Empty:
                    break

    def prepare_food(self, food):
        food_id = food['food_id']
        preparation_time = MENU[food_id]['preparation-time'] * TIME_UNIT
        
        segments = 32
        for _ in range(segments):
            # Check if there are foods to put in cooking apparatus
            self.send_cooking_apparatus_foods()
            # Submit any Prepared foods from cooking apparatus
            OrderList.submit_cooking_apparatus_prepared_foods()
            time.sleep(preparation_time / segments)
        
        food["cook_id"] = self.cook_id
        OrderList.give_prepared_food(food)
