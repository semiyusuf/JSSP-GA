# ga.py
import time
import random

from chromosome import init_population
from operators import tournament_selection, order_crossover, inversion_mutation
from sba import decode_semi_active


def evaluate_population(instance, population):
    """Decode every chromosome, return list of makespans (lower = better)."""
    return [decode_semi_active(instance, chrom)[1] for chrom in population]


def run_ga(instance, pop_size, n_generations, crossover_prob, mutation_prob,
           tournament_k=3, elitism_count=1, seed=None):
    """
    Runs one complete GA optimization on the given instance.
    Returns a dict with the best makespan found, the chromosome that
    produced it, the generation at which it last improved (convergence),
    execution time, and the full best-so-far-per-generation history
    (needed later for the convergence plot).
    """
    start_time = time.time()
    rng = random.Random(seed)

    population = init_population(instance, pop_size, rng)
    fitnesses = evaluate_population(instance, population)

    best_fitness = min(fitnesses)
    best_chromosome = population[fitnesses.index(best_fitness)]
    convergence_generation = 0
    history = [best_fitness]

    for gen in range(1, n_generations + 1):
        # Elitism: carry the current best individual(s) forward unchanged.
        elite_idx = sorted(range(len(population)), key=lambda i: fitnesses[i])[:elitism_count]
        elites = [population[i] for i in elite_idx]

        offspring = []
        while len(offspring) < pop_size - elitism_count:
            parent1 = tournament_selection(population, fitnesses, tournament_k, rng)
            parent2 = tournament_selection(population, fitnesses, tournament_k, rng)

            if rng.random() < crossover_prob:
                child = order_crossover(parent1, parent2, instance.n_jobs, rng)
            else:
                child = parent1.copy()

            if rng.random() < mutation_prob:
                child = inversion_mutation(child, rng)

            offspring.append(child)

        population = elites + offspring
        fitnesses = evaluate_population(instance, population)

        gen_best = min(fitnesses)
        if gen_best < best_fitness:
            best_fitness = gen_best
            best_chromosome = population[fitnesses.index(gen_best)]
            convergence_generation = gen

        history.append(best_fitness)

    return {
        "best_makespan": best_fitness,
        "best_chromosome": best_chromosome,
        "convergence_generation": convergence_generation,
        "execution_time": time.time() - start_time,
        "history": history,
    }