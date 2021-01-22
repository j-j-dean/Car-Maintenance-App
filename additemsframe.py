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
    build_item_info           -- stores item information when an item was selected to be updated


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
from PIL import ImageTk, Image


#
# Provide data/methods for the add items window
#
class AddItemsFrame:

    # initialize the window contents and store data in object
    def __init__(self, master, tk):

        self.master = master
        self.tk = tk

        self.update_mode = False

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

        # Create cancel button to return to previous frame
        self.cancel_button = Button(self.frame, text="←", command=self.do_cancel,
                                    font=("Helvetica", 16), bg=self.tk.background)
        self.cancel_button.config(borderwidth=0)
        self.cancel_button.place(x=10, y=95, anchor=NW)

        # Create and insert car image
        load_file = "car.png"
        img = Image.open(load_file)
        img = img.resize((40,40),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_panel.image = photo
        self.img_panel.place(x=150, y=120, anchor=CENTER)

        # Create label to display the selected car name
        self.car_name_label = Label(self.frame, text = "", font=("Helvetica", 16), bg=self.tk.background)
        self.car_name_label.place(x=150, y=160, anchor=CENTER)

        # Create and insert wrench image
        load_file = "wrench.png"
        img = Image.open(load_file)
        img = img.resize((40,40),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_panel.image = photo
        self.img_panel.place(x=150, y=230, anchor=CENTER)

        # Create label to display adding/updating the maintenance item
        self.add_items_label = Label(self.frame, text = "", font=("Helvetica", 12), bg=self.tk.background)
        self.add_items_label.place(x=150, y=260, anchor=CENTER)

        # Create entry for maintenance item name (ie. "Oil Change")
        self.item_name_label = Label(self.frame, text = "Enter Item Name: ",
                                     font=("Helvetica", 10), bg=self.tk.background)
        self.item_name_label.place(x=30, y=310, anchor=W)
        self.item_name_entry = Entry(self.frame)
        self.item_name_entry.place(x=150, y=310, anchor=W)

        # Create perform maintenance label
        self.description_label = Label(self.frame, text = "Perform Maintenance",
                                       font=("Helvetica", 12), bg=self.tk.background)
        self.description_label.place(x=150, y=360, anchor=CENTER)

        # Create entry to allow a mileage frequency to be specified for the maintenance item
        self.mileage_freq_label = Label(self.frame, text = "every", font=("Helvetica", 10), bg=self.tk.background)
        self.mileage_freq_label.place(x=50, y=410, anchor=W)
        self.mileage_freq_entry = Entry(self.frame)
        self.mileage_freq_entry.place(x=100, y=410, anchor=W)
        self.mileage_freq_label2 = Label(self.frame, text="miles", font=("Helvetica", 10), bg=self.tk.background)
        self.mileage_freq_label2.place(x=230, y=410, anchor=W)

        # Create entry to specify a time in months (frequency) to be specified for the maintenance item
        self.months_freq_label = Label(self.frame, text = "every", font=("Helvetica", 10), bg=self.tk.background)
        self.months_freq_label.place(x=50, y=440, anchor=W)
        self.months_freq_entry = Entry(self.frame)
        self.months_freq_entry.place(x=100, y=440, anchor=W)
        self.months_freq_label2 = Label(self.frame, text = "months", font=("Helvetica", 10), bg=self.tk.background)
        self.months_freq_label2.place(x=230, y=440, anchor=W)

        # Create label to display information to the user
        self.info_label = Label(self.frame, text="", fg="red", font=("Helvetica", 12), bg=self.tk.background)
        self.info_label.place(x=150, y=480, anchor=CENTER)

        # Create button to save maintenance items for the selected car
        self.additem_button = Button(self.frame, text="Save", command=self.do_add, font=("Helvetica", 10),bg=self.tk.background)
        self.additem_button.place(x=15, y=530, anchor=SW)

        # Build the item list and display items to the user
        self.build_item_info()

    # add an additional item for the selected car into the CarMaintenance object
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
            # If validation error issue validation error message
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

                    # return to perform maintenance view if updating or to the items view if adding new item data
                    if self.update_mode:
                        self.master.activate_perform_maint_window()
                    else:
                        self.master.activate_items_window()

    # cancels returning to the previous view
    def do_cancel(self):
        if self.update_mode:
            self.master.activate_perform_maint_window()
        else:
            self.master.activate_items_window()

    # build the item information when an update is requested
    def build_item_info(self):

        # determine if update requested based on an item being selected
        item_text_entry = cm.selections.get_item_selected()
        if item_text_entry != "":
            self.update_mode = True
        else:
            self.update_mode = False

        car = cm.selections.get_car_selected()
        car_text = car.replace('_', ' ')
        self.car_name_label.config(text=car_text)

        # if updating maintenance item - display stored maintenance item data
        if self.update_mode:
            item = cm.selections.get_item_selected()
            item_text_entry = item_text_entry.replace('_', ' ')
            self.item_name_entry.insert(0, item_text_entry)
            self.item_name_entry.config(state=DISABLED)
            freq_miles = cm.car_data.get_item_freq_miles(car, item)
            if freq_miles != 0: self.mileage_freq_entry.insert(0, freq_miles)
            freq_months = cm.car_data.get_item_freq_time(car, item)
            if freq_months != 0: self.months_freq_entry.insert(0, freq_months)
            self.add_items_label.config(text="Update Maintenance Item")
        else:
            self.add_items_label.config(text="Add Maintenance Item")
