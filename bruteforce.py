from itertools import product

def solve_bruteforce(grid, cnf):
    rows, cols = len(grid), len(grid[0])

    vars_in_cnf = set(abs(lit) for clause in cnf.clauses for lit in clause)

    unknowns = []
    vars_used = []
    for i in range(rows):
        for j in range(cols):
            if not isinstance(grid[i][j], int):
                v = i * cols + j + 1
                if v in vars_in_cnf:
                    unknowns.append((i, j))
                    vars_used.append(v)

    var_to_idx = {var: idx for idx, var in enumerate(vars_used)}

    def clause_satisfied(clause, bits):
        satisfied = False
        for lit in clause:
            var = abs(lit)
            idx = var_to_idx.get(var, None)
            if idx is None:
                return True
            val = bits[idx]
            if (lit > 0 and val) or (lit < 0 and not val):
                satisfied = True
        return satisfied

    for bits in product([False, True], repeat=len(vars_used)):
        if all(clause_satisfied(clause, bits) for clause in cnf.clauses):
            result = []
            for i in range(rows):
                row_res = []
                for j in range(cols):
                    cell = grid[i][j]
                    if isinstance(cell, int):
                        row_res.append(cell)
                    else:
                        v = i * cols + j + 1
                        idx = var_to_idx.get(v, None)
                        if idx is not None:
                            val = bits[idx]
                            row_res.append('T' if val else 'G')
                        else:
                            row_res.append('T')
                result.append(row_res)
            return result
    return None
