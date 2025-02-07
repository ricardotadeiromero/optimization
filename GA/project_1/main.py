from data import *
import random
from config import GAConfig
from ga import GeneticAlgorithm
from chromosome import Chromosome
from fitness import FitnessEvaluator

config = GAConfig(population_size=50)

def gene_generator():
    shuffled_tasks = tasks.copy()
    allocation = [[] for _ in resources]
    random.shuffle(shuffled_tasks)
    while shuffled_tasks:
        resource_idx = random.randint(0, len(resources)-1)
        task = shuffled_tasks.pop()
        allocation[resource_idx].append(task)
    return allocation

# Instanciação do GA
ga = GeneticAlgorithm(
    population_size=config.population_size,
    chromosome_class=Chromosome,
    gene_generator=gene_generator,
    fitness_function=FitnessEvaluator.evaluate,
    crossover_rate=config.crossover_rate,
    mutation_rate=config.mutation_rate,
    max_generations=config.max_generations
)

# Execução
best_solution, fitness_history = ga.run()
print(f"Fitness: {best_solution.fitness}")
for idx, resource in enumerate(best_solution.genes):
    print(f"Recurso {idx+1}")
    print("------------------")
    for task in resource:
        print(f"Tarefa {task.id}")

print(f"Fitness histórico: {fitness_history}")