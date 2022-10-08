import time
import queue
import threading

from OrderList import OrderList
from settings import TIME_UNIT, MENU, kitchen_print


class CookThread(threading.Thread):
    def __init__(self, cook_id, rank, *args, **kwargs):
        super(CookThread, self).__init__(*args, **kwargs)
        self.cook_id = cook_id
        self.rank = rank

    def run(self):
        in_progress = []
        simultaneous_foods = 2
        while True:
            # # Fix this later
            # kitchen_print(f'Cook({self.cook_id}) -> {in_progress}')

            while len(in_progress) < simultaneous_foods:
                try:
                    food = OrderList.foods_to_prepare[self.rank].get(timeout=0.01*TIME_UNIT)
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
                food["cook_id"] = self.cook_id
                OrderList.give_prepared_food(food)

    #         # Work with Regular Orders
    #         for complexity in range(self.rank, 0, -1):
    #             try:
    #                 food = OrderList.foods_to_prepare[complexity].get(timeout=0.01*TIME_UNIT)
    #                 self.prepare_food(food)
    #                 break
    #             except queue.Empty:
    #                 pass

    # def prepare_food(self, food):
    #     food_id = food['food_id']
    #     preparation_time = MENU[food_id]['preparation-time'] * TIME_UNIT
    #     time.sleep(preparation_time)
    #     food["cook_id"] = self.cook_id
    #     OrderList.give_prepared_food(food)
