def read_input_file(path):
    grid = []
    with open(path) as f:
        for line in f:
            row = []
            for val in line.strip().split(','):
                val = val.strip()
                if val == '_':
                    row.append('')  
                elif val.isdigit():
                    row.append(int(val))
                elif val in ['T', 'G']:
                    row.append(val)
                else:
                    row.append('')  
            grid.append(row)
    return grid


def write_output_file(grid, path):
    with open(path, 'w') as f:
        for row in grid:
            line = ', '.join(str(cell) if cell != '' else '_' for cell in row)
            f.write(line + '\n')


def print_grid(grid):
    for row in grid:
        print(', '.join(str(cell) if cell != '' else '_' for cell in row))
