import random

class Chromosome:
    def __init__(self, genes):
        self.genes = genes  # Representação da solução (ex: lista, array numpy)
        self.fitness = None  # Valor de aptidão (calculado posteriormente)

    def mutate(self, mutation_rate, mutation_method):
        """Aplica mutação trocando elementos aleatórios dentro dos genes."""
        if random.random() < mutation_rate:
            r1, r2 = random.sample(range(len(self.genes)), 2)  # Garantir que r1 != r2
            if self.genes[r1] and self.genes[r2]:
                idx1 = random.randint(0, len(self.genes[r1]) - 1)
                idx2 = random.randint(0, len(self.genes[r2]) - 1)
                if idx1 != idx2:  # Evita trocar o mesmo índice
                    self.genes[r1][idx1], self.genes[r2][idx2] = self.genes[r2][idx2], self.genes[r1][idx1]
        return self


    @classmethod
    def crossover(cls, parent1, parent2, crossover_rate, crossover_method):
        """Realiza crossover de um ponto, garantindo que os genes tenham tamanho adequado."""
        if random.random() < crossover_rate:
            child1, child2 = [], []

            for g1, g2 in zip(parent1.genes, parent2.genes):
                if g1 and g2:  # Evita listas vazias
                    point = random.randint(0, min(len(g1), len(g2)) - 1)  # Garante que haja troca real
                    new_g1 = g1[:point] + g2[point:]
                    new_g2 = g2[:point] + g1[point:]
                else:
                    new_g1, new_g2 = g1, g2  # Se vazios, mantém

                child1.append(new_g1)
                child2.append(new_g2)

            return cls(child1), cls(child2)
        
        return cls(parent1.genes), cls(parent2.genes)  # Sem crossover

    