import random

class Chromosome:
    def __init__(self, genes):
        self.genes = genes  # Representação da solução (ex: lista, array numpy)
        self.fitness = None  # Valor de aptidão (calculado posteriormente)

    def mutate(self, mutation_rate, mutation_strategy):
        """Aplica mutação aos genes com base em uma estratégia."""

        if random.random() < mutation_rate:
            r1,r2 = random.sample(range(len(self.genes)),2)
            if self.genes[r1] and self.genes[r2]:
                idx1 = random.randint(0, len(self.genes[r1])-1)
                idx2 = random.randint(0, len(self.genes[r2])-1)
                self.genes[r1][idx1], self.genes[r2][idx2] = self.genes[r2][idx2], self.genes[r1][idx1]
        return self

    @classmethod
    def crossover(cls, parent1, parent2, crossover_rate, crossover_method):
        """Realiza crossover entre dois pais para gerar filhos."""
        parent1, parent2 = parent1.genes, parent2.genes
        if random.random() < crossover_rate:
            # Exemplo: crossover em um ponto
            child1 = [resource.copy() for resource in parent1]
            child2 = [resource.copy() for resource in parent2]
            
            for i in range(len(child1)):
                if child1[i] and child2[i]:
                    point = random.randint(0, min(len(child1[i]), len(child2[i])))
                    child1[i][point:], child2[i][point:] = child2[i][point:], child1[i][point:]
            
            return Chromosome(child1), Chromosome(child2)
        return cls(parent1), cls(parent2)  # Sem crossover