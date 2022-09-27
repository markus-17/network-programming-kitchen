import time
import queue
import threading

from OrderList import OrderList
from settings import TIME_UNIT, MENU


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
