JOB SHOP SCHEDULE PROBLEM - SOLVED USING GA WITH SCHEDULE BUILDING ALGORITHM 

# JSSP-GA

A genetic algorithm for the Job Shop Scheduling Problem (JSSP), using an operation-based
chromosome encoding and a semi-active schedule-building algorithm (SBA) to decode each
chromosome into a feasible schedule.

#Group No: Group 4
#Course: ACIT4610

## Overview

- **Chromosome representation** — a flat list of job IDs whose length equals the instance's
  total number of operations; each job ID appears once per operation it has.
  `source/instance.py`, `source/chromosome.py`
- **SBA decoder** — walks the chromosome once, tracking `job_ready` (per job) and
  `machine_free` (per machine), scheduling each operation at
  `max(job_ready[job], machine_free[machine])`. `source/sba.py` (`decode_semi_active`)
- **GA operators** — k-way tournament selection, an Order-Crossover variant adapted for
  repeated job labels, and inversion mutation. `source/operators.py`
- **GA loop** — population init, elitism, selection/crossover/mutation, fixed-generation
  termination. `source/geneticAlgorithm.py` (`run_ga`)
- **Experiment runner** — runs the GA across all benchmark instances and parameter sets,
  writes `results/experiment_results.csv`. `source/experiments.py`
- **Plotting** — Gantt charts and convergence curves. `source/make_plots.py`,
  `source/visualize.py`
- **Analysis** — computes optimality gap against known-optimal makespans and produces
  summary tables by category/parameter set. `source/analysis.py`

## Project structure

```
JSSP-GA/
├── data/                         # benchmark instance files — SEE WARNING BELOW
│   ├── la01.txt   ├── la02.txt
│   ├── la16.txt   ├── la17.txt
│   └── la31.txt   ├── la32.txt
├── results/
│   ├── experiment_results.csv
│   ├── gantt_<instance>.png
│   ├── convergence_<instance>.png
│   └── summary_by_*.csv          # produced by analysis.py
├── source/
│   ├── instance.py                # JSSPInstance class + file parsing
│   ├── chromosome.py               # population init, validity check
│   ├── operators.py                # selection, crossover, mutation
│   ├── sba.py                      # semi-active decoder
│   ├── geneticAlgorithm.py         # main GA loop (run_ga)
│   ├── experiments.py              # runs all experiments, writes CSV
│   ├── make_plots.py               # generates Gantt + convergence figures
│   ├── visualize.py                # plotting helpers used by make_plots.py
│   ├── analysis.py                 # optimality-gap and summary tables
│   └── testChromosomeOperator.py   # quick end-to-end sanity check
├── requirements.in
├── requirements.txt
└── README.md
```

## ⚠ Before you submit: `data/` is not in this repository

`.gitignore` currently excludes the entire `data/` folder, so the six instance files the
scripts depend on (`la01.txt`, `la02.txt`, `la16.txt`, `la17.txt`, `la31.txt`, `la32.txt`)
were never pushed. As it stands, a fresh clone of this repo cannot run anything — every
script below will fail with `FileNotFoundError`, which conflicts with the assignment's
"must be executable" requirement.

**Fix, from the project root:**
```bash
# remove the "data/" line from .gitignore, then:
git add data/ .gitignore
git commit -m "Include benchmark instance data required to run the project"
git push
```

## Requirements

- Python 3.11+
- pandas, numpy, matplotlib, pytest (see `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/semiyusuf/JSSP-GA.git
   cd JSSP-GA
   ```

2. Create and activate a virtual environment:

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **macOS / Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Running on the example data

All commands are run from the project root, with the virtual environment activated.

**1. Quick sanity check** — confirms parsing, population initialization, crossover, and
mutation all produce valid chromosomes, and runs one short GA pass end-to-end:
```bash
python source/testChromosomeOperator.py
```

**2. Run the full experiment batch** — evaluates 3 categories × 3 parameter sets × 10 runs
each (this takes several minutes, mainly due to the `large` category and the `C_heavy`
parameter set):
```bash
python source/experiments.py
```
Prints best/mean makespan per instance and parameter set to the console, and writes the
full results table to `results/experiment_results.csv`.

**3. Generate Gantt charts and convergence plots** for all six instances:
```bash
python source/make_plots.py
```
Writes `results/gantt_<instance>.png` (best schedule found using the `C_heavy` parameter
set) and `results/convergence_<instance>.png` (best-so-far makespan per generation, all
three parameter sets overlaid) for each instance.

**4. Analyze results** — computes the optimality gap against known-optimal makespans and
summarizes by category and by parameter set (requires step 2 to have run first):
```bash
python source/analysis.py
```
Writes `summary_by_category.csv`, `summary_by_parameter_set.csv`, and
`summary_by_category_and_paramset.csv` to `results/`.

## Parameter sets

| Set | Population | Generations | Crossover prob. | Mutation prob. |
|---|---|---|---|---|
| A_light | 50 | 100 | 0.7 | 0.05 |
| B_medium | 100 | 200 | 0.8 | 0.10 |
| C_heavy | 150 | 300 | 0.9 | 0.15 |

Each combination is run 10 times (different random seeds) per instance.

## Test instances

| Category | Instances |
|---|---|
| Small | la01, la02 |
| Medium | la16, la17 |
| Large | la31, la32 |

## Limitations

This implementation uses a semi-active schedule builder: each operation is appended after
its machine's currently-last-scheduled operation, without searching for earlier idle gaps.
Active and Giffler-Thompson builders, which backfill such gaps and can produce shorter
makespans, were considered during design but not implemented given the project's time
constraints.