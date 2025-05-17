from itertools import combinations
from pysat.formula import CNF
from pysat.solvers import Minisat22  

def varnum(i, j, cols):
    return i * cols + j + 1

def neighbors(i, j, rows, cols):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            ni, nj = i + dx, j + dy
            if 0 <= ni < rows and 0 <= nj < cols:
                yield (ni, nj)

def gen_cnf_from_grid(grid):
    rows, cols = len(grid), len(grid[0])
    clause_set = set()

    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            if isinstance(cell, int):
                neigh = list(neighbors(i, j, rows, cols))
                vars_ = [varnum(x, y, cols) for (x, y) in neigh]

                for combo in combinations(vars_, len(vars_) - cell + 1):
                    clause = tuple(sorted(combo))
                    clause_set.add(clause)

                for combo in combinations(vars_, cell + 1):
                    clause = tuple(sorted([-v for v in combo]))
                    clause_set.add(clause)

    cnf = CNF()
    for clause in clause_set:
        cnf.append(list(clause))
    return cnf

def solve_with_pysat(grid):
    rows, cols = len(grid), len(grid[0])
    cnf = gen_cnf_from_grid(grid)
    
    solver = Minisat22()
    solver.append_formula(cnf.clauses)

    if solver.solve():
        model = solver.get_model()
        model_set = set(model)  

        result = [[cell if isinstance(cell, int) else '' for cell in row] for row in grid]

        unknowns = [(i, j) for i in range(rows) for j in range(cols) if not isinstance(grid[i][j], int)]
        var_map = { (i,j): varnum(i,j,cols) for (i,j) in unknowns }

        for (i, j) in unknowns:
            v = var_map[(i,j)]
            result[i][j] = 'T' if v in model_set else 'G'

        solver.delete()
        return result
    else:
        solver.delete()
        return None
