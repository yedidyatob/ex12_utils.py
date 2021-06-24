import tkinter as tk
import ex12_utils as utils
from functools import partial
from boggle_board_randomizer import randomize_board


class StartGame:
    """
    Class that opens start menu for the game with options to start game
    and exit from the game
    """
    START_GEOMETRY = "400x500"
    def __init__(self, root):
        self.root = root
        # define the size of the window
        root.geometry("400x500")

        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="snew")

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

        self.name_label = tk.Frame(self.main_frame, bd=20, background="LightBlue1")
        self.name_label.grid(row=0, column=0, sticky="snew")
        name = tk.Label(self.name_label, text="WELCOME\n TO\n BOGGLE!!!",
                        background="LightBlue1", fg="blue4", font=("Snap ITC", 20))
        name.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.start_label = tk.Frame(self.main_frame, bd=20, background="LightBlue1")
        self.start_label.grid(row=1, column=0, sticky="snew")
        start_button = tk.Button(self.start_label, text='START GAME', background="LightBlue1",
                                 activebackground="PaleGreen1", command=self.start_game,
                                 fg="blue4", font=("Comic Sans MS", 15, "bold"))
        start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.exit_label = tk.Frame(self.main_frame, bd=20, background="LightBlue1")
        self.exit_label.grid(row=2, column=0, sticky="snew")
        exit_button = tk.Button(self.exit_label, text='EXIT', background="LightBlue1",
                                activebackground="tomato", command=lambda: self.root.destroy(),
                                fg="blue4", font=("Comic Sans MS", 15, "bold"))
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
    All methods that control the game are realised here
    """
    # constants defined
    CELLS_IN_ROW = 4

    def __init__(self, root):

        self.word = ""
        self.path = []
        self.buttons = dict()
        self.board = randomize_board()
        self.score = 0
        self.time_limit = 180
        self.words_list = utils.readfile("boggle_dict.txt")
        self.guessed_words = []

        self._root = root
        # initialise root size
        self._root.geometry("600x750")

        tk.Grid.rowconfigure(self._root, 0, weight=1)
        tk.Grid.rowconfigure(self._root, 1, weight=1)
        tk.Grid.columnconfigure(self._root, 0, weight=1)

        self.text_frame = tk.Frame(self._root, height=150, width=600, background="LightBlue1")
        self.text_frame.grid(row=0, column=0, sticky="snew")
        # call to create info widgets
        self._create_menu(self.text_frame)

        self.desk_frame = tk.Frame(self._root, height=600, width=600, bd=20, background="LightBlue1")
        self.desk_frame.grid(row=1, column=0, sticky="snew")
        # call to create buttons grid
        self._create_grid(self.desk_frame, self.board)

        # run timer
        self.countdown(self.time_limit)
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
                                   font=("Comic Sans MS", 15, "bold"), relief=tk.GROOVE, cursor="tcross",
                                   background='mint cream', fg="blue4")
                button.bind("<Button-3>", partial(self.undo_action, i, j))
                button.grid(row=i, column=j, sticky="snew")
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
                self.buttons[(row, col)].configure(background="mint cream")
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
                self.buttons[(row, col)].configure(background="PaleGreen1")
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
                button.configure(activebackground="LightBlue1")
            else:
                button.configure(activebackground="tomato")

    def update_score(self):
        """
        Function that updates score
        :return:
        """
        self.score += int(len(self.word)) * 2
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
            self.buttons[(i, j)].configure(background="mint cream")
        self.active_background()

    def refresh_board(self):
        """
        Fucntion that is bounded to REFRESH button
        Changes all the letters on the board buttons
        :return:
        """
        self.desk_frame.destroy()
        # create board
        self.desk_frame = tk.Frame(self._root, height=600, width=600, bd=20, background="LightBlue1")
        self.desk_frame.grid(row=1, column=0, sticky="snew")
        # update path and word if refreshed
        self.path = []
        self.word = ""
        self._create_grid(self.desk_frame, utils.randomize_board())
        self.word_label["text"] = ""
        self.active_background()

    def countdown(self, count):
        """
        Fucntion which implements the timer of the game
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
        # call to change window with the same root
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
                             background="LightBlue1", fg="blue4", font=("Snap ITC", 20))
        self.word_label = tk.Label(frame, background="LightBlue1",
                                   fg="blue4", font=("Comic Sans MS", 12))
        score_label = tk.Label(frame, text="SCORE:", background="LightBlue1", fg="blue4", font=("Comic Sans MS", 12))
        self.score_value = tk.Label(frame, text="0", background="LightBlue1", fg="blue4", font=("Comic Sans MS", 12))
        time_label = tk.Label(frame, background="LightBlue1", bitmap="hourglass", fg="blue4")
        check_word = tk.Button(frame, text='CHECK', background="LightBlue1",
                               activebackground="PaleGreen1", command=self.check_word,
                               fg="blue4", font=("Comic Sans MS", 10, "bold"))
        refresh = tk.Button(frame, text='REFRESH', background="LightBlue1",
                            activebackground="PaleGreen1", command=self.refresh_board,
                            fg="blue4", font=("Comic Sans MS", 10, "bold"))
        self.timer = tk.Label(frame, background="LightBlue1", fg="blue4", font=("Comic Sans MS", 12))
        self.words = tk.Text(frame,
                             bg="LightBlue1", fg="blue4", font=("Comic Sans MS", 12), wrap=tk.WORD,
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
    def __init__(self, root, guessed_words, score):
        self.root = root
        self.guessed_words = guessed_words
        self.score = score
        # initialise root size
        root.geometry("600x750")
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        self.main_frame = tk.Frame(self.root, background="LightBlue1")
        self.main_frame.pack(expand=1, fill=tk.BOTH)
        tk.Grid.rowconfigure(self.main_frame, 0, weight=1)
        tk.Grid.rowconfigure(self.main_frame, 1, weight=1)
        tk.Grid.columnconfigure(self.main_frame, 0, weight=1)
        self.end_game()

    def end_game(self):
        """
        Function that creates all widgets on the final menu frame:
        final score, all the words guessed and two buttons - EXIT button
        and PLAY AGAIN button that do the appropriate commands
        :return:
        """
        info_frame = tk.Frame(self.main_frame, height=150, width=600, background="LightBlue1")
        info_frame.grid(row=0, column=0, sticky="snew")

        tk.Grid.rowconfigure(info_frame, 0, weight=1)
        tk.Grid.columnconfigure(info_frame, 0, weight=1)

        game_over = tk.Label(info_frame, text="GAME OVER!",
                             background="LightBlue1", fg="blue4", font=("Snap ITC", 30))
        game_over.grid(row=0, column=0, sticky="snew")

        results_frame = tk.Frame(self.main_frame, height=600, width=600, background="LightBlue1")
        results_frame.grid(row=1, column=0, sticky="snew")

        tk.Grid.rowconfigure(results_frame, 0, weight=1)
        tk.Grid.rowconfigure(results_frame, 1, weight=1)
        tk.Grid.rowconfigure(results_frame, 2, weight=1)
        tk.Grid.columnconfigure(results_frame, 0, weight=1)
        tk.Grid.columnconfigure(results_frame, 1, weight=1)

        words_guessed = tk.Label(results_frame, text="WORDS GUESSED: ",
                                 background="LightBlue1", fg="blue4", font=("Comic Sans MS", 15))
        words_guessed.grid(row=0, column=0)

        words = tk.Text(results_frame,
                        bg="LightBlue1", fg="blue4", font=("Comic Sans MS", 12),
                        relief=tk.SUNKEN, width=40, height=4, wrap=tk.WORD)
        words.insert(tk.END, self.guessed_words)
        words.grid(row=0, column=1)

        final_score = tk.Label(results_frame, text="FINAL SCORE: ",
                               background="LightBlue1", fg="blue4", font=("Comic Sans MS", 15))
        final_score.grid(row=1, column=0)

        score = tk.Label(results_frame, text=str(self.score),
                         background="LightBlue1", fg="blue4", font=("Comic Sans MS", 15))
        score.grid(row=1, column=1)

        again_button = tk.Button(results_frame, text='PLAY AGAIN', background="LightBlue1",
                                 activebackground="PaleGreen1", command=self.run_again,
                                 fg="blue4", font=("Comic Sans MS", 12, "bold"))
        again_button.grid(row=2, column=0)

        menu_button = tk.Button(results_frame, text='EXIT', background="LightBlue1",
                                activebackground="tomato", command=lambda: self.root.destroy(),
                                fg="blue4", font=("Comic Sans MS", 12, "bold"))
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


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("BOGGLE")
    StartGame(root)
    root.mainloop()
