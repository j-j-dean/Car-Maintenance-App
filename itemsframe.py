"""
Name
    itemsframe

DESCRIPTION
    This module contains the class allowing the user to add/update/delete selected items for a selected
    car in the maintenance list or updating the mileage for a selected car

CLASS
    ItemsFrame            -- object to store methods for allowing user to add/delete/update/select items
                             for a selected car in the maintenance list

FUNCTION
    __init__              -- stores master, and tk in the ItemsFrame window
                             object, and initializes the widgets in the window
                             allowing the user to add/delete/update items for the
                             selected car in the maintenance list
    set_option_background -- set the background color to highlight user selecting DELETE option
    do_update_mileage     -- activates the UpdateMileage view to allow user to update the current mileage
    build_items_list      -- stores the items for the selected car in the scroll list visible to the user
                             to allow for item selection
    do_cancel             -- returns control to the MainFrame view
    do_update_items       -- activates AddItemsFrame view to allow user to update the selected item
    do_add_items          -- activates AddItemsFrame view to allow user to add new items
    do_del_items          -- deletes selected item from selected car's maintenance items list
    clear_items_window    -- calls method grid_forget() to remove the ItemsFrame object from view
    activate_items_window -- activates the ItemsFrame view and restores its contents
    on_item_select        -- performs the following based on option menu selection:
                             Update Maintenance Log Item option - activates PerformMaintFrame view
                             Delete Selected Item option - delete item from car's maintenance list

DATA
    self                  -- contains the Frame object used for viewing
    self.master           -- contains the calling class to allow calling its methods
    self.tk               -- contains tkinter to allow creating window elements
                             (Labels, Buttons, Entries)
    cm.car_data           -- contains the CarMaintenance data object
    cm.selections         -- contains the user selected car name and item name
"""

import carmaintenance as cm
from tkinter import *

# provide data/methods for the ItemsFrame view
class ItemsFrame:

    # initialize the views contents and store data in object
    def __init__(self, master, tk):
        self.master = master
        self.tk = tk

        self.items_frame = Frame(self.tk)
        self.items_frame.grid(row =0, column=0, sticky=N+S+E+W)

        # Create cancel button to return to previous view
        self.cancel_button = Button(self.items_frame, text="X", command=self.do_cancel, font=("Helvetica", 16))
        self.cancel_button.config(height=2, borderwidth=0)
        self.cancel_button.grid(row=1, padx=5, pady=10, sticky=W)

        # Create label indicating list of maintenance items
        self.items_label = Label(self.items_frame, text="Maintenance Items", font=("Helvetica", 16))
        self.items_label.grid(row=1, padx=10, pady=10)
        self.items_label.config(height=2, width=15)

        # Create label to identify the car selected
        self.car_name_label = Label(self.items_frame, text="", font=("Helvetica", 12))
        self.car_name_label.grid(row=2)
        self.car_name_label.config(height=1)

        # Create label to identify the mileage for the car selected
        self.mileage_label = Label(self.items_frame, text="", font=("Helvetica", 12))
        self.mileage_label.grid(row=3)
        self.mileage_label.config(height=1)

        # Create label to display information to the user
        self.info_label = Label(self.items_frame, text="", font=("Helvetica", 10))
        self.info_label.grid(row=4, padx=5, sticky=W)

        # Create button to update the selected car's mileage
        self.update_mileage_button = Button(self.items_frame, text="Update Mileage", command=self.do_update_mileage,
                                            font=("Helvetica", 10))
        self.update_mileage_button.grid(row=4, padx=5, sticky=E)

        # Create list box to show all the maintenance items for the selected car
        self.items_scrollbar = Scrollbar(self.items_frame, orient="vertical")
        self.items_scrollbar.grid(row=5, column=1, sticky=N+S)
        self.items_list_nodes = Listbox(self.items_frame, exportselection=0, yscrollcommand=self.items_scrollbar.set,
                                        font=("Helvetica", 12))
        self.items_list_nodes.grid(row=5, column=0, padx = 5, pady = 5, sticky=N+S+E+W)
        self.items_list_nodes.config(width=30)
        self.items_list_nodes.bind("<<ListboxSelect>>", self.on_item_select)
        self.items_scrollbar.config(command=self.items_list_nodes.yview)

        # Create label and drop down menu to select between updating maintenance record or deleting items in list box
        self.selection_mode_label = Label(self.items_frame, text="Selection Mode:", font=("Helvetica", 10))
        self.selection_mode_label.grid(row=6, padx=5, pady=10, sticky=W)
        self.dropOptions=["Update Maintenance Log", "Delete Selected Item"]
        self.dropVar = StringVar()
        self.dropVar.set(self.dropOptions[0])  # default choice
        self.selection_mode_button = OptionMenu(self.items_frame, self.dropVar, *self.dropOptions,
                                                command=self.set_option_background)
        self.selection_mode_button.grid(row=6, pady=10, sticky=E)
        self.original_option_background_color = self.selection_mode_button.cget("background")

        # create add button to add maintenance items for selected car
        self.add_button = Button(self.items_frame, text="Add Item", command=self.do_add_items, font=("Helvetica", 10))
        self.add_button.config(borderwidth=2)
        self.add_button.grid(row=7, padx=10)

        # inserts the car names into the ListBox
        self.build_items_list()

    # Highlight the background color if delete mode selected
    def set_option_background(self, value):
        if value == self.dropOptions[1]: # delete mode
            self.selection_mode_button.config(background='yellow')
        else:
            self.selection_mode_button.config(background=self.original_option_background_color)

    # clears the MainFrame view and activates the UpdateMileageFrame view
    def do_update_mileage(self):
        self.clear_items_window()
        self.master.activate_update_mileage_window()

    # stores the item names for the selected car in the visible scroll list
    def build_items_list(self):
        self.items_list_nodes.delete(0, self.items_list_nodes.size())
        car = cm.selections.get_car_selected()
        items_list = cm.car_data.get_items_list(car)
        item_index=0
        for item in items_list:
            item_text_entry = item.replace('_', ' ')
            self.items_list_nodes.insert(END, item_text_entry)

            # color the item's background yellow if the maintenance is needed
            if cm.car_data.does_item_need_maintenance(car, item):
                self.items_list_nodes.itemconfig(item_index, {'bg': 'yellow'})
            else:
                self.items_list_nodes.itemconfig(item_index, {'bg': 'white'})
            item_index = item_index + 1

    # cancels the request clearing the view and returning to the MainFrame view
    def do_cancel(self):
        self.clear_items_window()
        self.master.activate_main_window()

    # sets update to True, clears the ItemsFrame view, and activates the AddItemsFrame view
    def do_update_items(self):
        self.clear_items_window()
        self.master.activate_add_items_window(update=True) # opens in update mode

    # clears the ItemsFrame view, and activates the AddItemsFrame view
    def do_add_items(self):
        cm.selections.set_item_selected("")  # clear item selected, since an add is being performed
        self.clear_items_window()
        self.master.activate_add_items_window()
 
    # delete the selected item from the car's maintenance list
    def do_del_items(self):
        car = cm.selections.get_car_selected()
        item = cm.selections.get_item_selected()
        cm.car_data.del_car_items(car, item)

    # removes from view the ItemsFrame view
    def clear_items_window(self):
        self.items_frame.grid_forget()

    # restores the view of the ItemsFrame view and restores it's contents
    def activate_items_window(self):
        self.items_frame.grid(column=0, row=0)
        car = cm.selections.get_car_selected()
        car_text_entry = car.replace('_', ' ')
        mileage = cm.car_data.get_mileage(car)
        msg_text = "Current Mileage: " + str(mileage)
        self.info_label.config(text=msg_text)
        self.car_name_label.config(text=car_text_entry)
        self.build_items_list()

    # Display Maintenance Item option selected - selection activates the PerformMaintFrame view
    # Delete Selected Item option selected - selection deletes the selected item from the car's maintenance list
    def on_item_select(self, event=None):
        curselection = self.items_list_nodes.curselection()
        if curselection:
            item_text_entry = self.items_list_nodes.get(curselection[0])
            item = item_text_entry.replace(' ', '_')
            cm.selections.set_item_selected(item)

            # if in display mode clear the view and activate the PerformMaintFrame view
            if self.dropVar.get() == "Update Maintenance Log":
                self.clear_items_window()
                self.master.activate_perform_maint_window()

            #else in delete mode - delete the item, clear the ItemsFrame view and reactivate the ItemsFrame view
            else:
                self.do_del_items()

                # reset the mode back to display mode to prevent accidental deletes
                self.dropVar.set(self.dropOptions[0])
                self.selection_mode_button.config(background=self.original_option_background_color)
                self.clear_items_window()
                self.activate_items_window()

