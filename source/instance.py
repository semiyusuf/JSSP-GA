import os

def parse_jssp_Dfile(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()] 

        #This is line one data being split into number of jabs and nuumber of machines
        n_jobs, n_machines = map(int, lines[0].split())

        jobs = []
        for job_index, line in enumerate(lines[1:n_jobs + 1]):
            numbers = list(map(int, line.split()))
        
            expected_count = 2* n_machines
            if len(numbers) != expected_count:
                raise ValueError(
                    f"Job {job_index} (line {job_index +2} in file):"
                    f"expected {expected_count} integers ({n_machines} machine/duration pairs)"
                    f"but found {len(numbers)}."
                )

            # operations[] pairs up (machine duration: integer in data file)
            operations = []
            for i in range(0, len(numbers), 2):
                machine = numbers[i]
                duration = numbers[i + 1]
                operations.append((machine, duration))

            jobs.append(operations)
    return {
        "n_jobs": n_jobs,
        "n_machines": n_machines,
        "jobs": jobs
    }

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "..", "data", "la01.txt")
print(f"Script directory: {script_dir}"
      f"File path: {file_path}")


result = parse_jssp_Dfile(file_path)
print(f"\n n_jobs: {result['n_jobs']}, n_machines: {result['n_machines']}")
print(f"Job 0 operations: {result['jobs'][0]}")

print(f"Total jobs parsed: {len(result['jobs'])}")
print(f"Job 0: {result['jobs'][0]}")
print(f"Job 1: {result['jobs'][1]}")
print(f"Job 8: {result['jobs'][8]}")
#print(f"Lines: {result['lines']}!")


