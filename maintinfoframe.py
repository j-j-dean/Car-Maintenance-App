"""
Name
    maintinfoframe

DESCRIPTION
    This module contains the class allowing the user to display items needing maintenance and for displaying
    all recent maintenance performed for all items for all cars

CLASS
    MaintInfoFrame                -- object to store methods for allowing user to display items needing maintenance
                                     for displaying all maintenance items stored for all cars

FUNCTION
    __init__                      -- stores master, and tk in the MaintInfoFrame window
                                     object, and initializes the widgets in the window
                                     allowing the user to update the mileage and date when
                                     maintenance was performed on an item for the
                                     selected car in the maintenance list
    show_recent_maint             -- displays the recent maintenance for all items stored for all cars
    do_cancel                     -- returns control to the Main Frame object
    show_maint_needed             -- displays any needed maintenance for all items stored for all cars

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
import tkinter.scrolledtext as scrolledtext
from PIL import ImageTk, Image


#
# Provide data/methods for the MaintInfo view
#
class MaintInfoFrame(Frame):

    # initialize the window contents and store data in object
    def __init__(self, master, tk):

        super(Frame).__init__()
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
                                    font=("Helvetica", 16, "bold"), bg=self.tk.background)
        self.cancel_button.config(borderwidth=0)
        self.cancel_button.place(x=10, y=95, anchor=NW)

        # Create maintenance information label
        self.info_label = Label(self.frame, text="Car Maintenance Info",
                                font=("Helvetica", 16), bg=self.tk.background)
        self.info_label.place(x=155, y=150, anchor=CENTER)

        # Create and insert wrench image
        load_file = "wrench.png"
        img = Image.open(load_file)
        img = img.resize((30,30),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.img_panel = Label(self.frame, image=photo, bg=self.tk.background)
        self.img_panel.image = photo
        self.img_panel.place(x=35, y=150, anchor=CENTER)

        # Create scrollable text box to place maintenance info into
        self.text_box = scrolledtext.ScrolledText(self.frame, width=37, height=20, font=("Helvetica", 10))
        self.text_box.place(x=9, y=170, anchor=NW)

        # Create show recent maintenance button to view recent maintenance performed
        self.recent_maint_button = Button(self.frame, text="Recent Maintenance Performed",
                                          command=self.show_recent_maint,
                                          font=("Helvetica", 10), bg=self.tk.background)
        self.recent_maint_button.config(borderwidth=2, width=24)
        self.recent_maint_button.place(x=150, y=520, anchor=CENTER)

        self.show_maint_needed()

    # display all recent maintenance performed
    def show_recent_maint(self):
        msg_text = "Previous Maintenance\n\n"
        for car in cm.car_data.get_car_list():
            msg_text += car + '\n'
            item_list = cm.car_data.get_items_list(car)
            if item_list == []:
                msg_text += ' '*5+"No items listed\n"
            else:
                for item in item_list:
                    last_miles = cm.car_data.get_item_last_mileage(car, item)
                    last_date = cm.car_data.get_item_last_date(car, item)
                    msg_text += ' '*5 + item + '\n'
                    msg_text += ' '*10 + 'Mileage: ' + str(last_miles) + '\n'
                    msg_text += ' '*10 + 'Date: ' + str(last_date) + '\n'
            msg_text += '\n'

        self.text_box.delete('1.0', END)
        self.text_box.insert(INSERT, msg_text)

    # activates the MainFrame view
    def do_cancel(self):
        self.master.activate_main_window()

    # display maintenance needed for each car in Car Maintenance list
    def show_maint_needed(self):
        cars_need_maint = False
        self.text_box.delete('1.0', END)

        # display all maintenance needed for all cars
        msg_text = "Maintenance needed for:\n\n"
        for car in cm.car_data.get_car_list():
            if cm.car_data.does_car_need_maintenance(car):
                cars_need_maint = True
                msg_text += car +"\n"
                for item in cm.car_data.get_items_list(car):
                    if cm.car_data.does_item_need_maintenance(car, item):
                        msg_text += " "*5+item+"\n"
                msg_text += "\n"
        if not cars_need_maint:
            msg_text = "No cars need maintenance at this time!"
        self.text_box.insert(INSERT, msg_text)
