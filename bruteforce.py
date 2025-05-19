import time
from multiprocessing import Pool, cpu_count
from pysat.formula import CNF

def bits_from_int(value, length):
    return [(value >> i) & 1 == 1 for i in range(length)]

def check_assignment(clauses, assignment):
    for clause in clauses:
        satisfied = False
        for lit in clause:
            var = abs(lit)
            val = assignment.get(var, False)
            if (lit > 0 and val) or (lit < 0 and not val):
                satisfied = True
                break
        if not satisfied:
            return False
    return True

def brute_force_worker(args):
    start, end, variables, clauses, cells, grid, rows, cols, timeout = args
    t0 = time.perf_counter()
    length = len(variables)

    for value in range(start, end):
        if time.perf_counter() - t0 > timeout:
            return None
        bits = bits_from_int(value, length)
        assignment = {variables[i]: bits[i] for i in range(length)}
        if check_assignment(clauses, assignment):
            result = []
            for i in range(rows):
                row_res = []
                for j in range(cols):
                    cell = grid[i][j]
                    if isinstance(cell, int):
                        row_res.append(cell)
                    else:
                        v = i * cols + j + 1
                        if v in assignment:
                            row_res.append('T' if assignment[v] else 'G')
                        else:
                            row_res.append('T')
                result.append(row_res)
            return result
    return None

def brute_force_parallel(grid, cnf, timeout=150):
    rows, cols = len(grid), len(grid[0])

    vars_in_cnf = set(abs(lit) for clause in cnf.clauses for lit in clause)

    variable_map = {}
    for i in range(rows):
        for j in range(cols):
            if not isinstance(grid[i][j], int):
                v = i * cols + j + 1
                if v in vars_in_cnf:
                    variable_map[(i, j)] = v

    variables = list(variable_map.values())
    cells = list(variable_map.keys())
    total = 1 << len(variables)

    num_cpus = cpu_count()
    num_chunks = min(num_cpus, max(1, total // 10000))
    chunk_size = total // num_chunks

    args_list = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_chunks - 1 else total
        args_list.append((start, end, variables, cnf.clauses, cells, grid, rows, cols, timeout))

    with Pool(num_chunks) as pool:
        results = pool.map(brute_force_worker, args_list)

    return next((res for res in results if res is not None), None)
