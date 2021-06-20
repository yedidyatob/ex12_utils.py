from ex12_utils import *
import os

TEST_DICT_ROOT = "test-dicts"


# noinspection Duplicates
def file_path(name):
    return os.path.join(TEST_DICT_ROOT, name)


# class TestLoadWordsDict:
#
#     def test_basic(self):
#         expected = {"dog": True, "cat": True, "meow": True}
#         assert load_words_dict(file_path("alpha.txt")) == expected
#
#     def test_non_alpha(self):
#         expected = {"123": True, "!@#": True, "***": True}
#         assert load_words_dict(file_path("non-alpha.txt")) == expected
#
#     def test_spaces(self):
#         expected = {"a a": True, "b b": True}
#         assert load_words_dict(file_path("spaces.txt")) == expected
#
#     def test_empty_line(self):
#         expected = {"bob": True, "": True, "cat": True}
#         assert load_words_dict(file_path("empty-line.txt")) == expected


# noinspection Duplicates
class TestIsValidPath:

    def test_basic_row(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        path = [(0, 0), (0, 1), (0, 2)]
        assert is_valid_path(board, path, word_dict) == "CAT"

    def test_basic_col(self):
        board = [['C', 'D', 'B', 'Q'],
                 ['A', 'O', 'I', 'Q'],
                 ['T', 'G', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        path = [(0, 0), (1, 0), (2, 0)]
        assert is_valid_path(board, path, word_dict) == "CAT"

    def test_basic_diag_1(self):
        board = [['D', 'Q', 'Q', 'Q'],
                 ['Q', 'O', 'Q', 'Q'],
                 ['Q', 'Q', 'G', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BOT': True}
        path = [(0, 0), (1, 1), (2, 2)]
        assert is_valid_path(board, path, word_dict) == "DOG"

    def test_changed_direction(self):
        board = [['A', 'T', 'R', 'Q'],
                 ['Q', 'L', 'E', 'Q'],
                 ['Q', 'Q', 'B', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'ALBERT': True}
        path = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
        assert is_valid_path(board, path, word_dict) == "ALBERT"

    def test_valid_path_word_not_in_dict(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'DOG': True, 'BIT': True}
        path = [(0, 0), (0, 1), (0, 2)]
        assert is_valid_path(board, path, word_dict) is None

    def test_valid_path_word_shorter_than_in_dict(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        path = [(0, 0), (0, 1)]
        assert is_valid_path(board, path, word_dict) is None

    def test_valid_path_word_longer_than_in_dict(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        path = [(0, 0), (0, 1), (0, 2), (0, 3)]
        assert is_valid_path(board, path, word_dict) is None

    def test_path_exits_board(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        path = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
        assert is_valid_path(board, path, word_dict) is None

    def test_path_starts_outside_board(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        path = [(0, 4), (0, 3), (0, 2)]
        assert is_valid_path(board, path, word_dict) is None

    def test_same_point_twice_in_path(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        path = [(0, 0), (0, 1), (0, 0)]
        assert is_valid_path(board, path, word_dict) is None

    def test_not_adjacent_coordinates(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        path = [(0, 0), (0, 1), (2, 2)]
        assert is_valid_path(board, path, word_dict) is None

    def test_negative_coordinates(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        path = [(0, -2), (0, -1), (0, 0)]
        assert is_valid_path(board, path, word_dict) is None

    def test_empty_path(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        path = []
        assert is_valid_path(board, path, word_dict) is None

    def test_one_letter_in_dict(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'C': True, 'DOG': True, 'BIT': True}
        path = [(0, 0)]
        assert is_valid_path(board, path, word_dict) == "C"

    def test_one_letter_not_in_dict(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'P': True, 'DOG': True, 'BIT': True}
        path = [(0, 0)]
        assert is_valid_path(board, path, word_dict) is None

    def test_multi_letter_cells(self):
        board = [['Q', 'Q', 'Q', 'Q'],
                 ['DO', 'GS', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'DOGS': True}
        path = [(1, 0), (1, 1)]
        assert is_valid_path(board, path, word_dict) == "DOGS"

    def test_does_not_split_cells(self):
        board = [['Q', 'Q', 'Q', 'Q'],
                 ['DO', 'GS', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'DOG': True}
        path = [(1, 0), (1, 1)]
        assert is_valid_path(board, path, word_dict) is None


def load_words_dict(file):
    milon = open(file)
    lines = set(line.strip() for line in milon.readlines())
    milon.close()
    return lines


# noinspection Duplicates
class TestFindWords:

    # Regular cases

    def test_basic_rows(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        expected = [("CAT", [(0, 0), (0, 1), (0, 2)]),
                    ("DOG", [(1, 0), (1, 1), (1, 2)]),
                    ("BIT", [(2, 0), (2, 1), (2, 2)])]
        assert sorted(find_length_n_words(3, board, word_dict)) == \
               sorted(expected)

    def test_basic_cols(self):
        board = [['C', 'D', 'B', 'Q'],
                 ['A', 'O', 'I', 'Q'],
                 ['T', 'G', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BIT': True}
        expected = [("CAT", [(0, 0), (1, 0), (2, 0)]),
                    ("DOG", [(0, 1), (1, 1), (2, 1)]),
                    ("BIT", [(0, 2), (1, 2), (2, 2)])]
        assert sorted(find_length_n_words(3, board, word_dict)) == \
               sorted(expected)

    def test_basic_diag_1(self):
        board = [['D', 'Q', 'Q', 'Q'],
                 ['Q', 'O', 'Q', 'Q'],
                 ['Q', 'Q', 'G', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BOT': True}
        expected = [("DOG", [(0, 0), (1, 1), (2, 2)])]
        assert find_length_n_words(3, board, word_dict) == expected

    def test_basic_diag_2(self):
        board = [['Q', 'Q', 'D', 'Q'],
                 ['Q', 'O', 'Q', 'Q'],
                 ['G', 'Q', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BOT': True}
        expected = [("DOG", [(0, 2), (1, 1), (2, 0)])]
        assert find_length_n_words(3, board, word_dict) == expected

    def test_shared_letters(self):
        board = [['D', 'O', 'T', 'Q'],
                 ['O', 'Q', 'O', 'Q'],
                 ['G', 'Q', 'B', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'DOT': True, 'DOG': True, 'BOT': True}
        expected = [("DOG", [(0, 0), (1, 0), (2, 0)]),
                    ("DOT", [(0, 0), (0, 1), (0, 2)]),
                    ("BOT", [(2, 2), (1, 2), (0, 2)])]
        assert sorted(find_length_n_words(3, board, word_dict)) == \
               sorted(expected)

    def test_changed_direction(self):
        board = [['A', 'T', 'R', 'Q'],
                 ['Q', 'L', 'E', 'Q'],
                 ['Q', 'Q', 'B', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'ALBERT': True}
        expected = [("ALBERT", [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2),
                                (0, 1)])]
        assert find_length_n_words(6, board, word_dict) == expected

    # Special cases

    def test_not_use_same_letter_twice(self):
        board = [['A', 'T', 'R', 'Q'],
                 ['Q', 'L', 'E', 'Q'],
                 ['Q', 'Q', 'B', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'ALBERTA': True}
        expected = []
        assert find_length_n_words(7, board, word_dict) == expected

    def test_words_not_in_board(self):
        board = [['Q', 'Q', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q'],
                 ['Q', 'Q', 'B', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'DOT': True, 'DOG': True, 'BOT': True}
        expected = []
        assert find_length_n_words(3, board, word_dict) == expected

    def test_no_words_in_length_n_1(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'O', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BOT': True}
        expected = []
        assert find_length_n_words(2, board, word_dict) == expected

    def test_no_words_in_length_n_2(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'O', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CATH': True, 'DOGH': True, 'BOTH': True}
        expected = []
        assert find_length_n_words(3, board, word_dict) == expected

    def test_n_in_too_big(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'O', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'CAT': True, 'DOG': True, 'BOT': True}
        expected = []
        assert find_length_n_words(1000, board, word_dict) == expected

    def test_finds_correct_length_1(self):
        board = [['Q', 'Q', 'Q', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['Q', 'Q', 'I', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'DOG': True, 'DOGI': True}
        expected = [("DOG", [(1, 0), (1, 1), (1, 2)])]
        assert find_length_n_words(3, board, word_dict) == expected

    def test_finds_correct_length_2(self):
        board = [['Q', 'Q', 'Q', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['Q', 'Q', 'I', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'DOG': True, 'DOGI': True}
        expected = [("DOGI", [(1, 0), (1, 1), (1, 2), (2, 2)])]
        assert find_length_n_words(4, board, word_dict) == expected

    def test_multiple_options(self):
        board = [['Q', 'O', 'Q', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['Q', 'O', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'DOG': True}
        expected_1 = [("DOG", [(1, 0), (1, 1), (1, 2)])]
        expected_2 = [("DOG", [(1, 0), (0, 1), (1, 2)])]
        expected_3 = [("DOG", [(1, 0), (2, 1), (1, 2)])]
        actual = find_length_n_words(3, board, word_dict)
        assert sorted(actual) == sorted(expected_1 + expected_2 + expected_3)

    def test_palindrome(self):
        board = [['Q', 'Q', 'Q', 'Q'],
                 ['B', 'O', 'B', 'Q'],
                 ['Q', 'Q', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'BOB': True}
        expected_1 = [("BOB", [(1, 0), (1, 1), (1, 2)])]
        expected_2 = [("BOB", [(1, 2), (1, 1), (1, 0)])]
        actual = find_length_n_words(3, board, word_dict)
        assert sorted(actual) == sorted(expected_1 + expected_2)

    def test_single_letter_word(self):
        board = [['Q', 'Q', 'Q', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['Q', 'Q', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'D': True, 'O': True, 'G': True}
        expected = [("D", [(1, 0)]), ("O", [(1, 1)]), ("G", [(1, 2)])]
        assert sorted(find_length_n_words(1, board, word_dict)) == \
               sorted(expected)

    def test_n_is_0(self):
        board = [['Q', 'Q', 'Q', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['Q', 'Q', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'D': True, 'O': True, 'G': True}
        expected = []
        assert find_length_n_words(0, board, word_dict) == expected

    def test_multi_letter_cells(self):
        board = [['Q', 'Q', 'Q', 'Q'],
                 ['DO', 'GS', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'DOGS': True}
        expected = [("DOGS", [(1, 0), (1, 1)])]
        assert find_length_n_paths(2, board, word_dict) == expected

    def test_does_not_split_cells(self):
        board = [['Q', 'Q', 'Q', 'Q'],
                 ['DO', 'GS', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = {'DOG': True}
        expected = []
        assert find_length_n_words(2, board, word_dict) == expected

    def test_long_dict(self):
        board = [['C', 'A', 'T', 'Q'],
                 ['D', 'O', 'G', 'Q'],
                 ['B', 'I', 'T', 'Q'],
                 ['Q', 'Q', 'Q', 'Q']]
        word_dict = load_words_dict(file_path("boggle_dict.txt"))
        expected = [('ADO', [(0, 1), (1, 0), (1, 1)]),
                    ('AGO', [(0, 1), (1, 2), (1, 1)]),
                    ('BID', [(2, 0), (2, 1), (1, 0)]),
                    ('BIG', [(2, 0), (2, 1), (1, 2)]),
                    ('BIO', [(2, 0), (2, 1), (1, 1)]),
                    ('BIT', [(2, 0), (2, 1), (2, 2)]),
                    ('BOA', [(2, 0), (1, 1), (0, 1)]),
                    ('BOD', [(2, 0), (1, 1), (1, 0)]),
                    ('BOG', [(2, 0), (1, 1), (1, 2)]),
                    ('BOI', [(2, 0), (1, 1), (2, 1)]),
                    ('BOT', [(2, 0), (1, 1), (0, 2)]),
                    ('BOT', [(2, 0), (1, 1), (2, 2)]),
                    ('CAD', [(0, 0), (0, 1), (1, 0)]),
                    ('CAG', [(0, 0), (0, 1), (1, 2)]),
                    ('CAT', [(0, 0), (0, 1), (0, 2)]),
                    ('COB', [(0, 0), (1, 1), (2, 0)]),
                    ('COD', [(0, 0), (1, 1), (1, 0)]),
                    ('COG', [(0, 0), (1, 1), (1, 2)]),
                    ('COT', [(0, 0), (1, 1), (0, 2)]),
                    ('COT', [(0, 0), (1, 1), (2, 2)]),
                    ('DAG', [(1, 0), (0, 1), (1, 2)]),
                    ('DIB', [(1, 0), (2, 1), (2, 0)]),
                    ('DIG', [(1, 0), (2, 1), (1, 2)]),
                    ('DIT', [(1, 0), (2, 1), (2, 2)]),
                    ('DOB', [(1, 0), (1, 1), (2, 0)]),
                    ('DOC', [(1, 0), (1, 1), (0, 0)]),
                    ('DOG', [(1, 0), (1, 1), (1, 2)]),
                    ('DOT', [(1, 0), (1, 1), (0, 2)]),
                    ('DOT', [(1, 0), (1, 1), (2, 2)]),
                    ('GAD', [(1, 2), (0, 1), (1, 0)]),
                    ('GAT', [(1, 2), (0, 1), (0, 2)]),
                    ('GIB', [(1, 2), (2, 1), (2, 0)]),
                    ('GID', [(1, 2), (2, 1), (1, 0)]),
                    ('GIO', [(1, 2), (2, 1), (1, 1)]),
                    ('GIT', [(1, 2), (2, 1), (2, 2)]),
                    ('GOA', [(1, 2), (1, 1), (0, 1)]),
                    ('GOB', [(1, 2), (1, 1), (2, 0)]),
                    ('GOD', [(1, 2), (1, 1), (1, 0)]),
                    ('GOT', [(1, 2), (1, 1), (0, 2)]),
                    ('GOT', [(1, 2), (1, 1), (2, 2)]),
                    ('OAT', [(1, 1), (0, 1), (0, 2)]),
                    ('OBI', [(1, 1), (2, 0), (2, 1)]),
                    ('OCA', [(1, 1), (0, 0), (0, 1)]),
                    ('ODA', [(1, 1), (1, 0), (0, 1)]),
                    ('TAD', [(0, 2), (0, 1), (1, 0)]),
                    ('TAG', [(0, 2), (0, 1), (1, 2)]),
                    ('TAO', [(0, 2), (0, 1), (1, 1)]),
                    ('TID', [(2, 2), (2, 1), (1, 0)]),
                    ('TIG', [(2, 2), (2, 1), (1, 2)]),
                    ('TOC', [(0, 2), (1, 1), (0, 0)]),
                    ('TOC', [(2, 2), (1, 1), (0, 0)]),
                    ('TOD', [(0, 2), (1, 1), (1, 0)]),
                    ('TOD', [(2, 2), (1, 1), (1, 0)]),
                    ('TOG', [(0, 2), (1, 1), (1, 2)]),
                    ('TOG', [(2, 2), (1, 1), (1, 2)]),
                    ('TOT', [(0, 2), (1, 1), (2, 2)]),
                    ('TOT', [(2, 2), (1, 1), (0, 2)])]
        assert sorted(find_length_n_words(3, board, word_dict)) == expected

    def test_full_dict_random_board(self):
        board = [['T', 'G', 'O', 'T'],
                 ['R', 'D', 'B', 'F'],
                 ['H', 'N', 'U', 'P'],
                 ['N', 'A', 'S', 'N']]
        word_dict = load_words_dict(file_path("boggle_dict.txt"))
        expected_3 = [('AND', [(3, 1), (2, 1), (1, 1)]),
                      ('ANN', [(3, 1), (2, 1), (3, 0)]),
                      ('ANN', [(3, 1), (3, 0), (2, 1)]),
                      ('ANS', [(3, 1), (2, 1), (3, 2)]),
                      ('ASP', [(3, 1), (3, 2), (2, 3)]),
                      ('AUF', [(3, 1), (2, 2), (1, 3)]),
                      ('BOD', [(1, 2), (0, 2), (1, 1)]),
                      ('BOG', [(1, 2), (0, 2), (0, 1)]),
                      ('BOT', [(1, 2), (0, 2), (0, 3)]),
                      ('BUD', [(1, 2), (2, 2), (1, 1)]),
                      ('BUN', [(1, 2), (2, 2), (2, 1)]),
                      ('BUN', [(1, 2), (2, 2), (3, 3)]),
                      ('BUS', [(1, 2), (2, 2), (3, 2)]),
                      ('DOB', [(1, 1), (0, 2), (1, 2)]),
                      ('DOF', [(1, 1), (0, 2), (1, 3)]),
                      ('DOG', [(1, 1), (0, 2), (0, 1)]),
                      ('DOT', [(1, 1), (0, 2), (0, 3)]),
                      ('DUB', [(1, 1), (2, 2), (1, 2)]),
                      ('DUN', [(1, 1), (2, 2), (2, 1)]),
                      ('DUN', [(1, 1), (2, 2), (3, 3)]),
                      ('DUP', [(1, 1), (2, 2), (2, 3)]),
                      ('FOB', [(1, 3), (0, 2), (1, 2)]),
                      ('FOG', [(1, 3), (0, 2), (0, 1)]),
                      ('FUB', [(1, 3), (2, 2), (1, 2)]),
                      ('FUD', [(1, 3), (2, 2), (1, 1)]),
                      ('FUN', [(1, 3), (2, 2), (2, 1)]),
                      ('FUN', [(1, 3), (2, 2), (3, 3)]),
                      ('GOB', [(0, 1), (0, 2), (1, 2)]),
                      ('GOD', [(0, 1), (0, 2), (1, 1)]),
                      ('GOT', [(0, 1), (0, 2), (0, 3)]),
                      ('HAN', [(2, 0), (3, 1), (2, 1)]),
                      ('HAN', [(2, 0), (3, 1), (3, 0)]),
                      ('HAS', [(2, 0), (3, 1), (3, 2)]),
                      ('NAH', [(2, 1), (3, 1), (2, 0)]),
                      ('NAH', [(3, 0), (3, 1), (2, 0)]),
                      ('NAN', [(2, 1), (3, 1), (3, 0)]),
                      ('NAN', [(3, 0), (3, 1), (2, 1)]),
                      ('NAS', [(2, 1), (3, 1), (3, 2)]),
                      ('NAS', [(3, 0), (3, 1), (3, 2)]),
                      ('NUB', [(2, 1), (2, 2), (1, 2)]),
                      ('NUB', [(3, 3), (2, 2), (1, 2)]),
                      ('NUN', [(2, 1), (2, 2), (3, 3)]),
                      ('NUN', [(3, 3), (2, 2), (2, 1)]),
                      ('NUS', [(2, 1), (2, 2), (3, 2)]),
                      ('NUS', [(3, 3), (2, 2), (3, 2)]),
                      ('OFT', [(0, 2), (1, 3), (0, 3)]),
                      ('PUB', [(2, 3), (2, 2), (1, 2)]),
                      ('PUD', [(2, 3), (2, 2), (1, 1)]),
                      ('PUN', [(2, 3), (2, 2), (2, 1)]),
                      ('PUN', [(2, 3), (2, 2), (3, 3)]),
                      ('PUS', [(2, 3), (2, 2), (3, 2)]),
                      ('SAN', [(3, 2), (3, 1), (2, 1)]),
                      ('SAN', [(3, 2), (3, 1), (3, 0)]),
                      ('SAU', [(3, 2), (3, 1), (2, 2)]),
                      ('SUB', [(3, 2), (2, 2), (1, 2)]),
                      ('SUD', [(3, 2), (2, 2), (1, 1)]),
                      ('SUN', [(3, 2), (2, 2), (2, 1)]),
                      ('SUN', [(3, 2), (2, 2), (3, 3)]),
                      ('SUP', [(3, 2), (2, 2), (2, 3)]),
                      ('TOD', [(0, 3), (0, 2), (1, 1)]),
                      ('TOG', [(0, 3), (0, 2), (0, 1)]),
                      ('UDO', [(2, 2), (1, 1), (0, 2)]),
                      ('UFO', [(2, 2), (1, 3), (0, 2)]),
                      ('UNS', [(2, 2), (2, 1), (3, 2)]),
                      ('UNS', [(2, 2), (3, 3), (3, 2)]),
                      ('UPS', [(2, 2), (2, 3), (3, 2)])]
        expected_4 = [('ANNS', [(3, 1), (3, 0), (2, 1), (3, 2)]),
                      ('ANUS', [(3, 1), (2, 1), (2, 2), (3, 2)]),
                      ('BUDO', [(1, 2), (2, 2), (1, 1), (0, 2)]),
                      ('BUFO', [(1, 2), (2, 2), (1, 3), (0, 2)]),
                      ('BUNA', [(1, 2), (2, 2), (2, 1), (3, 1)]),
                      ('BUND', [(1, 2), (2, 2), (2, 1), (1, 1)]),
                      ('BUNN', [(1, 2), (2, 2), (2, 1), (3, 0)]),
                      ('BUNS', [(1, 2), (2, 2), (2, 1), (3, 2)]),
                      ('BUNS', [(1, 2), (2, 2), (3, 3), (3, 2)]),
                      ('DUAN', [(1, 1), (2, 2), (3, 1), (2, 1)]),
                      ('DUAN', [(1, 1), (2, 2), (3, 1), (3, 0)]),
                      ('DUNS', [(1, 1), (2, 2), (2, 1), (3, 2)]),
                      ('DUNS', [(1, 1), (2, 2), (3, 3), (3, 2)]),
                      ('DUPS', [(1, 1), (2, 2), (2, 3), (3, 2)]),
                      ('FUND', [(1, 3), (2, 2), (2, 1), (1, 1)]),
                      ('FUNS', [(1, 3), (2, 2), (2, 1), (3, 2)]),
                      ('FUNS', [(1, 3), (2, 2), (3, 3), (3, 2)]),
                      ('HAND', [(2, 0), (3, 1), (2, 1), (1, 1)]),
                      ('HASP', [(2, 0), (3, 1), (3, 2), (2, 3)]),
                      ('HAUD', [(2, 0), (3, 1), (2, 2), (1, 1)]),
                      ('HAUF', [(2, 0), (3, 1), (2, 2), (1, 3)]),
                      ('HAUN', [(2, 0), (3, 1), (2, 2), (2, 1)]),
                      ('HAUN', [(2, 0), (3, 1), (2, 2), (3, 3)]),
                      ('NANS', [(3, 0), (3, 1), (2, 1), (3, 2)]),
                      ('NUNS', [(2, 1), (2, 2), (3, 3), (3, 2)]),
                      ('NUNS', [(3, 3), (2, 2), (2, 1), (3, 2)]),
                      ('PUNA', [(2, 3), (2, 2), (2, 1), (3, 1)]),
                      ('PUNS', [(2, 3), (2, 2), (2, 1), (3, 2)]),
                      ('PUNS', [(2, 3), (2, 2), (3, 3), (3, 2)]),
                      ('SAND', [(3, 2), (3, 1), (2, 1), (1, 1)]),
                      ('SNUB', [(3, 2), (2, 1), (2, 2), (1, 2)]),
                      ('SNUB', [(3, 2), (3, 3), (2, 2), (1, 2)]),
                      ('SPUD', [(3, 2), (2, 3), (2, 2), (1, 1)]),
                      ('SPUN', [(3, 2), (2, 3), (2, 2), (2, 1)]),
                      ('SPUN', [(3, 2), (2, 3), (2, 2), (3, 3)]),
                      ('SUNN', [(3, 2), (2, 2), (2, 1), (3, 0)]),
                      ('TOFU', [(0, 3), (0, 2), (1, 3), (2, 2)]),
                      ('UNDO', [(2, 2), (2, 1), (1, 1), (0, 2)])]
        expected_5 = [('BUNAS', [(1, 2), (2, 2), (2, 1), (3, 1), (3, 2)]),
                      ('BUNDH', [(1, 2), (2, 2), (2, 1), (1, 1), (2, 0)]),
                      ('BUNDT', [(1, 2), (2, 2), (2, 1), (1, 1), (0, 0)]),
                      ('DUANS', [(1, 1), (2, 2), (3, 1), (2, 1), (3, 2)]),
                      ('HAUNS', [(2, 0), (3, 1), (2, 2), (2, 1), (3, 2)]),
                      ('HAUNS', [(2, 0), (3, 1), (2, 2), (3, 3), (3, 2)]),
                      ('NANDU', [(3, 0), (3, 1), (2, 1), (1, 1), (2, 2)]),
                      ('PUNAS', [(2, 3), (2, 2), (2, 1), (3, 1), (3, 2)]),
                      ('SUNNA', [(3, 2), (2, 2), (2, 1), (3, 0), (3, 1)]),
                      ('TOFUS', [(0, 3), (0, 2), (1, 3), (2, 2), (3, 2)])]
        expected_6 = [
            ('NANDUS', [(3, 0), (3, 1), (2, 1), (1, 1), (2, 2), (3, 2)]),
            ('NHANDU', [(3, 0), (2, 0), (3, 1), (2, 1), (1, 1), (2, 2)]),
            ('SANNUP', [(3, 2), (3, 1), (3, 0), (2, 1), (2, 2), (2, 3)]),
            ('SUNDOG', [(3, 2), (2, 2), (2, 1), (1, 1), (0, 2), (0, 1)]),
            ('SUNNAH', [(3, 2), (2, 2), (2, 1), (3, 0), (3, 1), (2, 0)]),
            ('UNHASP', [(2, 2), (2, 1), (2, 0), (3, 1), (3, 2), (2, 3)])]
        assert sorted(find_length_n_words(3, board, word_dict)) == expected_3
        assert sorted(find_length_n_words(4, board, word_dict)) == expected_4
        assert sorted(find_length_n_words(5, board, word_dict)) == expected_5
        assert sorted(find_length_n_words(6, board, word_dict)) == expected_6

