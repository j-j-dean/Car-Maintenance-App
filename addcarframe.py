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
# Provide data/methods for the add car view
#
class AddCarFrame:

    # initialize the window contents and store data in object
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

        # Create label requesting the addition of a new car to the maintenance list
        self.add_label = Label(self.frame, text="Add New Car",font=("Helvetica", 16),bg=self.tk.background)
        self.add_label.place(x=150, y=150, anchor=CENTER)

        # Create and insert car image
        load_file = "car.png"
        img = Image.open(load_file)
        img = img.resize((75,75),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_panel.image = photo
        self.img_panel.place(x=150, y=230, anchor=CENTER)

        # Create entry to add a car name to the maintenance list
        self.car_name_label = Label(self.frame, text="Enter Car Name:",
                                    font=("Helvetica", 12), bg=self.tk.background)
        self.car_name_label.place(x=150, y=300, anchor=CENTER)
        self.car_name_entry = Entry(self.frame, command=None)
        self.car_name_entry.place(x=150, y=335, anchor=CENTER)
        
        # Create entry to add car's mileage to the maintenance list
        self.mileage_label = Label(self.frame, text = "Enter Mileage: ", font=("Helvetica", 12), bg=self.tk.background)
        self.mileage_label.place(x=150, y=360, anchor=CENTER)
        self.mileage_entry=Entry(self.frame)
        self.mileage_entry.place(x=150, y=395, anchor=CENTER)

        # Create label to display information to the user
        self.info_label = Label(self.frame, text="", fg="red", font=("Helvetica", 12), bg=self.tk.background)
        self.info_label.place(x=150, y=430, anchor=CENTER)

        # create save button to perform the action to add the car to the maintenance list
        self.add_car_button = Button(self.frame, text="Save", command=self.do_add,
                                     font=("Helvetica", 12), bg=self.tk.background)
        self.add_car_button.place(x=15, y=530, anchor=SW)

    # adds an additional car entry to the CarMaintenance object
    def do_add(self):

        # change blanks to underscores in car name
        car_name = self.car_name_entry.get().replace(' ', '_')

        # Verify this car is not already in the list
        if not cm.car_data.is_new_car(car_name):
            self.info_label.config(text="Enter a new car name!")
        else:
            mileage = self.mileage_entry.get()

            # Verify mileage entered as a number
            if not v.is_valid_number(mileage):
                self.info_label.config(text="Enter mileage as a number!")
            else:
                cm.car_data.add_car(car_name, mileage)
                self.car_name_entry.delete(0, END)
                self.mileage_entry.delete(0, END)
                cm.selections.set_car_selected(car_name)

                # return to the main view
                self.master.activate_main_window()

    # cancels the request by returning to the main view
    def do_cancel(self):
        self.master.activate_main_window()

