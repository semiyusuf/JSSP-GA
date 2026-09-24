# visualize.py
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def plot_gantt(instance, schedule, title="Gantt chart", save_path=None):
    fig, ax = plt.subplots(figsize=(10, 5))
    cmap = plt.get_cmap('tab20')
    for op in schedule:
        color = cmap(op.job % 20)
        ax.barh(op.machine, op.end - op.start, left=op.start, height=0.6,
                color=color, edgecolor='black')
        ax.text(op.start + (op.end - op.start) / 2, op.machine, f"J{op.job}",
                va='center', ha='center', fontsize=8, color='white')
    ax.set_xlabel("Time")
    ax.set_ylabel("Machine")
    ax.set_yticks(range(instance.n_machines))
    ax.set_title(title)
    handles = [mpatches.Patch(color=cmap(j % 20), label=f"Job {j}") for j in range(instance.n_jobs)]
    ax.legend(handles=handles, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=7)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.close(fig)


def plot_convergence(histories: dict, title="Convergence", save_path=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    for label, history in histories.items():
        ax.plot(range(len(history)), history, label=label)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best makespan so far")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.close(fig)