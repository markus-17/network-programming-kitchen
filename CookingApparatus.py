from asyncore import read
import enum
import time
import queue
import threading

from settings import TIME_UNIT, MENU, kitchen_print, COLORS
from OrderList import OrderList


class Oven(threading.Thread):
    def __init__(self, id, *args, **kwargs):
        super(Oven, self).__init__(*args, **kwargs)
        self.id = id
    
    def run(self):
        in_progress = []
        simultaneous_foods = 2
        while True:
            # Fix this later
            # kitchen_print(f'Oven({self.id}) -> {in_progress}', color=COLORS.OKCYAN)

            while len(in_progress) < simultaneous_foods:
                try:
                    food = OrderList.oven_foods_to_prepare.get(timeout=0.01 * TIME_UNIT)
                    food['cooked_for'] = 0
                    in_progress.append(food)
                except queue.Empty:
                    break

            ready = []
            for i, food in enumerate(in_progress):
                time.sleep(TIME_UNIT)
                food['cooked_for'] += 1
                food_id = food['food_id']
                preparation_time = MENU[food_id]["preparation-time"]
                if food['cooked_for'] >= preparation_time:
                    ready.append(i)

            for ready_id in ready[::-1]:
                food = in_progress.pop(ready_id)
                # FIX THIS LATER
                food['cook_id'] = 999_999
                OrderList.give_prepared_food(food)


class Stove(threading.Thread):
    def __init__(self, id, *args, **kwargs):
        super(Stove, self).__init__(*args, **kwargs)
        self.id = id
    
    def run(self):
        in_progress = []
        simultaneous_foods = 2
        while True:
            # Fix this later
            # kitchen_print(f'Stove({self.id}) -> {in_progress}', color=COLORS.OKCYAN)

            while len(in_progress) < simultaneous_foods:
                try:
                    food = OrderList.stove_foods_to_prepare.get(timeout=0.01 * TIME_UNIT)
                    food['cooked_for'] = 0
                    in_progress.append(food)
                except queue.Empty:
                    break

            ready = []
            for i, food in enumerate(in_progress):
                time.sleep(TIME_UNIT)
                food['cooked_for'] += 1
                food_id = food['food_id']
                preparation_time = MENU[food_id]["preparation-time"]
                if food['cooked_for'] >= preparation_time:
                    ready.append(i)

            for ready_id in ready[::-1]:
                food = in_progress.pop(ready_id)
                # FIX THIS LATER
                food['cook_id'] = 777_777
                OrderList.give_prepared_food(food)
