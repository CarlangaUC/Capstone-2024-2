UNIT_TIME = 1
WEATHER_FACT = 1
SECURITY_FACT = 1
REGULATIONS_FACT = 1


def costo_ruta(route):
    return (route.dist
            + WEATHER_FACT * route.weather
            + SECURITY_FACT * route.security
            + REGULATIONS_FACT * route.regulations)

def 