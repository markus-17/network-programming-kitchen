import os


class COLORS:
    # https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'


RESTAURANT_ID = int(os.getenv('RESTAURANT_ID'))

DINING_HALL_HOSTNAME = f'dining_hall_{RESTAURANT_ID}' if os.getenv('USING_DOCKER_COMPOSE') == '1' else 'localhost'
KITCHEN_HOSTNAME = f'kitchen_{RESTAURANT_ID}'

TIME_UNIT = 1 # s
NR_OF_OVENS = 2
NR_OF_STOVES = 1

MENUS = {
    1: {
        1: {
            "id": 1,
            "name": "pizza",
            "preparation-time": 20,
            "complexity": 2,
            "cooking-apparatus": "oven"
        },
        2: {
            "id": 2,
            "name": "salad",
            "preparation-time": 10,
            "complexity": 1,
            "cooking-apparatus": None
        },
        3: {
            "id": 3,
            "name": "zeama",
            "preparation-time": 7,
            "complexity": 1,
            "cooking-apparatus": "stove"
        },
        4: {
            "id": 4,
            "name": "Lasagna",
            "preparation-time": 30,
            "complexity": 2,
            "cooking-apparatus": "oven"
        },
        5: {
            "id": 5,
            "name": "Burger",
            "preparation-time": 15,
            "complexity": 1,
            "cooking-apparatus": "stove"
        },
        6: {
            "id": 6,
            "name": "Gyros",
            "preparation-time": 15,
            "complexity": 1,
            "cooking-apparatus": None
        },
        7: {
            "id": 7,
            "name": "Kebab",
            "preparation-time": 15,
            "complexity": 1,
            "cooking-apparatus": None
        },
    },
    2: {
        1: {
            "id": 1,
            "name": "Island Duck with Mulberry Mustard",
            "preparation-time": 35,
            "complexity": 3,
            "cooking-apparatus": "oven"
        },
        2: {
            "id": 2,
            "name": "Scallop Sashimi with Meyer Lemon Confit",
            "preparation-time": 32,
            "complexity": 3,
            "cooking-apparatus": None
        }, 
        3: {
            "id": 3,
            "name": "Waffles",
            "preparation-time": 10,
            "complexity": 1,
            "cooking-apparatus": "stove"
        },
        4: {
            "id": 4,
            "name": "Aubergine",
            "preparation-time": 20,
            "complexity": 2,
            "cooking-apparatus": "oven"
        },
        5: {
            "id": 5,
            "name": "Tobacco Chicken",
            "preparation-time": 30,
            "complexity": 2,
            "cooking-apparatus": "oven"
        },
        6: {
            "id": 6,
            "name": "Unagi Maki",
            "preparation-time": 20,
            "complexity": 2,
            "cooking-apparatus": None
        },
    }
}

if RESTAURANT_ID == 1:
    MENU = MENUS[1]
    RESTAURANT_NAME = 'DonHector'
    KITCHEN_PORT = 3001
    DINING_HALL_PORT = 8081
elif RESTAURANT_ID == 2:
    MENU = MENUS[2]
    RESTAURANT_NAME = 'DonCarlo'
    KITCHEN_PORT = 3002
    DINING_HALL_PORT = 8082

COOKS_CONFIGURATIONS = {
    1: {
        "rank": 3,
        "proficiency": 4,
        "name": None,
        "catchphrase": None
    },
    2: {
        "rank": 2,
        "proficiency": 3,
        "name": None,
        "catchphrase": None
    },
    3: {
        "rank": 2,
        "proficiency": 2,
        "name": None,
        "catchphrase": None
    },
    4: {
        "rank": 1,
        "proficiency": 2,
        "name": None,
        "catchphrase": None
    }
}

def kitchen_print(msg, color=COLORS.OKGREEN):
    print(f'{color}|-- KITCHEN --->>> {msg}')
