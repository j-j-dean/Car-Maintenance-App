"""
Name
    carmaintmain

DESCRIPTION
    This module contains the class that initializes the car maintenance user
    interface

CLASS
    CarMaintenanceGUI              -- object to support the car maintenance user interface

FUNCTION
    __init__                       -- stores tk, and car_data in the CarMaintenanceGUI
                                      object, and initializes the widgets in the view
                                      allowing the user to monitor their car maintenance
    do_exit                        -- exit the application
    activate_add_car_window        -- activates AddCarFrame object view
    activate_items_window          -- activates ItemsFrame object view
    activate_add_items_window      -- activates AddItemsFrame object view
    activate_update_mileage_window -- activates UpdateMileageFrame object view
    activate_perform_maint_window  -- activates PerformMaintFrame object view
    activate_maint_info_window     -- activates MaintInfoFrame object view
    activate_main_window           -- activates MainFrame object view

DATA
    my_gui                         -- contains the CarMaintenanceGUI object
    self.tk                        -- contains tkinter to allow creating window elements
                                      (Frames, Labels, Buttons, Entries)
    self.car_data                  -- contains the CarMaintenance data object
"""

import atexit
import carmaintenance as cm
import mainframe as mf
import addcarframe as acf
import itemsframe as itf
import additemsframe as aif
import updatemileageframe as umf
import performmaintframe as pf
import maintinfoframe as mif
from tkinter import *


#
# Provide data/methods for managing views
#
class CarMaintenanceGui:

    # initialize the view contents and store data in object
    def __init__(self):
        self.tk = Tk()
        self.tk.geometry("300x620")
        self.tk.title("Car Maintenance")
        self.tk.background = "#ddd"

        # Initialize the view for the main view
        self.frame  = mf.MainFrame(self, self.tk).frame

    # exits the application saving any unsaved data
    def do_exit(self):
        cm.store_car_maintenance_data(cm.car_data, cm.storage_file_name)
        self.tk.quit()

    # activates the AddCarFrame view
    def activate_add_car_window(self):
        self.frame.destroy()
        self.frame = acf.AddCarFrame(self,self.tk).frame

    # activates the ItemsFrame view
    def activate_items_window(self):
        self.frame.destroy()
        self.frame = itf.ItemsFrame(self, self.tk).frame

    # activates the AddItemsFrame view
    def activate_add_items_window(self):
        self.frame.destroy()
        self.frame = aif.AddItemsFrame(self, self.tk).frame

    # activates the UpdateMileageFrame view
    def activate_update_mileage_window(self):
        self.frame.destroy()
        self.frame = umf.UpdateMileageFrame(self, self.tk).frame

    # activates the PerformMaintFrame view
    def activate_perform_maint_window(self):
        self.frame.destroy()
        self.frame = pf.PerformMaintFrame(self, self.tk).frame

    # activate the MaintInfoFrame view
    def activate_maint_info_window(self):
        self.frame.destroy()
        self.frame = mif.MaintInfoFrame(self, self.tk).frame

    # activates the MainFrame view
    def activate_main_window(self):
        self.frame.destroy()
        self.frame = mf.MainFrame(self, self.tk).frame


#
# Main
#

#
# Activate and display the main window
#
my_gui = CarMaintenanceGui()
my_gui.frame.mainloop()

#
# Register the exit handler
#
atexit.register(my_gui.do_exit)




