import random

class Resource:

    def __init__(self, id):
        self.id = id

class Task:

    def __init__(self, id, duration, window, location, type):
        self.id = id
        self.duration = duration
        self.window = window
        self.location = location
        self.type = type

resources = [
    Resource(1),
    Resource(2),
    Resource(3),
    Resource(4),
]

preferences = [
    # Recurso 1
    {1: 300, 2: 250, 3: 400, 4: 500, 5: 450},
    # Recurso 2
    {1: 600, 2: 550, 3: 500, 4: 600, 5: 550},
    # Recurso 3
    {1: 400, 2: 400, 3: 300, 4: 700, 5: 800},
    # Recurso 4 - Preferível para tasks dos tipos 3 e 4 (custos menores nesses tipos)
    {1: 800, 2: 700, 3: 200, 4: 150, 5: 900}
]
tasks = [
    Task(1,30,(480,600),'A',5),
    Task(2,20,(540, 660), 'B',3),
    Task(3,40,(600,720), 'C', 2),
    Task(4,15, (480,720), 'D',2),
    Task(5,25,(600,780), 'C', 1),
    Task(6,20, (540,660),'B',4),
    Task(7,35,(480,660),'A',5),
    Task(8,10,(720,840), 'E',3),
    Task(9,50,(540,660),'F',1),
    Task(10,15,(660,780), 'G',4)
    # {'id': 'T1', 'duration': 30, 'window': (8,10), 'location': 'A', 'type': 5},
    # {'id': 'T2', 'duration': 20, 'window': (9,11), 'location': 'B', 'type': 3},
    # {'id': 'T3', 'duration': 40, 'window': (10,12), 'location': 'C', 'type': 2},
    # {'id': 'T4', 'duration': 15, 'window': (8,12), 'location': 'D', 'type': 2},
    # {'id': 'T5', 'duration': 25, 'window': (10,13), 'location': 'C', 'type': 1},
    # {'id': 'T6', 'duration': 20, 'window': (9,11), 'location': 'B', 'type': 4},
    # {'id': 'T7', 'duration': 35, 'window': (8,11), 'location': 'A', 'type': 5},
    # {'id': 'T8', 'duration': 10, 'window': (12,14), 'location': 'E', 'type': 3},
    # {'id': 'T9', 'duration': 50, 'window': (9,12), 'location': 'F', 'type': 1},
    # {'id': 'T10', 'duration': 15, 'window': (10,13), 'location': 'G' , 'type': 4}
]

# Matriz de distâncias mais complexa (inclui novos locais E, F, G)
distances = {
    'A': {'A':0, 'B':25, 'C':35, 'D':20, 'E':40, 'F':50, 'G':45},
    'B': {'A':25, 'B':0, 'C':15, 'D':30, 'E':35, 'F':45, 'G':30},
    'C': {'A':35, 'B':15, 'C':0, 'D':25, 'E':20, 'F':30, 'G':25},
    'D': {'A':20, 'B':30, 'C':25, 'D':0, 'E':15, 'F':25, 'G':20},
    'E': {'A':40, 'B':35, 'C':20, 'D':15, 'E':0, 'F':10, 'G':15},
    'F': {'A':50, 'B':45, 'C':30, 'D':25, 'E':10, 'F':0, 'G':20},
    'G': {'A':45, 'B':30, 'C':25, 'D':20, 'E':15, 'F':20, 'G':0},
}

