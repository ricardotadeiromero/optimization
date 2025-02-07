import random

class Population:
    def __init__(self, size, chromosome_class, gene_generator):
        self.chromosomes = [chromosome_class(gene_generator()) for _ in range(size)]
        self.chromosome_class = chromosome_class

    def evaluate_fitness(self, fitness_function):
        """Calcula a aptidão de todos os cromossomos."""
        for chromo in self.chromosomes:
            chromo.fitness = fitness_function(chromo.genes)

    def select_parents(self, selection_method="tournament", tournament_size=3):
        """Seleciona pais para reprodução."""
        if selection_method == "tournament":
            parents = []
            for _ in range(len(self.chromosomes)):
                tournament = random.sample(self.chromosomes, tournament_size)
                winner = min(tournament, key=lambda x: x.fitness)
                parents.append(winner)
            return parents
        # Outros métodos: roleta, ranking...

    def generate_next_generation(self, parents, crossover_rate, mutation_rate):
        """Gera a próxima geração via crossover e mutação."""
        next_gen = []
        for i in range(0, len(parents), 2):
            parent1, parent2 = parents[i], parents[i+1]
            child1, child2 = self.chromosome_class.crossover(parent1, parent2, crossover_rate, "single_point")
            child1.mutate(mutation_rate, "random")
            child2.mutate(mutation_rate, "random")
            next_gen.extend([child1, child2])
        self.chromosomes = next_gen