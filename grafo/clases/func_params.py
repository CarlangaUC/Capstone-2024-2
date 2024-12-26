import random

UNIT_TIME = 1
WEATHER_FACT = 1
SECURITY_FACT = 1
REGULATIONS_FACT = 1
FILE_NAME = "archivo.txt"


def recharge_dist(recharge):
    return int(random.randint(recharge, recharge + 10))


def speed_dist(speed):
    return speed


def costo_ruta(route):
    return (route.dist
            + WEATHER_FACT * route.weather
            + SECURITY_FACT * route.security
            + REGULATIONS_FACT * route.regulations)
