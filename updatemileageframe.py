"""
Name
    updatemileage

DESCRIPTION
    This module contains the class allowing the user to update the current mileage for a selected
    car in the maintenance list

CLASS
    UpdateMileageFrame             -- object to store methods for allowing user to update the current mileage
                                      for a selected car in the maintenance list

FUNCTION
    __init__                       -- stores master, and tk in the UpdateMileageFrame window
                                      object, and initializes the widgets in the window
                                      allowing the user update the current mileage for the
                                      selected car in the maintenance list
    do_update                      -- update the mileage in cm.car_data object and return control
                                      to the ItemsFrame object
    do_cancel                      -- returns control to the ItemsFrame object
    clear_update_mileage_window    -- calls method grid_forget() to remove the UpdateMileageFrame window
                                      from view
    activate_update_mileage_window -- sets the UpdateMileageFrame object back into view

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

# provide data/methods for the UpdateMileage view
class UpdateMileageFrame:

    # initialize the window contents and store data in object
    def __init__(self, master, tk):

        self.master = master
        self.tk = tk

        self.update_mileage_frame = Frame(self.tk)
        self.update_mileage_frame.grid(row =0, column=0, columnspan=4, sticky=N+S+E+W)

        # Create cancel button to return to previous frame
        self.cancel_button = Button(self.update_mileage_frame, text="X", command=self.do_cancel, font=("Helvetica", 16))
        self.cancel_button.config(height=2, borderwidth=0)
        self.cancel_button.grid(row=1, padx=5, pady=5, sticky=W)

        # Create label to display car name
        self.car_name_label = Label(self.update_mileage_frame, text="", font=("Helvetica", 16))
        self.car_name_label.grid(row=1, pady=5)

        # Create entry to add car's mileage to maintenance list button
        self.mileage_label = Label(self.update_mileage_frame, text="Update Current Mileage: ", font=("Helvetica", 12))
        self.mileage_label.grid(row=3, padx=10)
        self.mileage_label.config(height=2, width=30)
        self.mileage_entry=Entry(self.update_mileage_frame)
        self.mileage_entry.grid(row=4)

        # Create label to return information to the user
        self.info_label = Label(self.update_mileage_frame, text="", fg="red", font=("Helvetica", 12))
        self.info_label.grid(row=5, padx=10, pady=5)
        self.info_label.config(height=2)

        # Create update button to update and return to ItemsFrame window
        self.update_button = Button(self.update_mileage_frame, text="Update", command=self.do_update,
                                    font=("Helvetica", 10))
        self.update_button.config(height=1, borderwidth=2)
        self.update_button.grid(row=6, padx=10, pady=40, sticky=W)

    # update the mileage in cm.car_data object and return control to ItemsFrame view
    def do_update(self):
        mileage = self.mileage_entry.get()

        # validate mileage was entered as valid number
        if not v.is_valid_number(mileage):
            self.info_label.config(text="Enter mileage as a number!")
        else:
            car = cm.selections.get_car_selected()
            cm.car_data.set_mileage(car, mileage)
            self.clear_update_mileage_window()
            self.master.activate_items_window()

    # cancels the request by clearing the window and returning to the ItemsFrame view
    def do_cancel(self):
        self.clear_update_mileage_window()
        self.master.activate_items_window()

    # removes from view the UpdateMileageFrame view
    def clear_update_mileage_window(self):
        self.mileage_entry.delete(0, END)
        self.update_mileage_frame.grid_forget()

    # restores the view of the UpdateMileageFrame view
    def activate_update_mileage_window(self):
        self.update_mileage_frame.grid(column =0, row =0)
        car = cm.selections.get_car_selected()
        self.mileage_entry.insert(0, str(cm.car_data.get_mileage(car)))
        car_text_entry = car.replace('_', ' ')
        self.car_name_label.config(text=car_text_entry)
        self.info_label.config(text="")
