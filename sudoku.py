import pprint

pp = pprint.PrettyPrinter(indent=4)
SUDOKU_SIZE = 9


def _get_row(puzzle, row):
    """Returns the non-zero numbers for the specified row."""
    return [num for num in puzzle[row] if num > 0]


def _get_column(puzzle, col):
    """Returns the non-zero numbers for the specified column."""
    return [puzzle[row][col] for row in range(SUDOKU_SIZE) if puzzle[row][col] > 0]


def _get_grid(puzzle, row, col):
    """Returns the non-zero numbers of the specificed grid."""
    assert 0 <= row <= 2
    assert 0 <= col <= 2

    row_offset = row * 3
    col_offset = col * 3
    return [
        puzzle[y][x]
        for y in range(row_offset, row_offset + 3)
        for x in range(col_offset, col_offset + 3)
        if puzzle[y][x] > 0
    ]


def _check(puzzle):
    """Iterates through the unresolved cells evaluating the possible candidate values."""
    cells = dict()
    for y in range(SUDOKU_SIZE):
        for x in range(SUDOKU_SIZE):
            if puzzle[y][x] == 0:
                candidates = set(range(1, SUDOKU_SIZE + 1))
                taken = set(
                    _get_row(puzzle, y)
                    + _get_column(puzzle, x)
                    + _get_grid(puzzle, y // 3, x // 3)
                )
                cells[(y, x)] = candidates.difference(taken)

    return cells


def solve_puzzle(puzzle, update=True):
    """Recursively fills in cells that have a single candidate value."""
    if not update:
        return puzzle

    update = False
    cells = _check(puzzle)
    for key, candidates in cells.items():
        if len(candidates) == 1:
            update = True
            y, x = key
            puzzle[y][x] = candidates.pop()

    return solve_puzzle(puzzle, update)
