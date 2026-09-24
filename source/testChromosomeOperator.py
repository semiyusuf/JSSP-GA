from instance import parse_jssp_Dfile
from chromosome import init_population, is_valid_chromosome
from operators import order_crossover, inversion_mutation
import random
import os

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
print(f"Population: {pop} \n")