import tkinter as tk
from tkinter import font as tkfont

class FilmPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back to main menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()