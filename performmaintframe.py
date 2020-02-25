"""
Name
    performmaintframe

DESCRIPTION
    This module contains the class allowing the user to update when maintenance was performed on an item
    for a selected car in the maintenance list

CLASS
    PerformMaintFrame             -- object to store methods for allowing user to update the mileage and time
                                     when maintenance was performed for a selected car in the maintenance list

FUNCTION
    __init__                      -- stores master, and tk in the PerformMaintFrame window
                                     object, and initializes the widgets in the window
                                     allowing the user to update the mileage and date when
                                     maintenance was performed on an item for the
                                     selected car in the maintenance list
    do_add                        -- store the last performed maintenance information for the selected item
    do_update_item                -- clear the PerformMaint object and activate the AddItemsFrame object view
                                     to update the maintenance item's frequency data
    do_cancel                     -- returns control to the ItemsFrame object
    clear_perform_maint_window    -- calls method grid_forget() to remove the PerformMaintFrame window from view
    activate_perform_maint_window -- sets the PerformMaintFrame object back into view

DATA
    self                          -- contains the Frame object used for viewing
    self.master                   -- contains the calling class to allow calling its methods
    self.tk                       -- contains tkinter to allow creating window elements
                                     (Labels, Buttons, Entries)
    cm.car_data                   -- contains the CarMaintenance data object
    cm.selections                 -- contains the user selected car name and item name
"""

import carmaintenance as cm
import validation as v
from datetime import datetime
from tkinter import *

# provide data/methods for the PerformMaint view
class PerformMaintFrame:

    # initialize the window contents and store data in object
    def __init__(self, master, tk):
        self.master = master
        self.tk = tk

        self.perform_maint_frame = Frame(self.tk)
        self.perform_maint_frame.grid(row =0, column=0, sticky=N+S+E+W)

        # Create cancel button to return to previous frame
        self.cancel_button = Button(self.perform_maint_frame, text="X", command=self.do_cancel, font=("Helvetica", 16))
        self.cancel_button.config(height=2, borderwidth=0)
        self.cancel_button.grid(row=1, padx=5, pady=10, sticky=W)

        # Create label to display the selected item
        self.item_label = Label(self.perform_maint_frame, text="", font=("Helvetica", 16))
        self.item_label.grid(row=1)

        # Create label to display the selected car name
        self.car_name_label = Label(self.perform_maint_frame, text = "", font=("Helvetica", 16))
        self.car_name_label.grid(row=2)
        self.car_name_label.config(width=25)

        # Create button to allow user to modify the item's frequency of maintenance
        self.update_maint_item_button = Button(self.perform_maint_frame, command=self.do_update_item,
                                               text="View Maintenance Frequency", font=("Helvetica", 12))
        self.update_maint_item_button.grid(row=3, padx=10, pady=10)

        # Create lables to indicate recent maintenance performed
        self.maint_performed_label1 = Label(self.perform_maint_frame, text="Recent", font=("Helvetica", 12))
        self.maint_performed_label1.grid(row=5)
        self.maint_performed_label2 = Label(self.perform_maint_frame, text="Maintenance Performed", font=("Helvetica", 12))
        self.maint_performed_label2.grid(row=6, pady=10)

        # Create entry to allow user to specify the mileage frequency for the selected item
        self.last_maint_mileage_label = Label(self.perform_maint_frame, text="at", font=("Helvetica", 10))
        self.last_maint_mileage_label.grid(row=7, padx=40, pady=10, sticky=W)
        self.last_maint_mileage_entry = Entry(self.perform_maint_frame, font=("Helvetica", 10))
        self.last_maint_mileage_entry.grid(row=7)
        self.last_maint_mileage_label2 = Label(self.perform_maint_frame, text="miles", font=("Helvetica", 10))
        self.last_maint_mileage_label2.grid(row=7, padx=25, sticky=E)

        # Create entry to allow user to specify the time frequency in months for the selected item
        self.last_maint_date_label = Label(self.perform_maint_frame, text="on", font=("Helvetica", 10))
        self.last_maint_date_label.grid(row=8, padx=40, pady=10, sticky=W)
        self.last_maint_date_entry = Entry(self.perform_maint_frame, font=("Helvetica", 10))
        self.last_maint_date_entry.grid(row=8)
        self.last_maint_date_label2 = Label(self.perform_maint_frame, text="(mm/dd/yyyy)", font=("Helvetica", 10))
        self.last_maint_date_label2.grid(row=8, padx=5, sticky=E)

        # Create label to display information to the user
        self.info_label = Label(self.perform_maint_frame, text="", font=("Helvetica", 10))
        self.info_label.grid(row=9)

        # Create button to add/update the frequency information for the selected item
        self.add_maint_perform_button = Button(self.perform_maint_frame, command=self.do_add,
                                               text="Save", font=("Helvetica", 12))
        self.add_maint_perform_button.grid(row=10, padx=10)

    # store the last performed maintenance information for the selected item
    def do_add(self):
        info_text = ""
        last_maint_mileage = self.last_maint_mileage_entry.get()

        # validate the mileage and date were entered properly
        if not v.is_valid_number_or_blank(last_maint_mileage): info_text = "Enter mileages as a number!"
        last_maint_date = self.last_maint_date_entry.get()
        if not v.is_valid_date(last_maint_date): info_text = "Enter valid date as mm/dd/yyyy!"

        # if the data was entered properly store the frequency data for the selected item
        if info_text != "":
            self.info_label.config(text=info_text)
        else:
            car = cm.selections.get_car_selected()
            item = cm.selections.get_item_selected()
            freq_mileage = cm.car_data.get_item_freq_miles(car, item)
            freq_time = cm.car_data.get_item_freq_time(car, item)
            cm.car_data.add_car_items(car, item, freq_mileage, freq_time, last_maint_mileage, last_maint_date)
            self.clear_perform_maint_window()
            self.master.activate_items_window()

    # clear the PerformMaintFrame view and activate the AddItemsFrame view
    def do_update_item(self):
        self.clear_perform_maint_window()
        self.master.activate_add_items_window(update=True)

    # clear the PerformMaintFrame view and activate the ItemsFrame view
    def do_cancel(self):
        # cancels the request clearing the delete
        self.clear_perform_maint_window()
        self.master.activate_items_window()

    # clear the PerformMaintFrame view
    def clear_perform_maint_window(self):
        # removes from view the delete car window
        self.last_maint_date_entry.delete(0, END)
        self.last_maint_mileage_entry.delete(0, END)
        self.info_label.config(text="")
        self.perform_maint_frame.grid_forget()

    # activate the PerformMaintFrame view and restores it's contents
    def activate_perform_maint_window(self):
        # restores the view of the maintenance items window
        self.perform_maint_frame.grid(column=0, row=0)
        car = cm.selections.get_car_selected()
        car_text_entry = car.replace('_', ' ')
        self.car_name_label.config(text=car_text_entry)
        item = cm.selections.get_item_selected()
        item_text_entry = item.replace('_', ' ')
        self.item_label.config(text=item_text_entry)
        last_maint_mileage = cm.car_data.get_item_last_mileage(car, item)
        if last_maint_mileage != 0: self.last_maint_mileage_entry.insert(0, last_maint_mileage)
        last_maint_date = cm.car_data.get_item_last_date(car, item)
        if last_maint_date != "": self.last_maint_date_entry.insert(0, last_maint_date)

