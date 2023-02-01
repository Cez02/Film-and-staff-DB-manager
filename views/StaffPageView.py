import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

import controllers_GUI.StaffController as StaffController

class Record(tk.Frame):
    
    def __init__(self, parent, id, firstName, lastName, speciality):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness=2)

        IDLabel = tk.Entry(self, width=5)
        IDLabel.insert(0, id)
        IDLabel.pack(side=tk.LEFT)

        firstNameStringVar = tk.StringVar()
        lastNameStringVar = tk.StringVar()
        specialityStringVar = tk.StringVar()

        def UpdateFirstName(*args):
            try:
                StaffController.UpdateStaff(id, firstNameStringVar.get(), lastName, speciality)
            except Exception as e:
                messagebox.showerror("Error", e)

        def UpdateLastName(*args):
            try:
                StaffController.UpdateStaff(id, firstName, lastNameStringVar.get(), speciality)
            except Exception as e:
                messagebox.showerror("Error", e)

        def UpdateSpeciality(*args):
            try:
                StaffController.UpdateStaff(id, firstName, lastName, specialityStringVar.get())
            except Exception as e:
                messagebox.showerror("Error", e)


        firstNameStringVar.set(firstName)
        firstNameStringVar.trace("w", callback=lambda x,y,z: UpdateFirstName())
        firstNameLabel = tk.Entry(self, width=20, textvariable=firstNameStringVar)
        firstNameLabel.pack(side=tk.LEFT)

        lastNameStringVar.set(lastName)
        lastNameStringVar.trace("w", callback=lambda x,y,z: UpdateLastName())
        lastNameLabel = tk.Entry(self, width=20, textvariable=lastNameStringVar)
        lastNameLabel.pack(side=tk.LEFT)

        specialityStringVar.set(speciality)
        specialityStringVar.trace("w", callback=lambda x,y,z: UpdateSpeciality())
        specialityLabel = tk.Entry(self, width=20, textvariable=specialityStringVar)
        specialityLabel.pack(side=tk.LEFT)

class StaffPage(tk.Frame):

    recordsContainer = None

    def RefreshRecords(self):
        for widget in self.recordsContainer.winfo_children():
            widget.destroy()

        # myscrollbar = tk.Scrollbar(self.recordsContainer, orient=tk.VERTICAL, command=self.recordsContainer.yview)
        # myscrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        allStaff = StaffController.GetAllStaff()
        for rec in allStaff:
            newRecord = Record(self.recordsContainer, rec['id'], rec['first_name'], rec['last_name'], rec['speciality'])
            newRecord.pack(side=tk.TOP, pady=10, padx=20)

    def AddStaff(self):
        firstName = simpledialog.askstring("Input", "Enter the staff's first name", parent=self)
        lastName = simpledialog.askstring("Input", "Enter the staff's last name", parent=self)
        speciality = simpledialog.askstring("Input", "Enter the staff's speciality", parent=self)

        try:
            if StaffController.AddStaff(firstName, lastName, speciality):
                messagebox.showinfo("Success", "Staff added")
            self.RefreshRecords()
        except Exception as e:
            messagebox.showerror("Error", f"Adding staff failed with error:\n{e}")

    def RemoveStaff(self):
        id = simpledialog.askinteger("Input", "Enter the staff's id", parent=self)
        try:
            if StaffController.RemoveStaffByID(id):
                messagebox.showinfo("Success", "Staff removed")
            self.RefreshRecords()
        except Exception as e:
            messagebox.showerror("Error", f"Removing staff failed with error:\n{e}")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        TopFrame = tk.Frame(self)
        TopFrame.pack(side=tk.TOP, fill=tk.X)
        LowerFrame = tk.Frame(self)
        LowerFrame.pack(side=tk.TOP, fill=tk.BOTH)

        label = tk.Label(TopFrame, text="Staff manager")
        label.pack(side="top", fill="x", pady=10)



        # Setup sidebar

        sidebarContainer = tk.Frame(master=LowerFrame, highlightbackground="black", highlightthickness=2)
        sidebarContainer.pack(side=tk.LEFT, fill=tk.Y)

        backToMainMenuButton = tk.Button(sidebarContainer, text="Back to main menu",
                           command=lambda: controller.show_frame("StartPage"))
        backToMainMenuButton.pack(padx=8, pady=12)

        addStaffButton = tk.Button(sidebarContainer, text="Add staff",
                           command=self.AddStaff)
        addStaffButton.pack(padx=8, pady=12)

        self.removeStaffButton = tk.Button(sidebarContainer, text="Remove staff",
                           command=self.RemoveStaff)
        self.removeStaffButton.pack(padx=8, pady=12)

        # Setup records part

        parentCanvas = tk.Canvas(master=LowerFrame, highlightbackground="black", highlightthickness=2)
        parentCanvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.recordsContainer = tk.Frame(master=LowerFrame)
        self.recordsContainer.pack(side=tk.RIGHT, fill=tk.BOTH)

        myscrollbar = tk.Scrollbar(parentCanvas, orient=tk.VERTICAL, command=parentCanvas.yview)
        myscrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        self.recordsContainer.bind(
            "<Configure>",
            lambda e: parentCanvas.configure(
                scrollregion=parentCanvas.bbox("all")
            )
        )

        parentCanvas.create_window((0,0), window=self.recordsContainer, anchor="nw")

        parentCanvas.configure(yscrollcommand=myscrollbar.set)

        self.RefreshRecords()

        

