# make_plots.py
import os
from instance import parse_jssp_Dfile
from geneticAlgorithm import run_ga
from sba import decode_semi_active
from visualize import plot_gantt, plot_convergence

ALL_INSTANCES = {
    "small":  ["la01", "la02"],
    "medium": ["la16", "la17"],
    "large":  ["la31", "la32"],
}

PARAM_SETS = {
    "A_light":  dict(pop_size=50,  n_generations=100, crossover_prob=0.7, mutation_prob=0.05),
    "B_medium": dict(pop_size=100, n_generations=200, crossover_prob=0.8, mutation_prob=0.10),
    "C_heavy":  dict(pop_size=150, n_generations=300, crossover_prob=0.9, mutation_prob=0.15),
}

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "data")
results_dir = os.path.join(script_dir, "..", "results")
os.makedirs(results_dir, exist_ok=True)

for category, names in ALL_INSTANCES.items():
    for name in names:
        instance = parse_jssp_Dfile(os.path.join(data_dir, f"{name}.txt"))

        result = run_ga(instance, seed=0, **PARAM_SETS["C_heavy"])
        schedule, makespan = decode_semi_active(instance, result["best_chromosome"])
        plot_gantt(instance, schedule, title=f"{name} best schedule (Cmax={makespan})",
                   save_path=os.path.join(results_dir, f"gantt_{name}.png"))

        histories = {label: run_ga(instance, seed=0, **params)["history"]
                     for label, params in PARAM_SETS.items()}
        plot_convergence(histories, title=f"{name} convergence by parameter set",
                          save_path=os.path.join(results_dir, f"convergence_{name}.png"))
        print(f"Saved plots for {name}")