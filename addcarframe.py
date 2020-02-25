"""
Name
    addcarframe

DESCRIPTION
    This module contains the class allowing the user to add a car to the maintenance
    list

CLASS
    AddCarFrame              -- object to store methods for allowing user to add a car to the
                                maintenance list

FUNCTION
    __init__                 -- stores master, tk, and car_data in the AddCarFrame
                                object, and initializes the widgets in the view
                                allowing the user to add cars to the maintenance list
    do_add                   -- adds an additional car entry to the CarMaintenance object
                                and returns control to the MainFrame object
    do_cancel                -- returns control to the MainFrame object
    clear_add_car_window     -- calls method grid_forget() to remove the AddCarFrame
                                object from view
    activate_add_car_window  -- sets the AddCarFrame object back into view

DATA
    self                  -- contains the Frame object used for viewing
    self.master           -- contains the calling class to allow calling its methods
    self.tk               -- contains tkinter to allow creating window elements
                             (Labels, Buttons, Entries)
    cm.car_data           -- contains the CarMaintenance data object
    cm.selections         -- contains the user selected car name and item name
"""

import carmaintenance as cm
import validation as v
from tkinter import *

#provide data/methods for the add car view
class AddCarFrame:

    # initialize the window contents and store data in object
    def __init__(self, master, tk):

        self.master = master
        self.tk = tk

        self.add_car_frame = Frame(self.tk)
        self.add_car_frame.grid(row=0, column=0, sticky=N+S+E+W)

        # Create cancel button to return to previous view
        self.cancel_button = Button(self.add_car_frame, text="X", command=self.do_cancel, font=("Helvetica", 16))
        self.cancel_button.config(borderwidth=0)
        self.cancel_button.grid(row=1, padx=5, pady=20, sticky=W)

        # Create label requesting the addition of a new car to the maintenance list
        self.add_label = Label(self.add_car_frame, text="Add New Car",font=("Helvetica", 16))
        self.add_label.grid(row=1)

        # Create entry to add a car name to the maintenance list
        self.car_name_label = Label(self.add_car_frame, text = "Enter Car Name: ", font=("Helvetica", 12))
        self.car_name_label.grid(row=2, padx=5, pady=5)
        self.car_name_label.config(width=30)
        self.car_name_entry = Entry(self.add_car_frame, command=None)
        self.car_name_entry.grid(row=3, pady=5)
        
        # Create entry to add car's mileage to the maintenance list
        self.mileage_label = Label(self.add_car_frame, text = "Enter Mileage: ", font=("Helvetica", 12))
        self.mileage_label.grid(row=4, padx=5, pady=5)
        self.mileage_entry=Entry(self.add_car_frame)
        self.mileage_entry.grid(row=5)

        # Create label to display information to the user
        self.info_label = Label(self.add_car_frame, text="", fg="red", font=("Helvetica", 12))
        self.info_label.grid(row=6, padx=5, pady=10)

        # create save button to perform the action to add the car to the maintenance list
        self.add_car_button = Button(self.add_car_frame, text="Save", command=self.do_add, font=("Helvetica", 12))
        self.add_car_button.config(borderwidth=2)
        self.add_car_button.grid(row=7, pady=30)

    # adds an additional car entry to the CarMaintenance object
    def do_add(self):

        # change blanks to underscores in car name
        car_name = self.car_name_entry.get().replace(' ', '_')

        info_text = ""

        # Verify this car is not already in the list
        if not cm.car_data.is_new_car(car_name):
            info_text = "Enter a new car name!"
        else:
            mileage = self.mileage_entry.get()

            # Verify mileage entered as a number
            if not v.is_valid_number(mileage):
                info_text = "Enter mileage as a number!"
            else:
                cm.car_data.add_car(car_name, mileage)
                self.car_name_entry.delete(0, END)
                self.mileage_entry.delete(0, END)
                cm.selections.set_car_selected(car_name)

                # clear the add car view and return to the main view
                self.clear_add_car_window()
                self.master.activate_main_window()

        # update information label
        self.info_label.config(text = info_text)

    # cancels the request by clearing the view and returning to the main view
    def do_cancel(self):
        self.clear_add_car_window()
        self.master.activate_main_window()

    # removes from view the add car view
    def clear_add_car_window(self):
        self.add_car_frame.grid_forget()

    # restores the view of the add car view and restores it's contents
    def activate_add_car_window(self):
        self.add_car_frame.grid(column =0, row =0)
        self.info_label.config(text="")
        self.car_name_entry.focus_set()

