from dataclasses import dataclass

@dataclass
class GAConfig:
    population_size: int = 100
    crossover_rate: float = 0.8
    mutation_rate: float = 0.1
    max_generations: int = 200
    selection_method: str = "tournament"
