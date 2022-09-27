import threading
import itertools

from FlaskApp import flask_app
from CookThread import CookThread
from settings import KITCHEN_PORT, COOKS_CONFIGURATIONS


cook_threads = []

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
