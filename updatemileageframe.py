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
# Provide data/methods for the UpdateMileage view
#
class UpdateMileageFrame:

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

        # Create cancel button to return to previous frame
        self.cancel_button = Button(self.frame, text="←", command=self.do_cancel,
                                    font=("Helvetica", 16), bg=self.tk.background)
        self.cancel_button.config(borderwidth=0)
        self.cancel_button.place(x=10, y=95, anchor=NW)

        # Create and insert car image
        load_file = "car.png"
        img = Image.open(load_file)
        img = img.resize((75,75),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_panel.image = photo
        self.img_panel.place(x=150, y=190, anchor=CENTER)

        # Create label to display car name
        self.car_name_label = Label(self.frame, text="", font=("Helvetica", 16), bg=self.tk.background)
        self.car_name_label.place(x=150, y=250, anchor=CENTER)

        # Create entry to add car's mileage to maintenance list button
        self.update_mileage_label = Label(self.frame, text="Update Current Mileage: ",
                                   font=("Helvetica", 12), bg=self.tk.background)
        self.update_mileage_label.place(x=150, y=320, anchor=CENTER)
        self.update_mileage_entry=Entry(self.frame)
        self.update_mileage_entry.place(x=150, y=350, anchor=CENTER)

        # Create label to return information to the user
        self.info_label = Label(self.frame, text="", fg="red",
                                font=("Helvetica", 12), bg=self.tk.background)
        self.info_label.place(x=150, y=420, anchor=CENTER)

        # Create update button to update and return to ItemsFrame window
        self.update_button = Button(self.frame, text="Update Mileage", command=self.do_update,
                                    font=("Helvetica", 10), bg=self.tk.background)
        self.update_button.place(x=150, y=515, anchor=CENTER)

        car = cm.selections.get_car_selected()
        self.update_mileage_entry.insert(0, str(cm.car_data.get_mileage(car)))
        car_text_entry = car.replace('_', ' ')
        self.car_name_label.config(text=car_text_entry)
        self.info_label.config(text="")

    # update the mileage in cm.car_data object and return control to ItemsFrame view
    def do_update(self):
        mileage = self.update_mileage_entry.get()

        # validate mileage was entered as valid number
        if not v.is_valid_number(mileage):
            self.info_label.config(text="Enter mileage as a number!")
        else:
            car = cm.selections.get_car_selected()
            cm.car_data.set_mileage(car, mileage)
            self.master.activate_items_window()

    # activates the ItemsFrame view
    def do_cancel(self):
        self.master.activate_items_window()
