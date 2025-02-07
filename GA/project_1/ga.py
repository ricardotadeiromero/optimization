from population import Population

class GeneticAlgorithm:
    def __init__(
        self,
        population_size,
        chromosome_class,
        gene_generator,
        fitness_function,
        crossover_rate=0.8,
        mutation_rate=0.1,
        max_generations=100
    ):
        self.population = Population(population_size, chromosome_class, gene_generator)
        self.fitness_function = fitness_function
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

    def run(self):
        """Executa o GA até atingir critérios de parada."""
        best_fitness_history = []
        for generation in range(self.max_generations):
            self.population.evaluate_fitness(self.fitness_function)
            parents = self.population.select_parents(selection_method="tournament")
            self.population.generate_next_generation(parents, self.crossover_rate, self.mutation_rate)
            best_chromo = max(self.population.chromosomes, key=lambda x: x.fitness)
            best_fitness_history.append(best_chromo.fitness)
            if self._convergence_criteria(best_fitness_history):
                break
        return best_chromo.genes, best_fitness_history

    def _convergence_criteria(self, history, window=10, threshold=0.01):
        """Verifica se a aptidão estagnou."""
        if len(history) < window:
            return False
        return (max(history[-window:]) - min(history[-window:])) < threshold