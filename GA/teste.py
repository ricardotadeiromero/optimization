import random
from deap import base, creator, tools

# Dados de entrada (modificados para usar localizações corretas)
resources = [
    {'id': 'R1'},
    {'id': 'R2'},
]

tasks = [
    {'id': 'T1', 'duration': 30, 'window': (8, 10), 'location': 'A'},
    {'id': 'T2', 'duration': 20, 'window': (9, 11), 'location': 'B'},
    {'id': 'T3', 'duration': 40, 'window': (10, 12), 'location': 'C'},
    {'id': 'T4', 'duration': 15, 'window': (8, 12), 'location': 'D'}
]

distances = {
    'A': {'A': 0, 'B': 25, 'C': 35, 'D': 20},
    'B': {'A': 25, 'B': 0, 'C': 15, 'D': 30},
    'C': {'A': 35, 'B': 15, 'C': 0, 'D': 25},
    'D': {'A': 20, 'B': 30, 'C': 25, 'D': 0}
}

# --------------------------------------
# Correção 1: Função de crossover corrigida
# --------------------------------------
def crossover(parent1, parent2):
    child1 = [resource.copy() for resource in parent1]
    child2 = [resource.copy() for resource in parent2]
    
    for i in range(len(child1)):
        if child1[i] and child2[i]:
            point = random.randint(0, min(len(child1[i]), len(child2[i])))
            child1[i][point:], child2[i][point:] = child2[i][point:], child1[i][point:]
    
    return child1, child2

# --------------------------------------
# Correção 2: Função de mutação retorna indivíduo
# --------------------------------------
def mutation(individual):
    r1, r2 = random.sample(range(len(individual)), 2)
    if individual[r1] and individual[r2]:
        idx1 = random.randint(0, len(individual[r1])-1)
        idx2 = random.randint(0, len(individual[r2])-1)
        individual[r1][idx1], individual[r2][idx2] = individual[r2][idx2], individual[r1][idx1]
    return individual,

# --------------------------------------
# Correção 3: Geração de indivíduos com todas as tarefas alocadas
# --------------------------------------
def generate():
    all_tasks = tasks.copy()
    individual = [[] for _ in resources]
    
    # Distribui todas as tarefas aleatoriamente
    while all_tasks:
        task = all_tasks.pop(random.randint(0, len(all_tasks)-1))
        resource_idx = random.randint(0, len(resources)-1)
        individual[resource_idx].append(task)
    
    return creator.Individual(individual)

# --------------------------------------
# Correção 4: Função de fitness com cálculos corretos
# --------------------------------------
def fitnessFunction(individual):
    total_penalty = 0
    max_time = 0
    
    for resource in individual:
        current_time = 0
        prev_location = None
        prevTask = []
        for task in resource:
            start, end = task['window']
            duration = task['duration']
            location = task['location']
            
            # Calcula tempo de deslocamento
            if prev_location is not None:
                travel_time = distances[prev_location][location]
            else:
                travel_time = 0  # Primeira tarefa
            
            # Tempo de chegada
            arrival_time = current_time + travel_time
            
            # Verifica violação da janela de tempo
            if arrival_time > end:
                total_penalty += 1000  # Penalidade alta
            
            if task in prevTask:
                total_penalty += 1000
            # Tempo de início (considera janela)
            start_time = max(arrival_time, start)
            current_time = start_time + duration
            prev_location = location  # Atualiza localização
            prevTask.append(task)
        max_time = max(max_time, current_time)
    
    return (max_time + total_penalty,)

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
pop_size = 50
prob_crossover = 0.7
prob_mutacao = 0.2
num_geracoes = 100

# Execução
populacao = toolbox.population(n=pop_size)

for geracao in range(num_geracoes):
    # Avaliação
    fitnesses = list(map(toolbox.evaluate, populacao))
    for ind, fit in zip(populacao, fitnesses):
        ind.fitness.values = fit
    
    # Seleção
    selecionados = toolbox.select(populacao, len(populacao))
    
    # Crossover
    filhos = []
    for i in range(0, len(selecionados), 2):
        pai1, pai2 = selecionados[i], selecionados[i+1]
        if random.random() < prob_crossover:
            filho1, filho2 = toolbox.mate(pai1, pai2)
            filhos.append(filho1)
            filhos.append(filho2)
        else:
            filhos.append(pai1)
            filhos.append(pai2)
    
    # Mutação
    for filho in filhos:
        if random.random() < prob_mutacao:
            toolbox.mutate(filho)
    
    # Atualização da população
    populacao = filhos

# Resultado
melhor = tools.selBest(populacao, k=1)[0]
print("\nMelhor solução encontrada:")
for i, recurso in enumerate(melhor):
    print(f"Recurso {resources[i]['id']}:")
    for task in recurso:
        print(f"  → {task['id']} ({task['location']})")
print(f"\nTempo total: {melhor.fitness.values[0]} minutos")