# experiment.py
import os
import statistics
import pandas as pd

from instance import parse_jssp_Dfile
from geneticAlgorithm import run_ga

INSTANCE_FILES = {
    "small":  ["la01", "la02"],
    "medium": ["la16", "la17"],
    "large":  ["la31", "la32"],
}

PARAMETER_SETS = {
    "A_light":  dict(pop_size=50,  n_generations=100, crossover_prob=0.7, mutation_prob=0.05),
    "B_medium": dict(pop_size=100, n_generations=200, crossover_prob=0.8, mutation_prob=0.10),
    "C_heavy":  dict(pop_size=150, n_generations=300, crossover_prob=0.9, mutation_prob=0.15),
}

N_RUNS = 10  # 10-30 required; 10 is a defensible choice under time pressure -- say so in your report


def run_experiments(data_dir="data"):
    rows = []
    for category, names in INSTANCE_FILES.items():
        for name in names:
            #instance = parse_jssp_Dfile(f"{data_dir}/{name}.txt")

            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "..", "data", f"{name}.txt")
            instance = parse_jssp_Dfile(file_path)

            for param_label, params in PARAMETER_SETS.items():
                makespans, exec_times, convergences = [], [], []

                for run_idx in range(N_RUNS):
                    result = run_ga(instance, seed=run_idx, **params)
                    makespans.append(result["best_makespan"])
                    exec_times.append(result["execution_time"])
                    convergences.append(result["convergence_generation"])

                rows.append({
                    "category": category, "instance": name, "parameter_set": param_label,
                    "best": min(makespans), "worst": max(makespans),
                    "mean": statistics.mean(makespans),
                    "std_dev": statistics.pstdev(makespans) if len(makespans) > 1 else 0.0,
                    "avg_execution_time_s": statistics.mean(exec_times),
                    "avg_convergence_generation": statistics.mean(convergences),
                    "n_runs": N_RUNS,
                })
                print(f"{category}/{name} [{param_label}]: best={min(makespans)}, "
                      f"mean={statistics.mean(makespans):.1f}")

    df = pd.DataFrame(rows)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    df.to_csv(os.path.join(results_dir, "experiment_results.csv"), index=False)
    return df


if __name__ == "__main__":
    run_experiments()