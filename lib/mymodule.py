#################################################################
# FILE : nonogram.py
# WRITER : Alon Vizner
# EXERCISE : intro2cs1 ex8 2020
# DESCRIPTION: a program that solves a nonogram grid
# RESOURCES: http://mypy-lang.org/ , https://stackexchange.com/
#################################################################
from typing import List, Optional
from copy import deepcopy


def print_board(board: List[List[int]]) -> None:
    """
    helper function to print a board
    :param board: 2D list
    :return: None
    """
    for row in board:
        print(row)


############### Question 1 ###############


def get_blocks(row: List[int]) -> List[int]:
    """
    converts a row with 0s and 1s to a blocks list
    :param row: row with 0s and 1s
    :return: blocks list
    """
    blocks = list()
    black_squares = 0
    for num in row:
        if num == 0 and black_squares != 0:
            blocks.append(black_squares)
            black_squares = 0
        elif num == 1:
            black_squares += 1
    if black_squares > 0:
        blocks.append(black_squares)
    return blocks


def valid_row(n: int, row: List[int], blocks: List[int]) -> bool:
    """
    checks if a beginning of a row of length n matches the blocks constraints
    :param n: length of final row
    :param row: the start of a row to check
    :param blocks: constraints for a row
    :return: True if valid, false otherwise
    """
    row_blocks = get_blocks(row)
    if len(row_blocks) > len(blocks):
        return False

    if sum(row_blocks) + n - len(row) < sum(row_blocks):
        return False

    if len(row) == n:
        return row_blocks == blocks

    if len(row_blocks) == 0:
        return True

    for i in range(len(row_blocks) - 1):
        if row_blocks[i] != blocks[i]:
            return False

    if row[-1] != 0:
        return row_blocks[-1] <= blocks[len(row_blocks) - 1]
    return row_blocks[-1] == blocks[len(row_blocks) - 1]


def constraint_satisfactions(n: int, blocks: List[int]) -> List[List[int]]:
    """
    returns all valid rows of length n that satisfy the blocks constraints
    :param n: length of row
    :param blocks: list of constraints
    :return: list of valid rows
    """
    solutions: List[List[int]] = list()
    _constraint_satisfactions_helper(n, blocks, list(), solutions)
    return solutions


def _constraint_satisfactions_helper \
                (n: int, blocks: List[int],
                 curr_row: List[int], solutions: List[List[int]]) -> None:
    """
    helper function for constraint_satisfactions
    :param n: length of row
    :param blocks: list of constraints
    :param curr_row: current row
    :return: None, appends valid rows to solutions list
    """
    if len(curr_row) == n:
        if valid_row(n, curr_row, blocks):
            solutions.append(curr_row.copy())
        return

    curr_row.append(0)
    if valid_row(n, curr_row, blocks):
        _constraint_satisfactions_helper(n, blocks, curr_row, solutions)
    curr_row.pop()

    curr_row.append(1)
    if valid_row(n, curr_row, blocks):
        _constraint_satisfactions_helper(n, blocks, curr_row, solutions)
    curr_row.pop()


############### Question 2 ###############
def is_valid_placement(curr_row: List[int], blocks: List[int]) -> bool:
    """
    checks if a row is valid this far
    :param curr_row: row in grid with [0,1,-1]
    :param blocks: blocks constraints
    :return: True if valid, false otherwise
    """
    try:
        reisha = curr_row[:curr_row.index(-1)]
    except ValueError:
        reisha = curr_row

    return valid_row(len(curr_row), reisha, blocks)


def row_variations_helper(
        index: int, blocks: List[int],
        curr_row: List[int], solutions: List[List[int]]) -> None:
    """
    helper function for row_variations
    :param index: index in curr_row
    :param blocks: blocks constraints
    :param curr_row: current row being checked recursively
    :param solutions: list of all valid solutions
    :return: None
    """
    if index == len(curr_row):
        if get_blocks(curr_row) == blocks:
            solutions.append(curr_row.copy())
        return

    if curr_row[index] == 0 or curr_row[index] == 1:
        row_variations_helper(index + 1, blocks, curr_row, solutions)
        return

    curr_row[index] = 0
    if is_valid_placement(curr_row, blocks):
        row_variations_helper(index + 1, blocks, curr_row, solutions)

    curr_row[index] = 1
    if is_valid_placement(curr_row, blocks):
        row_variations_helper(index + 1, blocks, curr_row, solutions)

    curr_row[index] = -1


def row_variations(row: List[int], blocks: List[int]) -> List[List[int]]:
    """
    gets a row and returns all valid variations of that row with constraints
    :param row: row with [0,1,-1]
    :param blocks: blocks constraints
    :return: list of all valid rows
    """

    if -1 not in row:
        if get_blocks(row) == blocks:
            return [row]
        else:
            return list()

    solutions: List[List[int]] = list()
    row_variations_helper(0, blocks, row, solutions)
    return solutions


############### Question 3 ###############


def intersection_row(rows: List[List[int]]) -> List[int]:
    """
    gets a list of row and returns the intersection of all rows
    :param rows: list of rows with values {0,1,-1}
    :return: a row with values {0,1,-1}
    """
    if len(rows) == 0:
        return list()

    intersection = list()
    for index in range(len(rows[0])):
        index_values = list()
        for row in rows:
            index_values.append(row[index])
        if -1 in index_values:
            intersection.append(-1)
        else:
            if 0 not in index_values:
                intersection.append(1)
            elif 1 not in index_values:
                intersection.append(0)
            else:
                intersection.append(-1)

    return intersection


############### Question 4 ###############


def restart_board(row_count: int, col_count: int) -> List[List[int]]:
    """
    gets numbers of rows and columns and returns a grid
    restarted with values of -1
    :param row_count: number of rows
    :param col_count: number of columns
    :return: list of lists with values -1.
    """
    board = list()
    for i in range(row_count):
        row = list()
        for j in range(col_count):
            row.append(-1)
        board.append(row)
    return board


def solve_easy_board(board: List[List[int]],
                     constraints: List[List[List[int]]]) \
        -> Optional[List[List[int]]]:
    """
    gets a board and goes through constraints of rows and
    columns until it is solved or until no change took place.
    :param board: a restarted board
    :param constraints: list of row_constraints,col_constraints.
    :return: solved board, or partially solved board.
    """

    row_changed, col_changed = True, True

    while row_changed or col_changed:
        row_changed, col_changed = False, False
        # Change rows according to constraints
        for i, row in enumerate(board):
            all_possibilities = row_variations(row, constraints[0][i])
            if len(all_possibilities) == 0:
                return None
            intersection = intersection_row(all_possibilities)

            if row != intersection:  # if row has changed
                row_changed = True
                board[i] = intersection

        # Change columns according to constraints
        for col_index in range(len(board[0])):
            column: List[int] = list()
            for row_index in range(len(board)):
                column.append(board[row_index][col_index])
                # Form a list from column
            all_possibilities = row_variations(column,
                                               constraints[1][col_index])
            if len(all_possibilities) == 0:
                return None
            intersection = intersection_row(all_possibilities)

            if intersection != column:  # if column has changed
                col_changed = True
                for row_index in range(len(board)):
                    board[row_index][col_index] = intersection[row_index]

    return board


############### Question 5 ###############


def solve_easy_nonogram(constraints: List[List[List[int]]]) \
        -> Optional[List[List[int]]]:
    """
    gets a constraints list and solves the board
    :param constraints: a list of constraints
     [row_constraints,column_constraints]
    :return: a valid solved grid if such exists, partial solution otherwise
    """
    row_count = len(constraints[0])
    col_count = len(constraints[1])
    board = restart_board(row_count, col_count)
    solved = solve_easy_board(board, constraints)

    return solved


def solve_nonogram(
        constraints: List[List[List[int]]]) -> List[List[List[int]]]:
    """
    returns all solutions to a board
    :param constraints: a list of constraints
    [row_constraints,column_constraints]
    :return: a list with all valid solutions to the board,
    or an empty list if such doesn't exist
    """
    solutions: List[List[List[int]]] = list()
    sum1 = sum([sum(x) for x in constraints[0]])
    sum2 = sum([sum(x) for x in constraints[1]])
    if sum1 != sum2:
        return solutions
    board = solve_easy_nonogram(constraints)
    if board is None:
        return solutions
    if not is_partial_solution(board):
        return [board]

    solve_nonogram_helper(0, board, solutions, constraints)
    return solutions


def solve_nonogram_helper(
        index: int, board: List[List[int]],
        solutions: List[List[List[int]]],
        constraints: List[List[List[int]]]) -> None:
    """
    recursive helper function for solve nonogram
    :param index: index of cell in board
    :param board: the current solution being checked
    :param solutions: all solutions found
    :param constraints: list of constraints
    :return: None, appends solution to solutions list
    """
    if board is None:
        return

    row_len, col_len = len(constraints[1]), len(constraints[0])
    if index == row_len * col_len:
        solutions.append(board)
        return

    col_index, row_index = index % row_len, index // row_len

    if board[row_index][col_index] == -1:
        new_board = deepcopy(board)
        new_board[row_index][col_index] = 1
        solved_board = solve_easy_board(new_board, constraints)
        solve_nonogram_helper(index + 1, solved_board, solutions, constraints)

        new_board = board
        new_board[row_index][col_index] = 0
        solved_board = solve_easy_board(new_board, constraints)
        solve_nonogram_helper(index + 1, solved_board, solutions, constraints)

    else:
        solve_nonogram_helper(index + 1, board, solutions, constraints)


def is_partial_solution(board: List[List[int]]) -> bool:
    """
    checks if the solution is the only solution or only a partial one
    :param board: a board with some solution, partial or full
    :return: True if partial solution, False if only solution
    """
    for row in board:
        for cell in row:
            if cell == -1:
                return True
    return False
