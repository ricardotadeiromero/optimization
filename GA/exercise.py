import random
from deap import base, creator, tools

resources = [
    {'id': 'R1'},
    {'id': 'R2'},
    {'id': 'R3'},
]

tasks = [
    {'id': 'T1', 'duration': 30, 'window': (8,10), 'location': 'A'},
    {'id': 'T2', 'duration': 20, 'window': (9,11), 'location': 'B'},
    {'id': 'T3', 'duration': 40, 'window': (10,12), 'location': 'C'},
    {'id': 'T4', 'duration': 15, 'window': (8,12), 'location': 'D'},
    {'id': 'T5', 'duration': 20, 'window': (10,13), 'location': 'C'},
    {'id': 'T6', 'duration': 20, 'window': (9,11), 'location': 'B'}
]

distances = {
    'A': {'A': 0, 'B': 25, 'C': 35, 'D': 20},
    'B': {'A': 25,'B': 0, 'C': 15, 'D': 30},
    'C': {'A': 35, 'B': 15,'C': 0, 'D': 25},
    'D': {'A': 20, 'B': 30, 'C': 25, 'D': 0}
}

# Correção na função de crossover
def crossover(parent1, parent2):
    # Cria cópias dos pais como indivíduos DEAP
    child1 = [resource.copy() for resource in parent1]
    child2 = [resource.copy() for resource in parent2]
    
    for i in range(len(child1)):
        if child1[i] and child2[i]:
            point = random.randint(0, min(len(child1[i]), len(child2[i])))
            child1[i][point:], child2[i][point:] = child2[i][point:], child1[i][point:]
    
    return creator.Individual(child1), creator.Individual(child2)  # Convertemos para Individual

# Correção na função de mutação
def mutation(individual):
    r1, r2 = random.sample(range(len(individual)), 2)
    if individual[r1] and individual[r2]:
        idx1 = random.randint(0, len(individual[r1])-1)
        idx2 = random.randint(0, len(individual[r2])-1)
        individual[r1][idx1], individual[r2][idx2] = individual[r2][idx2], individual[r1][idx1]
    return creator.Individual(individual),  # Retorna um indivíduo DEAP

# Correção na geração da população
def generate():
    all_tasks = tasks.copy()
    individual = [[] for _ in resources]
    
    while all_tasks:
        task = all_tasks.pop(random.randint(0, len(all_tasks)-1))
        resource_idx = random.randint(0, len(resources)-1)
        individual[resource_idx].append(task)
    
    return creator.Individual(individual)  # Garante que retorna um Individual

def fitnessFunction(individual):
    penality = 0
    totalTime = 0
    prevTasks = []
    for resource in individual:
        currTime = 0
        prevLoc = None
        
        for task in resource:
            start, end = task['window']
            duration = task['duration']
            local = task['location']
            if prevLoc:
                travelTime = distances[prevLoc][local]
            else:
                travelTime = 0
            
            arrivalTime = travelTime + currTime
            if arrivalTime > end:
                penality += 1000
            if task in prevTasks:
                penality += 1000
            startTime = max(arrivalTime, start)
            currTime = startTime + duration
            prevTasks.append(task)
        totalTime = max(totalTime, currTime)
    return (totalTime+penality,)


# Configuração do DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, generate)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", fitnessFunction)
toolbox.register("mate", crossover)
toolbox.register("mutate", mutation)
toolbox.register("select", tools.selTournament, tournsize=3)

# Parâmetros do algoritmo
populacao = toolbox.population(n=50)
prob_crossover = 0.7
prob_mutacao = 0.2
num_geracoes = 100

# Execução
for geracao in range(num_geracoes):
    # Avalia a população
    fitnesses = list(map(toolbox.evaluate, populacao))
    for ind, fit in zip(populacao, fitnesses):
        ind.fitness.values = fit
    
    # Seleciona os melhores
    selecionados = toolbox.select(populacao, len(populacao))
    
    # Aplica crossover e mutação
    filhos = []
    for i in range(0, len(selecionados), 2):
        pai1, pai2 = selecionados[i], selecionados[i+1]
        if random.random() < prob_crossover:
            filho1, filho2 = toolbox.mate(pai1, pai2)
            filhos.extend([filho1, filho2])
        else:
            filhos.extend([pai1, pai2])
    
    # Aplica mutação
    for filho in filhos:
        if random.random() < prob_mutacao:
            toolbox.mutate(filho)
    
    # Atualiza a população
    populacao = filhos

# Melhor indivíduo
melhor = tools.selBest(populacao, k=1)[0]
print(f"Melhor solução: {melhor}")
print(f"Tempo total: {melhor.fitness.values[0]}")