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
    do_add_items          -- activates AddItemsFrame view to allow user to add new items
    do_del_items          -- deletes selected item from selected car's maintenance items list
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
from PIL import ImageTk, Image


#
# Provide data/methods for the ItemsFrame view
#
class ItemsFrame:

    # initialize the views contents and store data in object
    def __init__(self, master, tk):
        self.master = master
        self.tk = tk

        self.frame = Frame(self.tk, bg=self.tk.background)
        self.frame.pack(fill=BOTH, expand=TRUE)

        # Create and insert phone background image
        load_file = "phone-background.png"
        img = Image.open(load_file)
        photo = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_panel.image = photo
        self.img_panel.place(x=0, y=0, relwidth=1, relheight=1, anchor=NW)
        load_file = "phone-hdr.png"
        img = Image.open(load_file)
        photo = ImageTk.PhotoImage(img)
        self.img_hdr_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_hdr_panel.image = photo
        self.img_hdr_panel.place(x=20, y=80, anchor=NW)

        # Create cancel button to return to previous view
        self.cancel_button = Button(self.frame, text="←", command=self.do_cancel,
                                    font=("Helvetica", 16), bg=self.tk.background)
        self.cancel_button.config(borderwidth=0)
        self.cancel_button.place(x=10, y=95, anchor=NW)

        # Create and insert car image
        load_file = "car.png"
        img = Image.open(load_file)
        img = img.resize((25,25),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_panel.image = photo
        self.img_panel.place(x=150, y=115, anchor=CENTER)

        # Create label to identify the car selected
        self.car_name_label = Label(self.frame, text="", font=("Helvetica", 16), bg=self.tk.background)
        self.car_name_label.place(x=150, y=140, anchor=CENTER)

        # Create label to identify the mileage for the car selected
        self.mileage_label = Label(self.frame, text="", font=("Helvetica", 12), bg=self.tk.background)
        self.mileage_label.place(x=150, y=175, anchor=CENTER)

        # Create button to update the selected car's mileage
        self.update_mileage_button = Button(self.frame, text="Update Mileage", command=self.do_update_mileage,
                                            font=("Helvetica", 10), bg=self.tk.background)
        self.update_mileage_button.place(x=150, y=205, anchor=CENTER)

        # Create and insert wrench image
        load_file = "wrench.png"
        img = Image.open(load_file)
        img = img.resize((30,30),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_panel.image = photo
        self.img_panel.place(x=70, y=245, anchor=CENTER)

        # Create label indicating list of maintenance items
        self.items_label = Label(self.frame, text="Maintenance Items",
                                 font=("Helvetica", 12), bg=self.tk.background)
        self.items_label.place(x=155, y=245, anchor=CENTER)

        # Create list box to show all the maintenance items for the selected car
        self.items_scrollbar = Scrollbar(self.frame, orient="vertical")
        self.items_scrollbar.place(x=270, y=265, height=200, anchor=NW)
        self.items_list_nodes = Listbox(self.frame, exportselection=0, yscrollcommand=self.items_scrollbar.set,
                                        font=("Helvetica", 12))
        self.items_list_nodes.place(x=10, y=265, anchor=NW)
        self.items_list_nodes.config(width=29)
        self.items_list_nodes.bind("<<ListboxSelect>>", self.on_item_select)
        self.items_scrollbar.config(command=self.items_list_nodes.yview)

        # Create label and drop down menu to select between updating maintenance record or deleting items in list box
        self.selection_mode_label = Label(self.frame, text="Selection Mode:", font=("Helvetica", 10),
                                          bg=self.tk.background)
        self.selection_mode_label.place(x=10, y=485, anchor=W)
        self.dropOptions=["Update Maintenance Log", "Delete Selected Item"]
        self.dropVar = StringVar()
        self.dropVar.set(self.dropOptions[0])  # default choice
        self.selection_mode_button = OptionMenu(self.frame, self.dropVar, *self.dropOptions,
                                                command=self.set_option_background)
        self.selection_mode_button.place(x=115, y=485, anchor=W)
        self.selection_mode_button.config(bg=self.tk.background)
        self.original_option_background_color = self.selection_mode_button.cget("background")

        # create add button to add maintenance items for selected car
        self.add_button = Button(self.frame, text="Add Item", command=self.do_add_items,
                                 font=("Helvetica", 10), bg=self.tk.background)
        self.add_button.place(x=15, y=530, anchor=SW)

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
        self.master.activate_update_mileage_window()

    # stores the item names for the selected car in the visible scroll list
    def build_items_list(self):
        car = cm.selections.get_car_selected()
        car_text_entry = car.replace('_', ' ')
        mileage = cm.car_data.get_mileage(car)
        msg_text = "Current Mileage: " + str(mileage)
        self.mileage_label.config(text=msg_text)
        self.car_name_label.config(text=car_text_entry)
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

    # activates the MainFrame view
    def do_cancel(self):
        self.master.activate_main_window()

    # activates the AddItemsFrame view
    def do_add_items(self):
        cm.selections.set_item_selected("")  # clear item selected, since an add is being performed
        self.master.activate_add_items_window()
 
    # delete the selected item from the car's maintenance list
    def do_del_items(self):
        car = cm.selections.get_car_selected()
        item = cm.selections.get_item_selected()
        cm.car_data.del_car_items(car, item)

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
                self.master.activate_perform_maint_window()

            # else in delete mode - delete the item, clear the ItemsFrame view and reactivate the ItemsFrame view
            else:
                self.do_del_items()

                # reset the mode back to display mode to prevent accidental deletes
                self.dropVar.set(self.dropOptions[0])
                self.selection_mode_button.config(background=self.original_option_background_color)
                self.master.activate_items_window()

