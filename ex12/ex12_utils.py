###################################
# Files: ex12_utils_py, gui.py
# WRITER: Yedidya_Toberman, Yedidyat, 318533197
#            Illia_FORTUS, illia_fortus, 342851284
# EXERCISE: intro2cs ex12 2021
# SITES I USED: stackoverflow for GUI
###################################

from boggle_board_randomizer import LETTERS, randomize_board

SIZE = 4
PATHS = 1
WORDS = 2


def is_valid_path(board, path, words):
    """
    checks if path is valid.
    checks include:
    1) if cell is already in path
    2) if path is not continuous
    3) cell is legal
    4) word exists in dictionsary
    :param board: list of lists (paths)
    :param path: list of tuples
    :param words: iterable of words
    :return: string if path is valid. otherwise None
    """
    word = ""
    if path:
        for index, cell in enumerate(path):
            if index != 0:
                if not is_neighbor(cell, path[index - 1]):
                    return  # check if path is continuous
            if cell in path[:index]:
                return  # check if cell appears twice
            if not is_legal_cell(cell, board):
                return
            word += board[cell[0]][cell[1]]
        if word in words:
            return word


def is_legal_cell(cell, board):
    """
    checks if cell is legal.
    meaning if coordinates exist on board.
    :param board: list of lists
    :param cell: tuple (coordinates)
    :return:bool
    """
    max_index = len(board) - 1
    for i in cell:
        if not 0 <= i <= max_index:
            return False
    return True


def get_content(cell, board):
    """
    gets content of cell in board
    :param cell: tuple of coordinates
    :param board: list of lists, making a board
    :return: string of cell content
    """
    if is_legal_cell(cell, board):
        return board[cell[0]][cell[1]]


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
    """
    neighbors are all cells touching cell, including
    diagonally. 8 in total.
    Does not check the all neighbors exist!
    :param cell: tuple
    :return: list of tuples representing cell's neighbors
    """
    moves = [-1, 0, 1]
    neighbors = [(cell[0] + i, cell[1] + j) for i in moves for j in moves]
    neighbors.remove(cell)
    return neighbors


def helper_1(n, cell, paths, board, words, func, path=None):
    """
    Helper function to find all of the paths.
    Helps both find_length_n_paths and find_length_n_words.
    :param n: length of path/words to find
    :param cell: tuple
    :param paths: list of all paths that we find
    :param board: list of lists making a board
    :param words: iterable object containing all legal words.
    :param func: int representing which function is using the helper.
    either finds words according to length of word, or according to length
    of path.
    :param path: path taken till this iteration of the function.
    list of tuples.
    :return: does not return anything. appends paths to existing list.
    """
    if not path:
        path = []
    new_path = path[:] + [cell]
    new_word = path_to_word(new_path, board)
    length = len(new_word)
    new_words = {word: 0 for word in words if new_word in word[:length]}
    if new_words:
        last_added = len(get_content(cell, board))
        if (n == last_added and func == WORDS) \
                or (n <= 1 and func == PATHS):
            if new_path not in paths:
                paths.append(new_path)
        else:
            for neighbor in all_neighbors(cell):
                if neighbor in new_path or not is_legal_cell(neighbor, board):
                    continue
                else:
                    subtract = 1
                    if func == WORDS:
                        subtract = last_added
                    helper_1(n - subtract, neighbor, paths,
                             board, new_words, func, new_path)


def path_to_word(path, board):
    """
    gets string of letters on cells in path.
    :param path: list of tuples.
    :param board: list of lists making a board
    :return: string
    """
    return "".join(board[cell[0]][cell[1]] for cell in path)


def helper_2(n, board, words, func):
    """
    Uses helper 1 to find all paths of length n.

    :param n: int
    :param board: list of lists making a board
    :param words: iterable containing strings
    :param func:int representing which function is using the helper.
    either finds words according to length of word, or according to length
    of path.
    :return: list of lists
    """
    paths = []
    for i in range(SIZE):
        for j in range(SIZE):
            cell = (i, j)
            helper_1(n, cell, paths, board, words, func)
    filtered = []
    for path in paths:
        word = "".join(board[cell[0]][cell[1]] for cell in path)
        if word in words:
            filtered.append(path)
    return filtered


def find_length_n_paths(n, board, words):
    """
    finds n length paths using helper 2

    :return: list of lists of tuples (list of paths)
    """
    return helper_2(n, board, words, PATHS)


def find_length_n_words(n, board, words):
    """
    finds n length words using helper 2

    :return: list of lists of tuples (list of paths)
    """
    return helper_2(n, board, words, WORDS)


def max_score_paths(board, words):
    """
    finds all paths of words on board. if there are multiple paths to the same
    word, finds the path that gives the most points. if they gve the same
    amount of points, keeps just one of them.
    :param board: list of lists
    :param words: iterable containing words.
    :return: list of paths that give maximum score on given board.
    """
    all_paths = {}
    longest = len(max(words, key=len)) + 1
    for i in range(1, longest):
        new_paths = {path_to_word(path, board): path for path in
                     find_length_n_paths(i, board, words)}
        for word in new_paths:
            if word in all_paths:  # finds path giving most points
                if len(new_paths[word]) > len(all_paths[word]):
                    all_paths[word] = new_paths[word]
            else:
                all_paths[word] = new_paths[word]
    return list(all_paths.values())


def readfile(file):
    """
    reads text file containing words, and puts them in a dictionary.
    values are all 0 because they dont matter.
    :param file: txt fild name
    :return: dictionary of wirds
    """
    f_words = open(file)
    lines = f_words.readlines()
    lines_dic = {line[:-1]: 0 for line in lines}
    f_words.close()
    return lines_dic

if __name__ == '__main__':
    bord = randomize_board(LETTERS)
    bord1 = [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['I', 'G', 'K', 'L'], ['M', 'N', 'O', 'P']]
    melon = ('ABC', 'CDE', 'ABCD')

    milon = readfile("boggle_dict.txt")
    from time import time
    from pprint import pprint
    start = time()
    pprint(bord1)
    print(helper_2(4,bord1, melon, WORDS))
    print(max_score_paths(bord1, melon))
    end = time()

    print(end-start)
