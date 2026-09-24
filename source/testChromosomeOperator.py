import os
import random

from instance import parse_jssp_Dfile
from chromosome import init_population, is_valid_chromosome
from operators import order_crossover, inversion_mutation

#FIle imports
from sba import decode_semi_active
from geneticAlgorithm import run_ga

rng = random.Random(0)
#instance = parse_jssp_Dfile("data/la01.txt")
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "..", "data", "la01.txt")

instance = parse_jssp_Dfile(file_path)
pop = init_population(instance, pop_size=20, rng=rng)
assert all(is_valid_chromosome(c, instance) for c in pop), "invalid chromosome in initial population!"

c1 = order_crossover(pop[0], pop[1], instance.n_jobs, rng)
assert is_valid_chromosome(c1, instance), "OX broke validity!"

c2 = inversion_mutation(pop[0], rng)
assert is_valid_chromosome(c2, instance), "mutation broke validity!"
print("All valid.")
#print(f"Population: {pop} \n")


# Hand-worked check: 2 jobs, 2 machines. Job 0: (M0,3)->(M1,2). Job 1: (M1,2)->(M0,4).
# We calculated this by hand earlier in this project -- expected makespan = 7.
"""class ToyInstance:
    n_jobs = 2
    n_machines = 2
    jobs = [
        [(0, 3), (1, 2)],   # job 0
        [(1, 2), (0, 4)],   # job 1
    ]

toy_chrom = [1, 0, 0, 1]
_, toy_makespan = decode_semi_active(ToyInstance(), toy_chrom)
assert toy_makespan == 7, f"Expected 7, got {toy_makespan}"
print("Toy example PASS, makespan =", toy_makespan)

# Real instance: just confirm it runs and returns a plausible number
_, real_makespan = decode_semi_active(instance, pop[0])
print(f"la01 random chromosome makespan: {real_makespan}")"""

instance = parse_jssp_Dfile(file_path)  # adjust path as needed
result = run_ga(instance, pop_size=10, n_generations=20,
                 crossover_prob=0.8, mutation_prob=0.1, seed=0)

print(f"Best makespan: {result['best_makespan']}")
print(f"Converged at generation: {result['convergence_generation']}")
print(f"Execution time: {result['execution_time']:.3f}s")
print(f"History (first 5, last 5): {result['history'][:5]} ... {result['history'][-5:]}")