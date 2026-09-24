# sba.py
from collections import namedtuple

ScheduledOp = namedtuple("ScheduledOp", ["job", "op_index", "machine", "start", "end"])


def decode_semi_active(instance, chromosome):
    
    next_op_index = [0] * instance.n_jobs
    job_ready = [0] * instance.n_jobs
    machine_free = [0] * instance.n_machines
    schedule = []

    for job in chromosome:
        op_idx = next_op_index[job]
        machine, duration = instance.jobs[job][op_idx]

        start = max(job_ready[job], machine_free[machine])
        end = start + duration

        schedule.append(ScheduledOp(job=job, op_index=op_idx, machine=machine,
                                     start=start, end=end))

        job_ready[job] = end
        machine_free[machine] = end
        next_op_index[job] += 1

    makespan = max(op.end for op in schedule)
    return schedule, makespan
