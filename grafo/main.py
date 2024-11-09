from clases.clases import Manager

manager = Manager()
manager.add("ports.txt", "routes.txt", "ships.txt")
manager.processes([0, 1, 2])
print(manager.matrix)
manager.run(15)
