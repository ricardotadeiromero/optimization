from data import *
from typing import List

class FitnessEvaluator:
    @staticmethod
    def evaluate(chromosome_genes: List[List[Task]]):
        penalty = 0
        total_time = 0
        
        for resource in chromosome_genes:
            curr_time = 0
            prev_loc = None
            for task in resource:
                start, end = task.window
                # Verifique se 'distances' está definido e prev_loc é válido
                travel_time = distances.get(prev_loc, {}).get(task.location, 0) if prev_loc else 0
                arrival_time = curr_time + travel_time
                
                # Penalidades
                if arrival_time > end:
                    penalty += 1000
                elif arrival_time > start + task.duration:
                    penalty += 500
                
                # Atualiza o tempo atual
                curr_time = max(start, arrival_time) + task.duration
                prev_loc = task.location
            
            total_time = max(total_time, curr_time)
        
        return total_time + penalty  # Garanta que isso é numérico!