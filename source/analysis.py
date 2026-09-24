# analysis.py
import os
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(script_dir, "..", "results")

# JSPLib my known-optimal makespans for the six instances
KNOWN_OPTIMA = {
    "la01": 666, "la02": 655,
    "la16": 945, "la17": 784,
    "la31": 1784, "la32": 1850,
}


def load_results(csv_path=None):
    if csv_path is None:
        csv_path = os.path.join(results_dir, "experiment_results.csv")
    df = pd.read_csv(csv_path)
    df["optimum"] = df["instance"].map(KNOWN_OPTIMA)
    df["gap_pct"] = (df["best"] - df["optimum"]) / df["optimum"] * 100
    return df


def compare_by_category(df):
    return df.groupby("category").agg(
        mean_best=("best", "mean"),
        mean_worst=("worst", "mean"),
        mean_of_means=("mean", "mean"),
        mean_std_dev=("std_dev", "mean"),
        mean_gap_pct=("gap_pct", "mean"),
        mean_exec_time_s=("avg_execution_time_s", "mean"),
        mean_convergence_gen=("avg_convergence_generation", "mean"),
    ).reset_index()


def compare_by_parameter_set(df):
    return df.groupby("parameter_set").agg(
        mean_best=("best", "mean"),
        mean_of_means=("mean", "mean"),
        mean_std_dev=("std_dev", "mean"),
        mean_gap_pct=("gap_pct", "mean"),
        mean_exec_time_s=("avg_execution_time_s", "mean"),
        mean_convergence_gen=("avg_convergence_generation", "mean"),
    ).reset_index()


def compare_by_category_and_parameter_set(df):
    return df.groupby(["category", "parameter_set"]).agg(
        mean_best=("best", "mean"),
        mean_gap_pct=("gap_pct", "mean"),
        mean_exec_time_s=("avg_execution_time_s", "mean"),
    ).reset_index()


if __name__ == "__main__":
    df = load_results()

    print("=== Full results with optimality gap ===")
    cols = ["category", "instance", "parameter_set", "best", "worst", "mean",
            "std_dev", "gap_pct", "avg_execution_time_s", "avg_convergence_generation"]
    print(df[cols].to_string(index=False))

    print("\n=== By category (small vs medium vs large) ===")
    cat_summary = compare_by_category(df)
    print(cat_summary.to_string(index=False))
    cat_summary.to_csv(os.path.join(results_dir, "summary_by_category.csv"), index=False)

    print("\n=== By parameter set (A vs B vs C) ===")
    param_summary = compare_by_parameter_set(df)
    print(param_summary.to_string(index=False))
    param_summary.to_csv(os.path.join(results_dir, "summary_by_parameter_set.csv"), index=False)

    print("\n=== Category x parameter set ===")
    combo = compare_by_category_and_parameter_set(df)
    print(combo.to_string(index=False))
    combo.to_csv(os.path.join(results_dir, "summary_by_category_and_paramset.csv"), index=False)