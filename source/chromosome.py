# chromosome.py
import random


def random_chromosome(instance, rng: random.Random) -> list[int]:
    """One random, automatically-valid operation-based chromosome."""
    genes = []
    for job_id, operations in enumerate(instance.jobs):
        genes.extend([job_id] * len(operations))
    rng.shuffle(genes)
    return genes


def init_population(instance, pop_size: int, rng: random.Random) -> list[list[int]]:
    return [random_chromosome(instance, rng) for _ in range(pop_size)]


def is_valid_chromosome(chromosome: list[int], instance) -> bool:
    """Debug helper: confirms every job appears exactly as many times as it has operations."""
    for job_id, operations in enumerate(instance.jobs):
        if chromosome.count(job_id) != len(operations):
            return False
    return True