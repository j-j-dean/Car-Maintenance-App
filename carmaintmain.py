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
    clear_all_windows              -- clears all the visible views
    activate_add_car_window        -- activates AddCarFrame object view
    activate_items_window          -- activates ItemsFrame object view
    activate_add_items_window      -- activates AddItemsFrame object view
    activate_update_mileage_window -- activates UpdateMileageFrame object view
    activate_perform_maint_window  -- activates PerformMaintFrame object view
    activate_maint_info_window     -- activates MaintInfoFrame object view
    activate_main_window           -- activates MainFrame object view

DATA
    my_gui                         -- contains the CarMaintenanceGUI object
    self.tk                        -- cotains tkinter to allow creating window elements
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

# provide data/methods for managing views
class CarMaintenanceGui:

    # initialize the view contents and store data in object
    def __init__(self):
        self.tk = Tk()
        self.tk.geometry("300x460")
        self.tk.title("Car Maintenance")

        # Initialize the view for entering new car data
        self.add_car_frame = acf.AddCarFrame(self, self.tk,)

        # Initialize the view for displaying maintenance item information for a selected car
        self.items_frame = itf.ItemsFrame(self, self.tk)

        # Initialize the view for adding maintenance items for a selected car
        self.add_items_frame = aif.AddItemsFrame(self, self.tk)

        # Initialize the view for adding maintenance performed information for an item for a selected car
        self.perform_maint_frame = pf.PerformMaintFrame(self, self.tk)

        # Initialize the view for updating the mileage information for selected car
        self.update_mileage_frame = umf.UpdateMileageFrame(self, self.tk)

        # Initialize the view for displaying current maintenance information
        self.maint_info_frame = mif.MaintInfoFrame(self, self.tk)

        # Initialize the view for the main view - this is invoked last to be displayed first
        self.main_frame = mf.MainFrame(self, self.tk)

        self.tk.mainloop()

    # exits the application saving any unsaved data
    def do_exit(self):
        saved_car_data = cm.store_car_maintenance_data(cm.car_data, cm.storage_file_name)
        self.tk.quit()

    # clears all views
    def clear_all_windows(self):
        self.add_car_frame.clear_add_car_window()
        self.items_frame.clear_items_window()
        self.add_items_frame.clear_add_items_window()
        self.update_mileage_frame.clear_update_mileage_window()
        self.perform_maint_frame.clear_perform_maint_window()
        self.maint_info_frame.clear_maint_info_window()
        self.main_frame.clear_main_window()

    # activates the AddCarFrame view
    def activate_add_car_window(self):
        self.clear_all_windows()
        self.add_car_frame.activate_add_car_window()

    # activates the ItemsFrame view
    def activate_items_window(self):
        self.clear_all_windows()
        self.items_frame.activate_items_window()

    # activates the AddItemsFrame view
    def activate_add_items_window(self, update=False):
        self.clear_all_windows()
        self.add_items_frame.activate_add_items_window(update)

    # activates the UpdateMileageFrame view
    def activate_update_mileage_window(self):
        self.clear_all_windows()
        self.update_mileage_frame.activate_update_mileage_window()

    # activates the PerformMaintFrame view
    def activate_perform_maint_window(self):
        self.clear_all_windows()
        self.perform_maint_frame.activate_perform_maint_window()

    # activate the MaintInfoFrame view
    def activate_maint_info_window(self):
        self.clear_all_windows()
        self.maint_info_frame.activate_maint_info_window()

    # activates the MainFrame view
    def activate_main_window(self):
        self.clear_all_windows()
        self.main_frame.activate_main_window()

#
# Main
#

#
# Activate and display the main window
#
my_gui = CarMaintenanceGui()

#
# Register the exit handler
#
atexit.register(my_gui.do_exit)




