import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("BOGGLE")
    root.geometry("600x700")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.rowconfigure(root, 1, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    text_frame = tk.Frame(root, background="LightBlue1")
    text_frame.grid(row=0, column=0, sticky="snew")
    desk_frame = tk.Frame(root, bd=20, background="red")
    desk_frame.grid(row=1, column=0, sticky="snew")
    root.mainloop()
