"""
Name
    Mainframe

DESCRIPTION
    This module contains the class allowing the user to add/delete/update/select items for a selected
    car in the maintenance list

CLASS
    Main Frame            -- object to store methods for allowing user to perform car maintenance

FUNCTION
    __init__              -- stores master, and tk in the MainFrame window
                             object, and initializes the widgets in the window
                             allowing the user to perform car maintenance
    do_backup             -- backup the maintenance data
    do_restore            -- restore the maintenance data
    set_option_background -- set the background color to highlight user selecting DELETE option
    do_exit               -- performs exit request
    build_car_list        -- stores the car name for the selected car in the scroll list visible to the
                             user to allow for car selection
    display_items         -- clears the MainFrame view and activates the ItemsFrame view
    display_add_car       -- clears the MainFrame view and activates the AddCarFrame view
    display_info          -- clears the MainFrame view and activates the MaintInfoFrame view
    clear_main_window     -- calls method grid_forget() to clear the MainFrame view
    activate_main_window  -- activates the MainFrame view and restores it's contents
    on_car_select         -- performs the following based on option menu selection:
                             Display Maintenance Items option - activates PerformMaintFrame view
                             Delete Selected Car option - delete item from car's maintenance list

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

# provide data/methods for the MainFrame window
class MainFrame:

    # initialize the window contents and store data in object
    def __init__(self, master, tk):
        self.master = master
        self.tk = tk

        self.main_frame = Frame(self.tk)
        self.main_frame.grid(row =0, column=0, sticky=N+S+E+W)

        # Create cancel button to return to previous view
        self.exit_button = Button(self.main_frame, text="X", bd=0, command=self.do_exit, font=("Helvetica", 18))
        self.exit_button.grid(row=1, padx=5, pady=5, sticky=W)

        # Create backup button to backup the car maintenance data
        self.backup_button = Button(self.main_frame, text="Backup", command=self.do_backup, bd=0, font=("Helvetica", 10))
        self.backup_button.grid(row=1, padx=10, pady=5)
        #self.backup_button.config(state=DISABLED)

        # Restore the previously backed up car mainenance data
        self.restore_button = Button(self.main_frame, text="Restore", command=self.do_restore, bd=0, font=("Helvetica", 10))
        self.restore_button.grid(row=1, padx = 10, pady=5, sticky=E)

        # Create label to indicate the list of cars stored
        self.car_name_label = Label(self.main_frame, text="Cars", font=("Helvetica", 18))
        self.car_name_label.grid(row=2, padx=5, pady=5)
        self.car_device_label = Label(self.main_frame, text="on my device", font=("Helvetica", 10))
        self.car_device_label.grid(row=3, padx=5)

        # Create list box to show all the cars stored
        self.scrollbar = Scrollbar(self.main_frame, orient="vertical")
        self.scrollbar.grid(row =4, column=1, sticky=N+S)
        self.list_nodes = Listbox(self.main_frame, exportselection=0, yscrollcommand=self.scrollbar.set,
                                  font=("Helvetica", 12))
        self.list_nodes.grid(row=4, column=0, padx=5, pady=5, sticky=N+S+E+W)
        self.list_nodes.config(width=30)
        self.list_nodes.bind("<<ListboxSelect>>", self.on_car_select)
        self.scrollbar.config(command=self.list_nodes.yview)

        # Create label and drop down menu to select between displaying maintenance info or deleting cars in list box
        self.selection_mode_label = Label(self.main_frame, text="Selection Mode:", font=("Helvetica", 10))
        self.selection_mode_label.grid(row=6, padx=5, pady=10, sticky=W)
        self.dropOptions=["Display Maintenance Items", "Delete Selected Car"]
        self.dropVar = StringVar()
        self.dropVar.set(self.dropOptions[0])  # default choice
        self.selection_mode_button = OptionMenu(self.main_frame, self.dropVar, *self.dropOptions,
                                                command=self.set_option_background)
        self.selection_mode_button.grid(row=6, pady=10, sticky=E)
        self.original_option_background_color = self.selection_mode_button.cget("background")

        # create add button to add cars to the maintenance list
        self.add_car_button = Button(self.main_frame, text="Add Car", command=self.display_add_car, font=("Helvetica", 10))
        self.add_car_button.config(borderwidth=2, width=8)
        self.add_car_button.grid(row=7, padx=5, pady=20, sticky=W)

        # create info button to view current maintenance needs
        self.info_button = Button(self.main_frame, text="Info", command=self.display_info, font=("Helvetica", 10))
        self.info_button.config(borderwidth=2, width=8)
        self.info_button.grid(row=7, padx=5, sticky=E)

        # inserts the car names into the ListBox
        self.build_car_list()

    # backup the car data
    def do_backup(self):
        try:
            cm.store_car_maintenance_data(cm.car_data, cm.backup_and_restore_file_name)
        except OSError:
            print("Error backing up file to "+cm.backup_and_restore_file_name)
        else:
            self.activate_main_window()

    # restore the car data from backup file
    def do_restore(self):
        try:
            cm.car_data = cm.retrieve_car_maintenance_data(cm.backup_and_restore_file_name)
        except OSError:
            print("Error restoring from backup file "+cm.backup_and_restore_file_name)
        else:
            self.activate_main_window()

    # Highlight the background color if delete mode selected
    def set_option_background(self, value):

        # set background color to yellow if in delete mode
        if value == self.dropOptions[1]:
            self.selection_mode_button.config(background='yellow')
        else:
            self.selection_mode_button.config(background=self.original_option_background_color)

    # performs exit request
    def do_exit(self):
        self.tk.quit() # this will still invoke self.master.do_exit since it is registered exit handler

    # stores the car names for the selected cars in the visible scroll list
    def build_car_list(self):
        self.list_nodes.delete(0, self.list_nodes.size())
        car_list = cm.car_data.get_car_list()
        car_index=0
        if car_list is not None:
            for car in car_list:
                car_text_entry = car.replace('_', ' ')
                self.list_nodes.insert(END, car_text_entry)

                # set the background color to yellow if the car has items needed maintenance
                if cm.car_data.does_car_need_maintenance(car):
                    self.list_nodes.itemconfig(car_index, {'bg': 'yellow'})
                else:
                    self.list_nodes.itemconfig(car_index, {'bg': 'white'})
                car_index = car_index+1

    # clears the MainFrame view and activates the ItemsFrame view
    def display_items(self):
        self.clear_main_window()
        self.master.activate_items_window()

    # clears the MainFrame view and activates the AddCarFrame view
    def display_add_car(self):
        self.clear_main_window()
        self.master.activate_add_car_window()

    # clears the MainFrame view and activates the MaintInfo view
    def display_info(self):
        self.clear_main_window()
        self.master.activate_maint_info_window()

    # clears the MainFrame view
    def clear_main_window(self):
        self.main_frame.grid_forget()

    # activates the MainFrame view and restores it's contents
    def activate_main_window(self):
        self.main_frame.grid(column=0, row=0)
        self.build_car_list()
        # reset car selected
        cm.selections.set_car_selected("")

    # Display Maintenance Items option selected - selection activates the ItemsFrame view
    # Delete Selected Car option selected - selection deletes the selected car from the maintenance list
    def on_car_select(self, event=None):

        curselection = self.list_nodes.curselection()

        # verify actual car selected
        if curselection:
            car_text_entry = self.list_nodes.get(curselection[0])
            car = car_text_entry.replace(' ', '_')
            cm.selections.set_car_selected(car)

            # if in display mode clear the MainFrame view and activate the ItemsFrame view
            if self.dropVar.get() == "Display Maintenance Items":
                self.clear_main_window()
                self.master.activate_items_window()

            # else in delete mode - clear the MainFrame view, delete the car from the list, reactivate MainFrame view
            else:
                car = cm.selections.get_car_selected()
                cm.car_data.del_car(car)
                cm.selections.set_car_selected("")

                # reset the mode back to display mode to prevent accidental deletes
                self.dropVar.set(self.dropOptions[0])
                self.selection_mode_button.config(background=self.original_option_background_color)
                self.clear_main_window()
                self.activate_main_window()

