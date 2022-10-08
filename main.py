import threading
import itertools

from FlaskApp import flask_app
from CookThread import CookThread
from CookingApparatus import Stove, Oven
from settings import KITCHEN_PORT, COOKS_CONFIGURATIONS, NR_OF_STOVES, NR_OF_OVENS


cook_threads = []
stove_threads = []
oven_threads = []

if __name__ == '__main__':
    server_thread = threading.Thread(
        target=lambda: flask_app.run(
            host='0.0.0.0', port=KITCHEN_PORT, debug=False, use_reloader=False)
    )

    for stove_id in range(1, NR_OF_STOVES + 1):
        stove = Stove(stove_id)
        stove_threads.append(stove)

    for oven_id in range(1, NR_OF_OVENS + 1):
        oven = Oven(oven_id)
        oven_threads.append(oven)

    for cook_id, cook_configuration in COOKS_CONFIGURATIONS.items():
        for _ in range(cook_configuration["proficiency"]):
            cook_thread = CookThread(cook_id, cook_configuration['rank'])
            cook_threads.append(cook_thread)

    for thread in itertools.chain(stove_threads, oven_threads, [server_thread], cook_threads):
        thread.start()
