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
    clear_maint_info_window       -- calls method grid_forget() to remove the MaintInfoFrame window from view
    activate_maint_info_window    -- sets the MaintInfoFrame object back into view

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
import tkinter.scrolledtext as scrolledtext

#provide data/methods for the MaintInfo view
class MaintInfoFrame:

    # initialize the window contents and store data in object
    def __init__(self, master, tk):

        self.master = master
        self.tk = tk

        self.maint_info_frame = Frame(self.tk)
        self.maint_info_frame.grid(row=0, column=0, sticky=N+S+E+W)

        # Create cancel button to return to previous view
        self.cancel_button = Button(self.maint_info_frame, text="X", command=self.do_cancel, font=("Helvetica", 16))
        self.cancel_button.config(borderwidth=0)
        self.cancel_button.grid(row=1, padx=5, pady=20, sticky=W)

        # Create maintenance information label
        self.info_label = Label(self.maint_info_frame, text="Car Maintenance Info", font=("Helvetica", 16))
        self.info_label.grid(row=1)

        # Create scrollable text box to place maintenance info into
        self.text_box = scrolledtext.ScrolledText(self.maint_info_frame, width=40, height=20, font=("Helvetica", 10))
        self.text_box.grid(row=2)

        # Create show recent maintenance button to view recent maintenance performed
        self.recent_maint_button = Button(self.maint_info_frame, text="Recent Maintenance Performed",
                                          command=self.show_recent_maint, font=("Helvetica", 10))
        self.recent_maint_button.config(borderwidth=2, width=24)
        self.recent_maint_button.grid(row=3, pady=10)

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
                    msg_text += ' '*10 +'Mileage: ' + str(last_miles) + '\n'
                    msg_text += ' '*10 + 'Date: ' + str(last_date) + '\n'
            msg_text += '\n'

        self.text_box.delete('1.0', END)
        self.text_box.insert(INSERT, msg_text)

    # cancels the request by clearing the view and returning to the MainFrame view
    def do_cancel(self):
        self.clear_maint_info_window()
        self.master.activate_main_window()

    # removes the MaintInfo object from view
    def clear_maint_info_window(self):
        self.maint_info_frame.grid_forget()

    # activates the MaintInfo object view and restores it's contents
    def activate_maint_info_window(self):
        self.maint_info_frame.grid()
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