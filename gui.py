import PySimpleGUI as sg
import pickle
from sudoku import solve_puzzle, SUDOKU_SIZE, is_complete, backtrack


sg.ChangeLookAndFeel("GreenTan")

filename = "puzzle"


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


def save(puzzle):
    with open(filename, "wb") as file:
        pickle.dump(puzzle, file)


def load_puzzle():
    try:
        with open(filename, "rb") as file:
            loaded_puzzle = pickle.load(file)
        display(window, loaded_puzzle)
    except FileNotFoundError as e:
        print(e)


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
        # Hard puzzles need another approach
        if not is_complete(solution):
            backtrack(solution)
        display(window, solution)

    if event == "Store":
        puzzle = convert(values.values())
        puzzle = chunk(puzzle)
        save(puzzle)

    if event == "Restore":
        load_puzzle()
