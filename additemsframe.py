"""
Name
    additemsframe

DESCRIPTION
    This module contains the class allowing the user to add a maintenance item
    to the maintenance list for the selected car

CLASS
    AddItemsFrame             -- object to store methods for allowing user to add items to the
                                 maintenance list for a selected car

FUNCTION
    __init__                  -- stores master, tk, and car_data in the AddItemsFrame
                                 object, and initializes the widgets in the view
                                 allowing the user to add items to the maintenance list
                                 for a selected car
    do_add                    -- adds an additional item entry to the CarMaintenance object
                                 for a selected car and returns control to the ItemsFrame
                                 object
    do_cancel                 -- returns control to the ItemsFrame object
    clear_add_items_window    -- calls method grid_forget() to remove the AddItemsFrame
                                 object from view
    activate_add_items_window -- sets the AddItemsFrame object back into view

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

#provide data/methods for the add items window
class AddItemsFrame:

    # initialize the window contents and store data in object
    def __init__(self, master, tk):

        self.master = master
        self.tk = tk

        self.update_mode = False

        self.add_items_frame = Frame(self.tk)
        self.add_items_frame.grid(row =0, column=0, sticky=N+S+E+W)

        # Create cancel button to return to previous frame
        self.cancel_button = Button(self.add_items_frame, text="X", command=self.do_cancel, font=("Helvetica", 16))
        self.cancel_button.config(borderwidth=0)
        self.cancel_button.grid(row=1, padx=5, pady=10, sticky=W)

        # Create label to display the selected car name
        self.car_name_label = Label(self.add_items_frame, text = "", font=("Helvetica", 16))
        self.car_name_label.grid(row=1)

        # Create label to display adding/updating the maintenance item
        self.add_items_label = Label(self.add_items_frame, text = "", font=("Helvetica", 12))
        self.add_items_label.grid(row=2, padx=10)
        self.add_items_label.config(width=30)

        # Create entry for maintenance item name (ie. "Oil Change")
        self.item_name_label = Label(self.add_items_frame, text = "Enter Item Name: ", font=("Helvetica", 10))
        self.item_name_label.grid(row=4, padx=10, pady=20, sticky=W)
        self.item_name_entry = Entry(self.add_items_frame)
        self.item_name_entry.grid(row =4, padx=10, sticky=E)

        # Create perform maintenance label
        self.description_label = Label(self.add_items_frame, text = "Perform Maintenance",font=("Helvetica", 12))
        self.description_label.grid(row=5)
        self.description_label.config(height=2)

        # Create entry to allow a mileage frequency to be specified for the maintenance item
        self.mileage_freq_label = Label(self.add_items_frame, text = "every", font=("Helvetica", 10))
        self.mileage_freq_label.grid(row=6, padx=10, pady=10, sticky=W)
        self.mileage_freq_entry = Entry(self.add_items_frame)
        self.mileage_freq_entry.grid(row=6)
        self.mileage_freq_label2 = Label(self.add_items_frame, text="miles", font=("Helvetica", 10))
        self.mileage_freq_label2.grid(row=6, padx=10, sticky=E)

        # Create entry for all a time in months frequency to be specified for the maintenance item
        self.months_freq_label = Label(self.add_items_frame, text = "every", font=("Helvetica", 10))
        self.months_freq_label.grid(row=7, padx=10, sticky=W)
        self.months_freq_entry = Entry(self.add_items_frame)
        self.months_freq_entry.grid(row=7)
        self.months_freq_label2 = Label(self.add_items_frame, text = "months", font=("Helvetica", 10))
        self.months_freq_label2.grid(row=7, padx=10, sticky=E)

        # Create label to display information to the user
        self.info_label = Label(self.add_items_frame, text="", fg="red", font=("Helvetica", 12))
        self.info_label.grid(row=8, padx=5)

        # Create button to save maintenance items for the selected car
        self.additem_button = Button(self.add_items_frame, text="Save", command=self.do_add, font=("Helvetica", 10))
        self.additem_button.config(borderwidth=2)
        self.additem_button.grid(row=9)

    #add an additional item for the selected car into the CarMaintenance object
    def do_add(self):
        info_text = ""
        car = cm.selections.get_car_selected()
        item = self.item_name_entry.get().replace(' ','_')
        freq_miles = self.mileage_freq_entry.get()

        # construct error message if invalid data entered
        if not v.is_valid_number_or_blank(freq_miles): info_text = "Enter mileages as a number!"
        freq_time = self.months_freq_entry.get()
        if not v.is_valid_number_or_blank(freq_time): info_text = "Enter number of months as a number!"

        # Issue warning to user if no Maintenance Item specified
        if item == "":
            self.info_label.config(text="Please enter maintenance item!")
        else:
            # Issue validation errors
            if info_text != "":
                self.info_label.config(text=info_text)
            else:
                # If maintenance item already exists - issue item already exists error
                if not self.update_mode and not cm.car_data.is_new_item(car, item):
                    self.info_label.config(text="Maintenance item already exists!")
                else:
                    # if updating get the stored data for the last time maintenance was performed for this item
                    if self.update_mode:
                        last_maint_mileage = cm.car_data.get_item_last_mileage(car, item)
                        last_maint_date = cm.car_data.get_item_last_date(car, item)
                    else:
                        last_maint_mileage = ""
                        last_maint_date = ""

                    # update the stored information for this maintenance item
                    cm.car_data.add_car_items(car, item, freq_miles, freq_time, last_maint_mileage, last_maint_date)
                    self.clear_add_items_window()

                    # return to perform maintenance view if updating or to the items view if adding new item data
                    if self.update_mode:
                        self.master.activate_perform_maint_window()
                    else:
                        self.master.activate_items_window()

    # cancels the request by clearing the view and returning to the previous view
    def do_cancel(self):
        self.clear_add_items_window()
        if self.update_mode:
            self.master.activate_perform_maint_window()
        else:
            self.master.activate_items_window()

    # clears the add maintenance items view
    def clear_add_items_window(self):
        self.add_items_frame.grid_forget()
        self.info_label.config(text="")
        self.item_name_entry.config(state=NORMAL)
        self.item_name_entry.delete(0, END)
        self.mileage_freq_entry.delete(0, END)
        self.months_freq_entry.delete(0, END)

    # activates the add maintenance items view and restores it's contents
    def activate_add_items_window(self, update=False):
        self.add_items_frame.grid(column=0, row=0)
        car = cm.selections.get_car_selected()
        self.car_name_label.config(text=car)

        # if updating maintenance item - display stored maintenance item data
        if update:
            self.update_mode = True
            item_text_entry = cm.selections.get_item_selected()
            item = item_text_entry.replace(' ', '_')
            self.item_name_entry.insert(0, item_text_entry)
            self.item_name_entry.config(state=DISABLED)
            freq_miles = cm.car_data.get_item_freq_miles(car, item)
            if freq_miles != 0: self.mileage_freq_entry.insert(0, freq_miles)
            freq_months = cm.car_data.get_item_freq_time(car, item)
            if freq_months != 0: self.months_freq_entry.insert(0, freq_months)
            self.add_items_label.config(text="Update Maintenance Item")
        else:
            self.update_mode = False
            self.add_items_label.config(text="Add Maintenance Item")
