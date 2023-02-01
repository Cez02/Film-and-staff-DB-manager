import tkinter as tk
from tkinter import font as tkfont

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to the staff and film DB manager")
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to staff records",
                            command=lambda: controller.show_frame("StaffPage"))
        # TODO
        # button2 = tk.Button(self, text="Go to film records",
        #                     command=lambda: controller.show_frame("FilmPage"))
        button1.pack()
        # button2.pack()