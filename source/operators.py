# operators.py
import random


def tournament_selection(population, fitnesses, k: int, rng: random.Random):
    """k-way tournament; lower fitness wins (we're minimizing makespan)."""
    contender_idx = rng.sample(range(len(population)), k)
    best_idx = min(contender_idx, key=lambda i: fitnesses[i])
    return population[best_idx]


def order_crossover(parent1: list[int], parent2: list[int], n_jobs: int, rng: random.Random) -> list[int]:
    """
    OX adapted for repeated genes: partition by JOB LABEL, not position.
    A random subset of job labels is inherited from parent1 at their original
    positions; every other position is filled by scanning parent2 left to
    right for occurrences of the remaining job labels. Both parents' full
    job-count multiset is respected automatically -- no repair step needed.
    """
    subset_size = rng.randint(1, max(1, n_jobs - 1))
    subset = set(rng.sample(range(n_jobs), subset_size))

    child = [None] * len(parent1)
    for i, gene in enumerate(parent1):
        if gene in subset:
            child[i] = gene

    fill_values = iter(gene for gene in parent2 if gene not in subset)
    for i in range(len(child)):
        if child[i] is None:
            child[i] = next(fill_values)

    return child


def inversion_mutation(chromosome: list[int], rng: random.Random) -> list[int]:
    """Reverses a random sub-segment. Reorders only -- can never break job counts."""
    child = chromosome.copy()
    i, j = sorted(rng.sample(range(len(child)), 2))
    child[i:j + 1] = reversed(child[i:j + 1])
    return child