from solver_pysat import neighbors
from itertools import product

def is_safe(grid, assignment, i, j):
    if isinstance(grid[i][j], int):
        return True

    rows, cols = len(grid), len(grid[0])
    for x in range(rows):
        for y in range(cols):
            if isinstance(grid[x][y], int):
                count = 0
                unknown = 0
                for ni, nj in neighbors(x, y, rows, cols):
                    if assignment[ni][nj] == 'T':
                        count += 1
                    elif assignment[ni][nj] == '':
                        unknown += 1
                if count > grid[x][y] or count + unknown < grid[x][y]:
                    return False
    return True

def clause_satisfied(clause, assignment, rows, cols, var_to_pos):
    for lit in clause:
        var = abs(lit)
        pos = var_to_pos.get(var, None)
        if pos is None:
            return True

        i, j = pos
        val = assignment[i][j]
        if val == '':
            continue

        if (lit > 0 and val == 'T') or (lit < 0 and val != 'T'):
            return True
    return False

def is_cnf_satisfied(cnf, assignment, rows, cols, var_to_pos):
    for clause in cnf.clauses:
        if not clause_satisfied(clause, assignment, rows, cols, var_to_pos):
            return False
    return True

def backtrack(grid, assignment, empty_cells, idx, cnf, rows, cols, var_to_pos):
    if idx == len(empty_cells):
        if is_cnf_satisfied(cnf, assignment, rows, cols, var_to_pos):
            return assignment
        else:
            return None

    i, j = empty_cells[idx]
    for val in ['T', 'G']:
        assignment[i][j] = val
        if is_safe(grid, assignment, i, j):
            result = backtrack(grid, assignment, empty_cells, idx + 1, cnf, rows, cols, var_to_pos)
            if result:
                return result
        assignment[i][j] = ''

    return None

def solve_backtracking(grid, cnf):
    rows, cols = len(grid), len(grid[0])
    assignment = [[cell if isinstance(cell, int) else '' for cell in row] for row in grid]
    empty_cells = [(i, j) for i in range(rows) for j in range(cols) if not isinstance(grid[i][j], int)]

    var_to_pos = {}
    for i in range(rows):
        for j in range(cols):
            v = i * cols + j + 1
            var_to_pos[v] = (i, j)

    return backtrack(grid, assignment, empty_cells, 0, cnf, rows, cols, var_to_pos)
