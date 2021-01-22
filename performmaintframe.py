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

from tkinter import *
from PIL import ImageTk, Image


#
# Provide data/methods for the PerformMaint view
#
class PerformMaintFrame:

    # initialize the window contents and store data in object
    def __init__(self, master, tk):
        self.master = master
        self.tk = tk

        self.frame = Frame(self.tk,bg=self.tk.background)
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
        self.car_name_label.place(x=150, y=150, anchor=CENTER)

        # Create and insert wrench image
        load_file = "wrench.png"
        img = Image.open(load_file)
        img = img.resize((30,30),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_panel.image = photo
        self.img_panel.place(x=150, y=200, anchor=CENTER)

        # Create label to display the selected item
        self.item_label = Label(self.frame, text="", font=("Helvetica", 16), bg=self.tk.background)
        self.item_label.place(x=150, y=230, anchor=CENTER)

        # Create button to allow user to modify the item's frequency of maintenance
        self.update_maint_item_button = Button(self.frame, command=self.do_update_item,
                                               text="View Maintenance Frequency", font=("Helvetica", 12), bg=self.tk.background)
        self.update_maint_item_button.place(x=150, y=280, anchor=CENTER)

        # Create labels to indicate recent maintenance performed
        self.maint_performed_label2 = Label(self.frame, text="Recent Maintenance Performed",
                                            font=("Helvetica", 12), bg=self.tk.background)
        self.maint_performed_label2.place(x=150, y=340, anchor=CENTER)

        # Create entry to allow user to specify the mileage frequency for the selected item
        self.last_maint_mileage_label = Label(self.frame, text="at", font=("Helvetica", 10), bg=self.tk.background)
        self.last_maint_mileage_label.place(x=30, y=385, anchor=W)
        self.last_maint_mileage_entry = Entry(self.frame, font=("Helvetica", 10))
        self.last_maint_mileage_entry.place(x=50, y=385, anchor=W)
        self.last_maint_mileage_label2 = Label(self.frame, text="miles", font=("Helvetica", 10), bg=self.tk.background)
        self.last_maint_mileage_label2.place(x=200, y=385, anchor=W)

        # Create entry to allow user to specify the time frequency in months for the selected item
        self.last_maint_date_label = Label(self.frame, text="on", font=("Helvetica", 10), bg=self.tk.background)
        self.last_maint_date_label.place(x=30, y=430, anchor=W)
        self.last_maint_date_entry = Entry(self.frame, font=("Helvetica", 10))
        self.last_maint_date_entry.place(x=50, y=430, anchor=W)
        self.last_maint_date_label2 = Label(self.frame, text="(mm/dd/yyyy)", font=("Helvetica", 10), bg=self.tk.background)
        self.last_maint_date_label2.place(x=200, y=430, anchor=W)

        # Create label to display information to the user
        self.info_label = Label(self.frame, text="", fg="red", font=("Helvetica", 10), bg=self.tk.background)
        self.info_label.place(x=150, y=460, anchor=CENTER)

        # Create button to add/update the frequency information for the selected item
        self.add_maint_perform_button = Button(self.frame, command=self.do_add,
                                               text="Save", font=("Helvetica", 12), bg=self.tk.background)
        self.add_maint_perform_button.place(x=15, y=530, anchor=SW)

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
            self.master.activate_items_window()

    # activates the AddItemsFrame view
    def do_update_item(self):
        self.master.activate_add_items_window()

    # activates the ItemsFrame view
    def do_cancel(self):
        self.master.activate_items_window()

