import PySimpleGUI as sg
from sudoku import solve_puzzle, SUDOKU_SIZE


sg.ChangeLookAndFeel("GreenTan")

stored_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

# Helper funcions


def get_value(row, col):
    contents = puzzle[row][col]
    return contents if contents else ""


def chunk(nums, n=9):
    return [nums[i : i + n] for i in range(0, len(nums), n)]


def convert(values):
    values = list(values)[1:]  # Ignore dictionary value for the menus
    return list(map(lambda x: 0 if x == "" else int(x), values))


def display(window, puzzle):
    """Displays the specified puzzle."""
    for row in range(SUDOKU_SIZE):
        for col in range(SUDOKU_SIZE):
            value = puzzle[row][col]
            window[(row, col)].update(value if value else "")


def clear_display(window):
    for row in range(9):
        for col in range(9):
            window[(row, col)].update("")


# Layout

menus = [[sg.Menu([["Game", ["Store", "Restore"]]])]]

input_rows = [
    [
        sg.InputText(
            key=(row, col),
            default_text="",
            size=(4, 1),
            pad=((7, 3) if col in (3, 6) else 3, (7, 3) if row in (3, 6) else 3),
        )
        for col in range(SUDOKU_SIZE)
    ]
    for row in range(SUDOKU_SIZE)
]

btn = [
    [
        sg.Button("Solve", pad=(3, 10)),
        sg.Button("Clear", pad=(3, 10)),
        sg.Button("Close", pad=((198, 3), 10)),
    ]
]

layout = menus + input_rows + btn

window = sg.Window("Sudoku Solver", layout, font="Courier 12")

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Close" or event == "Exit":
        break

    if event == "Clear":
        clear_display(window)

    if event == "Solve":
        puzzle = convert(values.values())
        puzzle = chunk(puzzle)
        solution = solve_puzzle(puzzle)
        display(window, solution)

    if event == "Store":
        puzzle = convert(values.values())
        stored_puzzle = chunk(puzzle)

    if event == "Restore":
        display(window, stored_puzzle)
