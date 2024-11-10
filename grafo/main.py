from collections import namedtuple
from clases.clases import Manager

Event = namedtuple("Event", ["final_port_id", "load"])

manager = Manager()
manager.add("ports.txt", "routes.txt", "ships.txt")
manager.processes([(0, [Event(1, 5), Event(2, 3)]),
                   (1, [Event(2, 2), Event(3, 3)]),
                   (2, [Event(0, 10)])])
manager.run(50)
