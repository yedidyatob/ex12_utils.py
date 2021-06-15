from boggle_board_randomizer import LETTERS, randomize_board
from pprint import pprint
from time import time


def is_valid_path(board, path, words):
    """

    :param board:
    :param path:
    :param words:
    :return:
    """
    word = ""
    for cell in path:
        if not is_legal_cell(cell, board):
            return
        word += board[cell[0]][cell[1]]
    if word in words:
        return True


def is_legal_cell(cell, board):
    """

    :param board:
    :param cell:
    :return:
    """
    max_index = len(board) - 1
    for i in cell:
        if not 0 <= i <= max_index:
            return False
    return True


def is_neighbor(cell1, cell2):
    """
    ASSUMES CELLS ARE LEGAL! DOES NOT CHECK IF CELLS ARE VALID.
    checks if cells are neighbors (in 8 directions).
    :param cell1: tuple
    :param cell2: tuple
    :return: bool
    """

    for i in range(2):
        if abs(cell1[i] - cell2[i]) > 1:
            return False
    if cell2 != cell1:
        return True


def all_neighbors(cell):
    moves = [-1, 0, 1]
    neighbors = [(cell[0] + i, cell[1] + j) for i in moves for j in moves]
    neighbors.remove(cell)
    return neighbors


def paths_helper(n, cell, paths, board, path=None):
    if not path:
        path = []
    for neighbor in all_neighbors(cell):
        new_path = path[:] + [cell]
        if neighbor in new_path or not is_legal_cell(neighbor, board):
            continue
        elif n <= 1:
            if new_path not in paths:
                paths.append(new_path)
        # elif neighbor in new_path or not is_legal_cell(neighbor, board):
        #     continue ##########
        else:
            # path.append(cell)
            paths_helper(n - 1, neighbor, paths, board, new_path)


def find_length_n_paths(n, board, words):
    size = len(board)
    paths = []
    for i in range(size):
        for j in range(size):
            cell = (i, j)
            paths_helper(n, cell, paths, board)
    filtered = []
    for path in paths:
        word = "".join(board[cell[0]][cell[1]] for cell in path)
        if word in words:
            filtered.append(path)

    return filtered


def find_length_n_words(n, board, words):
    pass


def max_score_paths(board, words):
    pass


if __name__ == '__main__':
    bord = randomize_board(LETTERS)
    bord1 = [['O', 'R', 'E', 'Y'],
             ['E', 'J', 'U', 'H'],
             ['H', 'E', 'N', 'O'],
             ['F', 'S', 'P', 'E']]
    pprint(bord1)

    pat = [(1, 3), (2, 3), (3, 3)]
    print(is_valid_path(bord1, pat, ["HOE"]))
    start = time()
    print(find_length_n_paths(3, bord1, ["HOE"]))
    end = time()
    print(end-start)
