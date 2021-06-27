###############################################
# FILE: gui.py
# EXERCISE: intro2cs2 ex12 2021
# DESCRIPTION: GUI for Boggle game
###############################################


import tkinter as tk
import ex12_utils as utils
from functools import partial
from boggle_board_randomizer import randomize_board


# fonts and color preferences of the game
BUTTON_BACKGROUND = "mint cream"
BACKGROUND = "LightBlue1"
NAME_FONT1 = ("Snap ITC", 20)
NAME_FONT2 = ("Snap ITC", 30)
MAIN_FONT = ("Comic Sans MS", 15, "bold")
FONT1 = ("Comic Sans MS", 15)
FONT2 = ("Comic Sans MS", 12, "bold")
POS_ACTIVE = "PaleGreen1"
NEG_ACTIVE = "tomato"
CLICKED_COLOR = "PaleGreen1"
FOREGROUND = "blue4"
STICKY = "snew"


class StartGame:
    """
    Class that opens start menu for the game with options to start game
    and to exit game
    """
    # initialise geometry of the window
    START_GEOMETRY = "400x500"

    def __init__(self, root):
        """
        start game with root, gives basic grid and dimensions.
        continues with create_window, which gives the rest of the setup.
        """
        self.root = root
        # define the size of the window
        root.geometry(self.START_GEOMETRY)

        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky=STICKY)

        # call to create widgets
        self.create_window()

    def create_window(self):
        """
        The function that creates a window of start menu and all widgets on it
        Has 3 frames with appropriate buttons or labels on them
        Start button runs the MainGame class
        Exit button destroys the GUI
        :return:
        """
        tk.Grid.rowconfigure(self.main_frame, 0, weight=1)
        tk.Grid.rowconfigure(self.main_frame, 1, weight=1)
        tk.Grid.rowconfigure(self.main_frame, 2, weight=1)
        tk.Grid.columnconfigure(self.main_frame, 0, weight=1)

        name_label = tk.Frame(self.main_frame, bd=20, background=BACKGROUND)
        name_label.grid(row=0, column=0, sticky=STICKY)
        name = tk.Label(name_label, text="WELCOME\n TO\n BOGGLE!!!",
                        background=BACKGROUND, fg=FOREGROUND, font=NAME_FONT1)
        name.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        start_label = tk.Frame(self.main_frame, bd=20, background=BACKGROUND)
        start_label.grid(row=1, column=0, sticky=STICKY)
        start_button = tk.Button(start_label, text='START GAME', background=BACKGROUND,
                                 activebackground=POS_ACTIVE, command=self.start_game,
                                 fg=FOREGROUND, font=MAIN_FONT)
        start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        exit_label = tk.Frame(self.main_frame, bd=20, background=BACKGROUND)
        exit_label.grid(row=2, column=0, sticky=STICKY)
        exit_button = tk.Button(exit_label, text='EXIT', background=BACKGROUND,
                                activebackground=NEG_ACTIVE, command=lambda: self.root.destroy(),
                                fg=FOREGROUND, font=MAIN_FONT)
        exit_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def start_game(self):
        """
        function bounded as command to exit button
        destroys main frame and starts the main game
        by calling to MainGame class
        :return:
        """
        self.main_frame.destroy()
        # call to start main game with the same root
        MainGame(self.root)


class MainGame:
    """
    The main game class that contains a 4x4 grid of buttons
    and all info fields like score, timer etc.
    """
    # constants defined
    CELLS_IN_ROW = 4
    GAME_GEOMETRY = "600x750"

    def __init__(self, root):

        """
        initialise all useful variables.
        """
        self.word = ""
        self.path = []
        self.buttons = dict()
        # board imported from given helper function
        self.board = randomize_board()
        self.score = 0
        self.time_limit = 180
        self.words_list = utils.readfile("boggle_dict.txt")
        self.guessed_words = []

        self._root = root
        # initialise root geometry
        self._root.geometry(self.GAME_GEOMETRY)

        tk.Grid.rowconfigure(self._root, 0, weight=1)
        tk.Grid.rowconfigure(self._root, 1, weight=1)
        tk.Grid.columnconfigure(self._root, 0, weight=1)

        self.text_frame = tk.Frame(self._root, height=150, width=600, background=BACKGROUND)
        self.text_frame.grid(row=0, column=0, sticky=STICKY)
        # call to create info widgets
        self._create_menu(self.text_frame)

        self.desk_frame = tk.Frame(self._root, height=600, width=600, bd=20, background=BACKGROUND)
        self.desk_frame.grid(row=1, column=0, sticky=STICKY)
        # call to create buttons grid
        self._create_grid(self.desk_frame, self.board)

        # run timer
        self.countdown(self.time_limit)
        # activate background
        self.active_background()

    def _create_grid(self, frame, board):
        """
        The function that creates 4x4 button grid
        Functions bounded to the buttons are called
        :param frame: tkinter Frame object on which the buttons are created
        :param board: 2D array of letters to be displayed on buttons
        :return:
        """
        for i in range(self.CELLS_IN_ROW):
            tk.Grid.rowconfigure(frame, i, weight=1)
            for j in range(self.CELLS_IN_ROW):
                tk.Grid.columnconfigure(frame, j, weight=1)
                button = tk.Button(frame, text=board[i][j],
                                   width=6, height=3, command=partial(self.button_action, i, j),
                                   font=MAIN_FONT, relief=tk.GROOVE, cursor="tcross",
                                   background=BUTTON_BACKGROUND, fg=FOREGROUND)
                # binding a feature: right mouse button click can undo the previous choice
                button.bind("<Button-3>", partial(self.undo_action, i, j))
                button.grid(row=i, column=j, sticky=STICKY)
                self.buttons[(i, j)] = button

    def undo_action(self, row, col, event=None):
        """
        Function that undoes the click on the button: removes the letter,
        changes color of the button and changes the path list
        :param row: int, represents the row coordinate of the button
        :param col: int, represents the column coordinate of the button
        :param event: event = None
        :return:
        """
        if self.path:
            # if current coordinates are last in path
            if (row, col) == self.path[-1]:
                self.buttons[(row, col)].configure(background=BUTTON_BACKGROUND)
                self.path.pop()
                self.word = self.word[:-1]
                self.word_label["text"] = self.word
                self.active_background()

    def button_action(self, row, col):
        """
        Function that does main button action: shows the letter on the screen,
        changes the color of the button and updates the path with the coordinates of the button
        :param row: int, represents the row coordinate of the button
        :param col: int, represents the column coordinate of the button
        :return:
        """
        if (row, col) not in self.path:
            # if the button clicked is valid
            if not self.path or utils.is_neighbor((row, col), self.path[-1]):
                self.buttons[(row, col)].configure(background=CLICKED_COLOR)
                self.path.append((row, col))
                self.word += self.buttons[(row, col)]["text"]
                self.word_label["text"] = self.word
                self.active_background()

    def active_background(self):
        """
        Function that changes active background of the buttons appropriately:
        if the button was already clicked - red, if not - blue
        :return:
        """
        for coordinate, button in self.buttons.items():
            # if the button is valid
            if (not self.path or utils.is_neighbor(coordinate, self.path[-1]))\
                    and coordinate not in self.path:
                button.configure(activebackground=POS_ACTIVE)
            else:
                button.configure(activebackground=NEG_ACTIVE)

    def update_score(self):
        """
        Function that updates score value
        :return:
        """
        self.score += int(len(self.word)) * 2
        # show an appropriate score on the screen
        self.score_value["text"] = str(self.score)

    def check_word(self):
        """
        Function that is bounded to CHECK WORD button
        Checks if the word is in the list of words, if yes -
        adds the words to the list of guessed words that is showed
        on the screen
        :return:
        """
        if self.word in self.words_list:
            # if the word is correct
            if self.word not in self.guessed_words:
                self.guessed_words.append(self.word)
                self.words.configure(state=tk.NORMAL)
                self.words.insert(tk.END, self.word + " ")
                self.words.configure(state=tk.DISABLED)
                self.update_score()
        self.path = []
        self.word = ""
        self.word_label["text"] = self.word
        # update background for buttons
        for (i, j) in self.buttons.keys():
            self.buttons[(i, j)].configure(background=BUTTON_BACKGROUND)
        self.active_background()

    def refresh_board(self):
        """
        Function that is bounded to REFRESH button
        Changes all the letters on the board buttons
        :return:
        """
        self.desk_frame.destroy()
        # create board from scratch
        self.desk_frame = tk.Frame(self._root, height=600, width=600, bd=20, background=BACKGROUND)
        self.desk_frame.grid(row=1, column=0, sticky=STICKY)
        # update path and current word when refreshed
        self.path = []
        self.word = ""
        self._create_grid(self.desk_frame, utils.randomize_board())
        self.word_label["text"] = ""
        self.active_background()

    def countdown(self, count):
        """
        Function which implements the timer of the game
        using root.after method
        Displays time left on the screen
        :param count: int, time of the game
        :return:
        """
        if count > 0:
            if len(str(count % 60)) == 1:
                self.timer["text"] = str(count // 60) + ":" + "0" + str(count % 60)
            else:
                self.timer["text"] = str(count // 60) + ":" + str(count % 60)
            # "recursive" call to root.after to get change after 1000 ms
            self._root.after(1000, self.countdown, count - 1)
        else:
            # call an appropriate function that ends current game
            self.endgame()

    def endgame(self):
        """
        Function that is called when the time ends
        Destroys all "children" of the root and calls
        to the class EndGame that opens final menu
        :return:
        """
        for child in self._root.winfo_children():
            child.destroy()
        # call to EndGame class with the same root
        EndGame(self._root, self.guessed_words, self.score)

    def _create_menu(self, frame):
        """
        Function that creates the widgets that represent information:
        timer, current score, guessed words, current word to which the letters are added
        and buttons REFRESH and CHECK WORD
        :param frame: tkinter Frame object on which all widgets are displayed
        :return:
        """
        tk.Grid.rowconfigure(frame, 0, weight=3)
        tk.Grid.rowconfigure(frame, 1, weight=1)
        tk.Grid.rowconfigure(frame, 2, weight=2)
        tk.Grid.rowconfigure(frame, 3, weight=1)
        tk.Grid.columnconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 1, weight=1)
        tk.Grid.columnconfigure(frame, 2, weight=1)
        tk.Grid.columnconfigure(frame, 3, weight=1)
        tk.Grid.columnconfigure(frame, 4, weight=1)

        game_name = tk.Label(frame, text="Find all the words!",
                             background=BACKGROUND, fg=FOREGROUND, font=NAME_FONT1)
        self.word_label = tk.Label(frame, background=BACKGROUND,
                                   fg=FOREGROUND, font=FONT1)
        score_label = tk.Label(frame, text="SCORE:", background=BACKGROUND, fg=FOREGROUND, font=FONT2)
        self.score_value = tk.Label(frame, text="0", background=BACKGROUND, fg=FOREGROUND, font=FONT2)
        time_label = tk.Label(frame, background=BACKGROUND, bitmap="hourglass", fg=FOREGROUND)
        check_word = tk.Button(frame, text='CHECK', background=BACKGROUND,
                               activebackground=POS_ACTIVE, command=self.check_word,
                               fg=FOREGROUND, font=FONT2)
        refresh = tk.Button(frame, text='REFRESH', background=BACKGROUND,
                            activebackground=POS_ACTIVE, command=self.refresh_board,
                            fg=FOREGROUND, font=FONT2)
        self.timer = tk.Label(frame, background=BACKGROUND, fg=FOREGROUND, font=FONT1)
        self.words = tk.Text(frame,
                             bg=BACKGROUND, fg=FOREGROUND, font=FONT2, wrap=tk.WORD,
                             relief=tk.SUNKEN, width=35, height=4, state=tk.DISABLED)

        game_name.grid(row=0, column=2)
        time_label.grid(row=1, column=0)
        self.timer.grid(row=1, column=1)
        score_label.grid(row=1, column=3)
        self.score_value.grid(row=1, column=4)
        self.word_label.grid(row=2, column=2)
        self.words.grid(row=3, column=2)
        check_word.grid(row=3, column=1)
        refresh.grid(row=3, column=3)


class EndGame:
    """
    The class that implements final menu in the current window
    """
    END_GEOMETRY = "600x750"

    def __init__(self, root, guessed_words, score):
        """
        initialise all useful variables.
        continues with end_game.
        """
        self.root = root
        self.guessed_words = guessed_words
        self.score = score
        # initialise root size
        root.geometry(self.END_GEOMETRY)

        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)

        self.main_frame = tk.Frame(self.root, background=BACKGROUND)
        self.main_frame.pack(expand=1, fill=tk.BOTH)
        tk.Grid.rowconfigure(self.main_frame, 0, weight=1)
        tk.Grid.rowconfigure(self.main_frame, 1, weight=1)
        tk.Grid.columnconfigure(self.main_frame, 0, weight=1)

        # call to create widgets
        self.end_game()

    def end_game(self):
        """
        Function that creates all widgets on the final menu frame:
        final score, all the words guessed and two buttons - EXIT button
        and PLAY AGAIN button that do the appropriate commands
        :return:
        """
        info_frame = tk.Frame(self.main_frame, height=150, width=600, background=BACKGROUND)
        info_frame.grid(row=0, column=0, sticky=STICKY)

        tk.Grid.rowconfigure(info_frame, 0, weight=1)
        tk.Grid.columnconfigure(info_frame, 0, weight=1)

        game_over = tk.Label(info_frame, text="GAME OVER!",
                             background=BACKGROUND, fg=FOREGROUND, font=NAME_FONT2)
        game_over.grid(row=0, column=0, sticky=STICKY)

        results_frame = tk.Frame(self.main_frame, height=600, width=600, background=BACKGROUND)
        results_frame.grid(row=1, column=0, sticky=STICKY)

        tk.Grid.rowconfigure(results_frame, 0, weight=1)
        tk.Grid.rowconfigure(results_frame, 1, weight=1)
        tk.Grid.rowconfigure(results_frame, 2, weight=1)
        tk.Grid.columnconfigure(results_frame, 0, weight=1)
        tk.Grid.columnconfigure(results_frame, 1, weight=1)

        words_guessed = tk.Label(results_frame, text="WORDS GUESSED: ",
                                 background=BACKGROUND, fg=FOREGROUND, font=MAIN_FONT)
        words_guessed.grid(row=0, column=0)

        words = tk.Text(results_frame,
                        bg=BACKGROUND, fg=FOREGROUND, font=FONT2,
                        relief=tk.SUNKEN, width=40, height=4, wrap=tk.WORD)
        words.insert(tk.END, self.guessed_words)
        words.grid(row=0, column=1)

        final_score = tk.Label(results_frame, text="FINAL SCORE: ",
                               background=BACKGROUND, fg=FOREGROUND, font=FONT1)
        final_score.grid(row=1, column=0)

        score = tk.Label(results_frame, text=str(self.score),
                         background=BACKGROUND, fg=FOREGROUND, font=FONT1)
        score.grid(row=1, column=1)

        again_button = tk.Button(results_frame, text='PLAY AGAIN', background=BACKGROUND,
                                 activebackground=POS_ACTIVE, command=self.run_again,
                                 fg=FOREGROUND, font=FONT2)
        again_button.grid(row=2, column=0)

        menu_button = tk.Button(results_frame, text='EXIT', background=BACKGROUND,
                                activebackground=NEG_ACTIVE, command=lambda: self.root.destroy(),
                                fg=FOREGROUND, font=FONT2)
        menu_button.grid(row=2, column=1)

    def run_again(self):
        """
        Function bounded to PLAY AGAIN button that runs the main game one more time
        by calling the MainGame class
        :return:
        """
        self.main_frame.destroy()
        # call with the same root to start the game
        MainGame(self.root)
