import threading
import itertools

import requests

from FlaskApp import flask_app
from CookThread import CookThread
from CookThread import Oven, Stove
from settings import KITCHEN_HOSTNAME, KITCHEN_PORT, COOKS_CONFIGURATIONS, NR_OF_OVENS, NR_OF_STOVES, RESTAURANT_ID, RESTAURANT_NAME, DINING_HALL_HOSTNAME, KITCHEN_PORT, MENU, DINING_HALL_PORT


cook_threads = []
oven_threads = []
stove_threads = []

if __name__ == '__main__':
    _ = requests.post(
        url=f'http://food_ordering:8000/register',
        json={
            'restaurant_id': RESTAURANT_ID,
            'name': RESTAURANT_NAME,
            'address': f'http://{DINING_HALL_HOSTNAME}:{DINING_HALL_PORT}',
            'menu_items': len(MENU),
            'menu': MENU
        }
    )
    
    server_thread = threading.Thread(
        target=lambda: flask_app.run(
            host='0.0.0.0', port=KITCHEN_PORT, debug=False, use_reloader=False)
    )

    for _ in range(NR_OF_OVENS):
        oven_threads.append(Oven())

    for _ in range(NR_OF_STOVES):
        stove_threads.append(Stove())

    for cook_id, cook_configuration in COOKS_CONFIGURATIONS.items():
        for _ in range(cook_configuration["proficiency"]):
            cook_thread = CookThread(cook_id, cook_configuration['rank'])
            cook_threads.append(cook_thread)

    for thread in itertools.chain(oven_threads, stove_threads, [server_thread], cook_threads):
        thread.start()
