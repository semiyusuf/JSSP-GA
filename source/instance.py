import os

class JSSPInstance:
    def __init__(self, name: str, n_jobs: int, n_machines: int, jobs: list[list[tuple[int, int]]]):
        self.name = name
        self.n_jobs = n_jobs
        self.n_machines = n_machines
        self.jobs = jobs

    @property #Makes it so that method caan be called without paratheses, like an attribute
    def n_operations(self):
        return sum(len(job) for job in self.jobs)
    #Method for representing the JSSPInstance object as a string
    def __repr__(self):
        return f"JSSPInstance(name={self.name!r}, n_jobs={self.n_jobs}, n_machines={self.n_machines}, jobs={self.jobs})"
    






# Function for parsing my datailes
def parse_jssp_Dfile(file_path):
    name = os.path.splitext(os.path.basename(file_path))[0]
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
    return JSSPInstance(name=name, n_jobs=n_jobs, n_machines=n_machines, jobs=jobs)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "..", "data", "la01.txt")
    print(f"Script directory: {script_dir}"
          f"File path: {file_path}")
    result = parse_jssp_Dfile(file_path)
    print(result)
    print(result.n_operations)

    instance = parse_jssp_Dfile(file_path)

    assert instance.n_jobs == 10, f"Expected 10 jobs, got {instance.n_jobs}"
    assert instance.n_machines == 5, f"Expected 5 machines, got {instance.n_machines}"
    assert len(instance.jobs) == 10, f"Expected 10 job entries, got {len(instance.jobs)}"
    assert instance.n_operations == 50, f"Expected 50 operations, got {instance.n_operations}"

"""result = parse_jssp_Dfile(file_path)
print(f"\n n_jobs: {result['n_jobs']}, n_machines: {result['n_machines']}")
print(f"Job 0 operations: {result['jobs'][0]}")

print(f"Total jobs parsed: {len(result['jobs'])}")
print(f"Job 0: {result['jobs'][0]}")
print(f"Job 1: {result['jobs'][1]}")
print(f"Job 8: {result['jobs'][8]}")
#print(f"Lines: {result['lines']}!")""" # old print statements for testing parsing


